from jira_agent import JiraAgent

def main():
    # Get project key from user
    project_key = input("Enter your Jira project key: ")
    
    # Initialize the Jira agent with project key
    agent = JiraAgent(project_key=project_key)
    
    # Create a new issue with a detailed description
    issue_key = agent.create_issue(
        summary="Test Issue with Long Description",
        description="""This is a test issue created by the Jira agent. 
        It contains a detailed description that will be summarized using Amazon Bedrock.
        
        The issue describes a new feature request for the application:
        1. User authentication system needs to be updated
        2. New password requirements should be implemented
        3. Two-factor authentication should be added
        4. Session management needs improvement
        
        Additional considerations:
        - Security audit required
        - User training materials needed
        - Documentation updates required
        - Testing plan to be developed""",
        issue_type="Task"
    )
    print(f"Created issue: {issue_key}")
    
    # Get a summary of the issue description
    summary = agent.summarize_description(issue_key)
    print("\nSummary of the issue description:")
    print(summary)
    
    # Add the summary as a comment
    agent.add_comment(issue_key, f"AI-Generated Summary:\n\n{summary}")
    print(f"\nAdded summary as a comment to issue: {issue_key}")
    
    # Get issue details
    issue_details = agent.get_issue(issue_key)
    print("\nIssue details:", issue_details)

if __name__ == "__main__":
    main() 