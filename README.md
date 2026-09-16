# Virgin Mobile UAE — Selenium Website UI Automation

A portfolio edition of the Python and Selenium website-testing suite I built during my Virgin Mobile UAE internship. It automates page-by-page checks across 21 customer journeys covering mobile plans, devices, tourist plans, and home internet. The suite validates navigation and expected page content, records load timing and failure evidence, and can report results to Jira Xray.

## My contribution

- Built and implemented the Python/Selenium automation suite for checking Virgin Mobile UAE's website pages and customer flows.
- Organized reusable page selectors and test journeys, with shared checks for expected headings, page transitions, and load timing.
- Added CSV result reporting and screenshot evidence for failed checkpoints.
- Integrated Jira Xray result updates, comments, and evidence uploads.

The public portfolio copy uses environment-based configuration instead of the company's live target and private integration values. It demonstrates the implementation without automatically running tests against Virgin Mobile's production website.

## What this project demonstrates

- 21 automated customer journeys organized by product flow and test-case ID.
- Reusable page selectors separated from test orchestration.
- A shared validation checkpoint for browser actions, exact heading checks, and load timing.
- CSV result summaries with screenshots attached to failed checkpoints.
- Jira Xray status, comments, and evidence uploads.
- Environment-based configuration with no credentials or live target URL stored in source control.

## Where the checking happens

`base.py` is the central execution and validation layer. Its `SafeStep()` function optionally clicks a UI element, waits for the destination heading, compares the visible text with the expected text supplied by the test, and records the checkpoint as pass or fail. `fail_and_exit()` handles screenshots, reporting, browser cleanup, and termination when a checkpoint fails.

The files under `Test_Cases/` define the customer journeys and expected text. The files under `pages/` contain the page-specific XPath selectors. `csv_handler.py` creates local evidence, while `xray_uploader.py` sends the matching result and attachments to Jira Xray.

## Project flow

1. A test case launches Chrome and registers its report name with `base.py`.
2. The test calls `SafeStep()` for each customer-facing checkpoint.
3. Each checkpoint optionally performs a click and validates the next page heading.
4. Results and load times are written to CSV; failures also capture screenshots.
5. The final status, comment, CSV, and screenshots are sent to the matching Xray test run.

## Configuration

Private integration values are intentionally excluded from this repository. To use Xray and Jira reporting, provide `XRAY_CLIENT_ID`, `XRAY_CLIENT_SECRET`, `XRAY_TEST_MAPPING_JSON`, `JIRA_DOMAIN`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, and `TEST_EXECUTION_KEY` through the process environment or protected CI/CD variables.

Tests also require an authorized non-production `BASE_URL` and `TEST_ACCOUNT_PASSWORD`. Automated CI execution is intentionally omitted from this public copy so cloning the repository cannot trigger customer or ordering flows. `.env.example` lists every required name without storing private values.

## Repository note

This public copy was created with fresh Git history so credentials, internal Jira mappings, private runner details, and working artifacts from the original development repository are not included. Run the suite only against an environment you own or are explicitly authorized to test.
