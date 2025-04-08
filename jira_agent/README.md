# Jira Agent

A Python-based agent for interacting with Jira's API to create and update tickets, with AI-powered description summarization using Amazon Bedrock.

## Setup

1. Clone this repository
2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your Jira and AWS credentials:
   ```bash
   cp .env.example .env
   ```

## Configuration

Edit the `.env` file with your credentials:

### Jira Credentials
- `JIRA_URL`: Your Jira instance URL (e.g., https://your-domain.atlassian.net)
- `JIRA_EMAIL`: Your Jira account email
- `JIRA_API_TOKEN`: Your Jira API token

### AWS Credentials (for Bedrock)
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `AWS_REGION`: Your AWS region (default: us-east-1)

To get a Jira API token:
1. Log in to https://id.atlassian.com/manage/api-tokens
2. Click "Create API token"
3. Give it a name and copy the token

To get AWS credentials:
1. Create an AWS account if you don't have one
2. Create an IAM user with Bedrock access
3. Generate access keys for the IAM user

## Usage

The `JiraAgent` class provides the following methods:

- `create_issue(summary, description, issue_type, project_key)`: Create a new Jira issue
- `update_issue(issue_key, fields)`: Update an existing issue
- `add_comment(issue_key, comment)`: Add a comment to an issue
- `get_issue(issue_key)`: Get issue details
- `summarize_description(issue_key)`: Generate an AI summary of the issue description

Example usage:
```python
from jira_agent import JiraAgent

# Initialize the agent with project key
agent = JiraAgent(project_key="YOUR_PROJECT")

# Create a new issue
issue_key = agent.create_issue(
    summary="My Issue",
    description="Issue description",
    issue_type="Task"
)

# Generate a summary of the issue description
summary = agent.summarize_description(issue_key)
print(f"Summary: {summary}")

# Add the summary as a comment
agent.add_comment(issue_key, f"AI-Generated Summary:\n\n{summary}")

# Get issue details
issue_details = agent.get_issue(issue_key)
```

See `example.py` for a complete usage example. 