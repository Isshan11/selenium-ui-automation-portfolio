import base64
import json
import requests
from zipfile import ZipFile
from pathlib import Path
from csv_handler import _get_nested_path
import os

CLIENT_ID = os.getenv("XRAY_CLIENT_ID")
CLIENT_SECRET = os.getenv("XRAY_CLIENT_SECRET")
GRAPHQL_URL = "https://xray.cloud.getxray.app/api/v2/graphql"
PRELOADED = False

TEST_EXECUTION_KEY = os.getenv("TEST_EXECUTION_KEY")
if not TEST_EXECUTION_KEY:
    raise RuntimeError("TEST_EXECUTION_KEY not set")

JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

# Test-to-issue mappings are supplied at runtime so private Jira keys stay out of source control.
SCRIPT_TO_JIRA = json.loads(os.getenv("XRAY_TEST_MAPPING_JSON", "{}"))

# Authenticates with Xray before any test execution or result can be updated.
def get_access_token():
    r = requests.post(
        "https://xray.cloud.getxray.app/api/v2/authenticate",
        headers={"Content-Type": "application/json"},
        json={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
    )
    if r.status_code == 200:
        return r.json().strip('"')
    return None

# Ensures the selected Test Execution contains every automated case before results are submitted.
def add_all_tests_to_te(headers):
    global PRELOADED
    if not headers:
        print("No Xray headers")
        return
    q1 = f'''query {{
      getTestExecutions(jql: "key = {TEST_EXECUTION_KEY}", limit: 1) {{
        results {{ issueId }}
      }}
    }}'''
    r1 = requests.post(GRAPHQL_URL, headers=headers, json={"query": q1}).json()
    issue_id = r1["data"]["getTestExecutions"]["results"][0]["issueId"]

    keys_str = ", ".join(SCRIPT_TO_JIRA.values())
    q2 = f'''query {{
      getTests(jql: "key in ({keys_str})", limit: 100) {{
        results {{ issueId jira(fields:["key"]) }}
      }}
    }}'''
    r2 = requests.post(GRAPHQL_URL, headers=headers, json={"query": q2}).json()
    test_ids = [t["issueId"] for t in r2["data"]["getTests"]["results"]]
    if not test_ids:
        print("No tests found")
        return

    ids_str = ", ".join(f'"{i}"' for i in test_ids)
    m = f'''mutation {{
      addTestsToTestExecution(issueId: "{issue_id}", testIssueIds: [{ids_str}]) {{
        addedTests
        warning
      }}
    }}'''
    r3 = requests.post(GRAPHQL_URL, headers=headers, json={"query": m})
    print("Add tests response:", r3.status_code, "-", r3.text)
    PRELOADED = True

# Connects a local script to its Xray run, updates status/comment, and attaches CSV evidence.
def upload_result(script_name, status, comment=None):
    if script_name not in SCRIPT_TO_JIRA:
        print("No mapping for", script_name)
        return

    test_key = SCRIPT_TO_JIRA[script_name]
    token = get_access_token()
    if not token:
        print("No Xray token")
        return

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    global PRELOADED
    if not PRELOADED:
        add_all_tests_to_te(headers)

    res1 = requests.post(GRAPHQL_URL, headers=headers, json={
        "query": f'''query {{ getTestExecutions(jql: "key = {TEST_EXECUTION_KEY}", limit: 1) {{ results {{ issueId }} }} }}'''
    })
    try:
        issue_id = res1.json()["data"]["getTestExecutions"]["results"][0]["issueId"]
    except:
        print("No issueId for", TEST_EXECUTION_KEY)
        return

    # Resolve the run belonging to this exact Jira test before changing its result.
    res2 = requests.post(GRAPHQL_URL, headers=headers, json={
        "query": f'''query {{
            getTestExecution(issueId: "{issue_id}") {{
                testRuns(limit: 100) {{
                    results {{ id test {{ jira(fields: ["key"]) }} }}
                }}
            }}
        }}'''
    })
    try:
        runs = res2.json()["data"]["getTestExecution"]["testRuns"]["results"]
        run_id = next(r["id"] for r in runs if r["test"]["jira"]["key"] == test_key)
    except:
        print("No runId for", test_key)
        return

    msg = (comment or f"Automated update for {script_name}").replace('"""', "'''")
    requests.post(GRAPHQL_URL, headers=headers, json={
        "query": f'''mutation {{ updateTestRunStatus(id: "{run_id}", status: "{status.upper()}") }}'''
    })
    requests.post(GRAPHQL_URL, headers=headers, json={
        "query": f'''mutation {{ updateTestRunComment(id: "{run_id}", comment: \"\"\"{msg}\"\"\") }}'''
    })

    base_dir = Path(__file__).resolve().parent / "Test_Results"
    candidate_paths = [
        Path(_get_nested_path(script_name, base_dir)),
        base_dir / script_name,
        base_dir / script_name.split('_')[0] / script_name
    ]

    # Package the matching CSV and screenshots as one reviewable Jira attachment.
    for path in candidate_paths:
        if not path.exists():
            continue
        zip_path = path.parent / f"{script_name}.zip"
        try:
            with ZipFile(zip_path, 'w') as z:
                csv_file = path / f"{script_name}.csv"
                if csv_file.exists():
                    z.write(csv_file, arcname=csv_file.name)
                screenshots = path / "screenshots"
                if screenshots.exists():
                    for img in screenshots.glob("*.png"):
                        z.write(img, arcname=f"screenshots/{img.name}")
        except Exception as e:
            print("Zip fail:", e)
            return

        auth_token = base64.b64encode(f"{JIRA_EMAIL}:{JIRA_API_TOKEN}".encode()).decode()
        jira_headers = {
            "Authorization": f"Basic {auth_token}",
            "X-Atlassian-Token": "no-check"
        }
        attachment_url = f"https://{JIRA_DOMAIN}/rest/api/2/issue/{TEST_EXECUTION_KEY}/attachments"
        try:
            with open(zip_path, 'rb') as f:
                res = requests.post(
                    attachment_url,
                    headers=jira_headers,
                    files={'file': (zip_path.name, f, 'application/zip')}
                )
                print("Uploaded", zip_path.name, res.status_code, res.text)
        except Exception as e:
            print("Upload fail:", e)
        zip_path.unlink(missing_ok=True)
        break
