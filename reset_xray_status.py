import requests
import os

# === CONFIG ===
CLIENT_ID = os.getenv("XRAY_CLIENT_ID")
CLIENT_SECRET = os.getenv("XRAY_CLIENT_SECRET")
TEST_EXECUTION_KEY = os.getenv("TEST_EXECUTION_KEY")
if not TEST_EXECUTION_KEY:
    raise RuntimeError("TEST_EXECUTION_KEY environment variable not set")
GRAPHQL_URL = "https://xray.cloud.getxray.app/api/v2/graphql"

# === Get Access Token ===
def get_access_token():
    res = requests.post(
        "https://xray.cloud.getxray.app/api/v2/authenticate",
        headers={"Content-Type": "application/json"},
        json={"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET}
    )
    if res.status_code == 200:
        return res.json().strip('"')
    else:
        print("Token fetch failed:", res.status_code, res.text)
        return None

# === Get Test Run IDs in the selected Test Execution ===
def get_test_run_ids(test_exec_key, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Step 1
    query_1 = {
        "query": f'''
        query {{
          getTestExecutions(jql: "key = {test_exec_key}", limit: 1) {{
            results {{
              issueId
            }}
          }}
        }}
        '''
    }

    res1 = requests.post(GRAPHQL_URL, headers=headers, json=query_1)
    print("[XRAY] Step 1 Response:", res1.text)

    try:
        issue_id = res1.json()["data"]["getTestExecutions"]["results"][0]["issueId"]
    except Exception as e:
        print("Could not extract issueId:", e)
        return []

    # Step 2
    query_2 = {
        "query": f'''
        query {{
          getTestExecution(issueId: "{issue_id}") {{
            testRuns(limit: 100) {{
              results {{
                id
              }}
            }}
          }}
        }}
        '''
    }

    res2 = requests.post(GRAPHQL_URL, headers=headers, json=query_2)
    print("[XRAY] Step 2 Response:", res2.text)

    try:
        return [r["id"] for r in res2.json()["data"]["getTestExecution"]["testRuns"]["results"]]
    except Exception as e:
        print("Could not extract test run IDs:", e)
        return []

# === Reset each test status to TODO ===
def reset_statuses_to_todo(test_run_ids, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    for run_id in test_run_ids:
        mutation = {
            "query": f'''
            mutation {{
              updateTestRunStatus(id: "{run_id}", status: "TODO")
            }}
            '''
        }

        res = requests.post(GRAPHQL_URL, headers=headers, json=mutation)
        if res.status_code == 200:
            print(f"[XRAY] Reset test run {run_id} to TODO")
        else:
            print(f"[XRAY] Failed to reset test run {run_id} - {res.status_code}: {res.text}")

# === MAIN ===
if __name__ == "__main__":
    print(f"[XRAY] Starting status reset for test execution: {TEST_EXECUTION_KEY}")
    token = get_access_token()
    if not token:
        exit(1)

    test_ids = get_test_run_ids(TEST_EXECUTION_KEY, token)
    if not test_ids:
        print("[XRAY] No test run IDs found.")
        exit(1)

    reset_statuses_to_todo(test_ids, token)
