<h2>ClineAI MCP | Agentic Jira & GitHub Assistant using MCP</h2>
<h2>📌Overview</h2>
This work demonstrates an <b>Agentic workflow system</b> using MCP (Model Context Protocol) servers for Jira and GitHub automation.<br><br>
The system integrates a VS Code <b>Cline extension as the agent orchestrator</b>, which interprets natural language commands and routes them to appropriate tool servers.<br><br>
It showcases how Jira and GitHub tasks such as issue tracking (listing, creation, and status transitions) and source control operations (repository inspection, commit history retrieval, and branch creation) can be done using an agent-based architecture.

<h2>🏗️ System Architecture</h2>

<p align="center">
  <img src="mcp-execution-outputs/cline-mcp-architecture.PNG" width="800"/><br>
  <i>Agentic Automation architecture showing Cline (VS Code) orchestrating Jira and GitHub MCP servers</i>
</p>

<h2>⚙️ Jira MCP Execution</h2>

<h4>📌 List Issues</h4>
<p align="center">
  <img src="mcp-execution-outputs/jira_list_issues.PNG" width="700"/><br>
  <i>Jira issues fetched using JQL query via MCP server</i>
</p>

<h4>📌 Create Issue</h4>

<p align="center">
  <img src="mcp-execution-outputs/jira_create_issue_prompt.PNG" width="700"/><br>
  <i>User prompt for creating a Jira issue via Cline agent</i>
</p>

<p align="center">
  <img src="mcp-execution-outputs/jira_create_issue_success.PNG" width="700"/><br>
  <i>Successful issue creation response from Jira MCP server</i>
</p>

<p align="center">
  <img src="mcp-execution-outputs/jira_output_issue_created.PNG" width="700"/><br>
  <i>Final output confirming Jira ticket creation</i>
</p>

<h4>📌 Transition Issue</h4>

<p align="center">
  <img src="mcp-execution-outputs/jira_transition_issue_prompt.PNG" width="700"/><br>
  <i>Prompt to transition Jira issue status</i>
</p>

<p align="center">
  <img src="mcp-execution-outputs/jira_transition_issue_success.PNG" width="700"/><br>
  <i>Successful transition execution response</i>
</p>

<p align="center">
  <img src="mcp-execution-outputs/jira-output-transition.PNG" width="700"/><br>
  <i>Final output confirming issue status update</i>
</p>

<h2> GitHub MCP Execution</h2>

<h4>📌 Repository Information</h4>
<p align="center">
  <img src="mcp-execution-outputs/github_repo_info.PNG" width="700"/><br>
  <i>Repository metadata fetched via GitHub MCP server</i>
</p>

<h4>📌 Recent Commits</h4>

<p align="center">
  <img src="mcp-execution-outputs/github_recent_commits_cloudpulse.PNG" width="700"/><br>
  <i>Recent commits from CloudPulse repository</i>
</p>

<p align="center">
  <img src="mcp-execution-outputs/github_recent_commits_java_repo.PNG" width="700"/><br>
  <i>Recent commits from Java repository</i>
</p>

<h4>📌 Create Branch</h4>

<p align="center">
  <img src="mcp-execution-outputs/github_create_branch.PNG" width="700"/><br>
  <i>Branch creation executed via GitHub MCP server</i>
</p>

<h2>🎯 Purpose</h2>

This project explores:
<ul>
  <li>Agent-based orchestration using MCP (Model Context Protocol) servers</li>
  <li>Tool abstraction for external system APIs (Jira and GitHub)</li>
  <li>Natural language driven automation via VS Code Cline extension</li>
  <li>Integration of Jira and GitHub into a unified agent-controlled system</li>
</ul>

<h2>🚀 Key Insight</h2>

This project demonstrates how agentic systems can bridge natural language and external system APIs, enabling structured automation of Jira and GitHub operations such as issue management, repository inspection, and branch creation—without direct manual API interaction.
