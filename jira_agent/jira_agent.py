import os
from typing import Dict, Optional
from jira import JIRA
from dotenv import load_dotenv
import boto3
import json

class JiraAgent:
    def __init__(self, project_key: Optional[str] = None):
        """
        Initialize the Jira agent
        
        Args:
            project_key: Optional project key. If not provided, it will be required in each method call.
        """
        load_dotenv()
        self.jira = JIRA(
            server=os.getenv('JIRA_URL'),
            basic_auth=(
                os.getenv('JIRA_EMAIL'),
                os.getenv('JIRA_API_TOKEN')
            )
        )
        self.project_key = project_key
        
        # Initialize Bedrock client
        self.bedrock = boto3.client(
            service_name='bedrock-runtime',
            region_name=os.getenv('AWS_REGION', 'us-east-1'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )

    def create_issue(self, summary: str, description: str, issue_type: str = 'Task', project_key: Optional[str] = None) -> str:
        """
        Create a new Jira issue
        
        Args:
            summary: The summary/title of the issue
            description: The description of the issue
            issue_type: The type of issue (Task, Bug, Story, etc.)
            project_key: Optional project key. If not provided, uses the one from constructor.
            
        Returns:
            The key of the created issue
        """
        project_key = project_key or self.project_key
        if not project_key:
            raise ValueError("Project key must be provided either in constructor or method call")

        issue_dict = {
            'project': project_key,
            'summary': summary,
            'description': description,
            'issuetype': {'name': issue_type},
        }
        
        new_issue = self.jira.create_issue(fields=issue_dict)
        return new_issue.key

    def update_issue(self, issue_key: str, fields: Dict) -> None:
        """
        Update an existing Jira issue
        
        Args:
            issue_key: The key of the issue to update
            fields: Dictionary of fields to update
        """
        issue = self.jira.issue(issue_key)
        issue.update(fields=fields)

    def add_comment(self, issue_key: str, comment: str) -> None:
        """
        Add a comment to an existing Jira issue
        
        Args:
            issue_key: The key of the issue
            comment: The comment text to add
        """
        issue = self.jira.issue(issue_key)
        self.jira.add_comment(issue, comment)

    def get_issue(self, issue_key: str) -> Dict:
        """
        Get the details of a Jira issue
        
        Args:
            issue_key: The key of the issue
            
        Returns:
            Dictionary containing issue details
        """
        issue = self.jira.issue(issue_key)
        return {
            'key': issue.key,
            'summary': issue.fields.summary,
            'description': issue.fields.description,
            'status': issue.fields.status.name,
            'created': issue.fields.created,
            'updated': issue.fields.updated
        }
        
    def summarize_description(self, issue_key: str) -> str:
        """
        Summarize the description of a Jira issue using Amazon Bedrock
        
        Args:
            issue_key: The key of the issue to summarize
            
        Returns:
            A summary of the issue description
        """
        issue = self.jira.issue(issue_key)
        description = issue.fields.description or ""
        
        if not description:
            return "No description available to summarize."
            
        prompt = f"""Please provide a concise summary of the following Jira issue description:

{description}

Summary:"""
            
        try:
            response = self.bedrock.invoke_model(
                modelId='anthropic.claude-3-sonnet-20240229-v1:0',
                body=json.dumps({
                    "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                    "max_tokens": 500,
                    "temperature": 0.7,
                    "top_p": 0.9,
                })
            )
            
            response_body = json.loads(response['body'].read())
            summary = response_body['completion'].strip()
            
            return summary
        except Exception as e:
            return f"Error generating summary: {str(e)}" 