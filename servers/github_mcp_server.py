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

    # List tools
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "get_repo_info",
                    "description": "Get basic repository info",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "repo": {"type": "string"}
                        },
                        "required": ["repo"]
                    }
                },
                {
                    "name": "get_recent_commits",
                    "description": "Get last 3 commit IDs",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "repo": {"type": "string"}
                        },
                        "required": ["repo"]
                    }
                },
                {
                    "name": "create_branch",
                    "description": "Create a new branch (requires confirmation)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "repo": {"type": "string"},
                            "branch_name": {"type": "string"},
                            "base_branch": {"type": "string"},
                            "confirm": {"type": "boolean"}
                        },
                        "required": ["repo", "branch_name", "base_branch"]
                    }
                }
            ]
        }

    # Execute Tools
    elif method == "tools/call":
        tool_name = request["params"]["name"]
        args = request["params"]["arguments"]

        token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }

        # ----------------------- Tool: Repo Info ----------------------------
        if tool_name == "get_repo_info":
            repo = args.get("repo")

            url = f"https://api.github.com/repos/{repo}"
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                return {"content": [{"type": "text", "text": "Failed to fetch repo info"}]}

            data = response.json()

            result_text = (
                f"Name: {data.get('name')}\n"
                f"Description: {data.get('description')}\n"
                f"Stars: {data.get('stargazers_count')}\n"
                f"Language: {data.get('language')}"
            )

            return {"content": [{"type": "text", "text": result_text}]}

        #--------------------- Tool: Recent Commits ---------------------------
        elif tool_name == "get_recent_commits":
            repo = args.get("repo")

            url = f"https://api.github.com/repos/{repo}/commits"
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                return {"content": [{"type": "text", "text": "Failed to fetch commits"}]}

            commits = response.json()[:3]
            commit_ids = [c["sha"][:7] for c in commits]

            return {
                "content": [
                    {"type": "text", "text": f"Last 3 commits: {commit_ids}"}
                ]
            }

        # --------------------------Tool: Create Branch----------------------------------
        elif tool_name == "create_branch":
            repo = args.get("repo")
            branch_name = args.get("branch_name")
            base_branch = args.get("base_branch")
            confirm = args.get("confirm", False)

            # Safety check before branch creation
            if not confirm:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                f"You are about to create a branch '{branch_name}' "
                                f"from '{base_branch}' in repo '{repo}'.\n"
                                f"Re-run with confirm=true to proceed."
                            )
                        }
                    ]
                }

            #Step 1: Get base branch SHA
            ref_url = f"https://api.github.com/repos/{repo}/git/ref/heads/{base_branch}"
            ref_response = requests.get(ref_url, headers=headers)

            if ref_response.status_code != 200:
                return {
                    "content": [{"type": "text", "text": "Failed to fetch base branch"}]
                }

            sha = ref_response.json()["object"]["sha"]

            # Step 2: Create branch
            create_url = f"https://api.github.com/repos/{repo}/git/refs"
            data = {
                "ref": f"refs/heads/{branch_name}",
                "sha": sha
            }

            create_response = requests.post(create_url, headers=headers, json=data)

            if create_response.status_code == 201:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Branch '{branch_name}' created successfully"
                        }
                    ]
                }
            else:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Failed: {create_response.text}"
                        }
                    ]
                }

    return {}

# Main loop  to wait for input from Cline
for line in sys.stdin:
    try:
        request = json.loads(line)
        result = handle_request(request)
        send_response(request.get("id"), result)
    except Exception as e:
        send_response(None, {"error": str(e)})
