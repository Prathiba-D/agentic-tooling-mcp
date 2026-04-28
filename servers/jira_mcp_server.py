import json
import sys
import os
import requests

def send_response(id, result):
    response = {
        "jsonrpc": "2.0",
        "id": id,
        "result": result
    }
    print(json.dumps(response))
    sys.stdout.flush()


# the function handles the request from Cline
def handle_request(request):
    method = request.get("method")

    jira_auth = os.environ.get("JIRA_AUTH")
    base_url = os.environ.get("JIRA_BASE_URL")

    headers = {
        "Authorization": jira_auth,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # List tools
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "list_issues",
                    "description": "List Jira issues",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "jql": {"type": "string"}
                        },
                        "required": ["jql"]
                    }
                },
                {
                    "name": "create_ticket",
                    "description": "Create a Jira ticket",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "project_key": {"type": "string"},
                            "summary": {"type": "string"},
                            "description": {"type": "string"}
                        },
                        "required": ["project_key", "summary"]
                    }
                },
                {
                    "name": "transition_issue",
                    "description": "Move a Jira issue to another status",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "issue_key": {"type": "string"},
                            "transition_name": {"type": "string"}
                        },
                        "required": ["issue_key", "transition_name"]
                    }
                }
            ]
        }

    # Execute Tools
    elif method == "tools/call":
        tool = request["params"]["name"]
        args = request["params"]["arguments"]

        # ---------------------------------LIST ISSUES ----------------------------
        if tool == "list_issues":
            jql = args.get("jql")

            url = f"{base_url}/rest/api/3/search/jql"

            params = {
                "jql": jql,
                "maxResults": 10,
                "fields": "*all"
            }

            res = requests.get(url, headers=headers, params=params)

            data = res.json()

            issues = data.get("issues", [])

            output = []

            for issue in issues:
                key = issue.get("key", "")
                summary = issue.get("fields", {}).get("summary", "")

                output.append(f"{key} - {summary}")

            return {
                "content": [
                    {
                        "type": "text",
                        "text": "\n".join(output) if output else "No issues found"
                    }
                ]
            }

        # ---------------------------- CREATE TICKET ----------------------------
        elif tool == "create_ticket":
            project_key = args.get("project_key")
            summary = args.get("summary")
            description = args.get("description", "")

            url = f"{base_url}/rest/api/3/issue"

            payload = {
                "fields": {
                    "project": {"key": project_key},
                    "summary": summary,
                    "description": description,
                    "issuetype": {"name": "Task"}
                }
            }

            res = requests.post(url, headers=headers, json=payload)

            if res.status_code == 201:
                key = res.json().get("key")
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Ticket created: {key}"
                        }
                    ]
                }
            else:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Failed: {res.text}"
                        }
                    ]
                }

        # -----------------------------------TRANSITION ISSUE -----------------------------------------
        elif tool == "transition_issue":
            issue_key = args.get("issue_key")
            transition_name = args.get("transition_name")

            # Step 1: Get available transitions
            transition_url = f"{base_url}/rest/api/3/issue/{issue_key}/transitions"

            res = requests.get(transition_url, headers=headers)

            if res.status_code != 200:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Failed to fetch transitions: {res.text}"
                        }
                    ]
                }

            transitions = res.json().get("transitions", [])

            transition_id = None

            # Find matching transition by name
            for t in transitions:
                if t.get("name", "").lower() == transition_name.lower():
                    transition_id = t.get("id")
                    break

            if not transition_id:
                available = [t.get("name") for t in transitions]
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Transition not found. Available: {available}"
                        }
                    ]
                }

            # Step 2: Perform transition
            url = f"{base_url}/rest/api/3/issue/{issue_key}/transitions"

            payload = {
                "transition": {
                    "id": transition_id
                }
            }

            res = requests.post(url, headers=headers, json=payload)

            if res.status_code == 204:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Issue {issue_key} moved to {transition_name}"
                        }
                    ]
                }
            else:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Transition failed: {res.text}"
                        }
                    ]
                }

    return {}

# Main loop  to wait for input from Cline
for line in sys.stdin:
    try:
        req = json.loads(line)
        result = handle_request(req)
        send_response(req.get("id"), result)
    except Exception as e:
        send_response(None, {"error": str(e)})
