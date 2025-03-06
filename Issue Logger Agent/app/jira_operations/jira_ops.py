import os
from rapidfuzz import fuzz
import openai
from app.connections.jira_connection import get_jira_client

class JiraOperations:
    def __init__(self):
        self.jira_client = get_jira_client()
        self.jira_url = os.getenv("JIRA_URL")
        self.project_key = os.getenv("JIRA_PROJECT_ID")

    def get_llm_similarity(self, summary1, summary2):
        """
        Uses OpenAI's LLM to determine if two issue summaries are similar.
        """
        prompt = f"""
        Compare the similarity between these two Jira issue summaries:

        1. "{summary1}"
        2. "{summary2}"

        If they describe the same or highly related issue, return "YES".
        Otherwise, return "NO".
        """

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an AI that compares Jira issues."},
                    {"role": "user", "content": prompt}],
            temperature=0  # Reduce randomness for consistency
        )

        return "YES" in response.choices[0].message.content

    def search_open_issues(self, project_key):
        """
        Fetches open issues from Jira (excluding closed ones).
        """
        JQL_QUERY = f'project = {project_key} AND statusCategory != Done ORDER BY created DESC'
        # Pagination to get all issues
        start_at = 0
        max_results = 50  # Maximum allowed value by Jira
        open_issues = []

        while True:
            issues = self.jira_client.search_issues(JQL_QUERY, startAt=start_at, maxResults=max_results)
            
            if not issues:
                break  # Stop if no more issues are found

            open_issues.extend(issues)
            start_at += max_results
        # open_issues = jira.search_issues(JQL_QUERY, maxResults=20)  # Get top 20 open issues
        return open_issues
    
    def find_similar_issues(self, open_issues, new_summary, threshold=40):
        """
        Uses fuzzy matching to find similar issues in Jira.
        """
        similar_issues = []
        new_summary = new_summary.lower().strip()

        for issue in open_issues:
            issue_summary = issue.fields.summary.lower().strip()
            
            similarity = self.get_llm_similarity(new_summary, issue_summary)
            if similarity:
                similar_issues.append(issue)

        # for issue in open_issues:
        #     issue_summary = issue.fields.summary.lower().strip()

        #     # Calculate similarity
        #     similarity_score = fuzz.ratio(new_summary, issue_summary)

        #     if similarity_score >= threshold:  # If match is strong, add to results
        #         similar_issues.append((issue, similarity_score))

        # # Sort issues by highest similarity
        # similar_issues.sort(key=lambda x: x[1], reverse=True)

        return similar_issues
    
    def create_jira_issue(self, project_key, summary, description, priority ,issue_type="Bug"):
        """
        Creates a new Jira issue.
        """
        priority_cache = {
            1 : "Highest",
            2 : "High",
            3 : "Medium",
            4 : "Low",
            5 : "Lowest"
        }

        new_issue = {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type},
            "priority": {"name": priority_cache[priority]},
        }
        
        issue = self.jira_client.create_issue(fields=new_issue)
        return issue
    
    def log_or_find_issue(self, summary, description, priority, force_override = False):
        """
        Logs a new issue if no similar open issues exist. Otherwise, returns existing open issues.
        """
        if not force_override:
            open_issues = self.search_open_issues(self.project_key)
            similar_issues = self.find_similar_issues(open_issues, summary)
            return_str = ''
            if similar_issues:
                return_str += "⚠️ Similar **open** issues found:\n"
                for issue in similar_issues:
                    # return_str += f"- {issue.key}: {issue.fields.summary} (Status: {issue.fields.status.name}, Similarity: {score}%)\n" 
                    return_str += f"- {issue.key}: {issue.fields.summary} (Status: {issue.fields.status.name})\n"
                return return_str + "Please check the above open issues before proceeding."

            # No similar open issue found, log a new one
            issue = self.create_jira_issue(self.project_key, summary, description, priority)
            issue_link = f"{self.jira_url}/browse/{issue.key}"
            
            return f"✅ Your issue has been logged: {issue_link}"
        else:
            issue = self.create_jira_issue(self.project_key, summary, description, priority)
            issue_link = f"{self.jira_url}/browse/{issue.key}"
            
            return f"✅ Your issue has been logged: {issue_link}"