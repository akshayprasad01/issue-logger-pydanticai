from dotenv import load_dotenv
load_dotenv()
import asyncio
import os
from app.run_agent.run_agent import test_agent
from app.jira_operations.jira_ops import JiraOperations

def log_issue(issue: str, force_create: bool = False):
    try:
        result = asyncio.run(test_agent(issue = issue))
        jira_ops = JiraOperations()
        description = str(issue) + '\n'
        description += f'''
The given issue is classified under {result.classification}

Priority : {result.priority} \n
Risk Level : {result.risk_level}/10

Kindly work on the issue and provide a resolution.
'''
        jira_result = jira_ops.log_or_find_issue(
            summary=result.summary,
            description=description,
            priority = result.priority,
            force_override=force_create
        )

        return_result = f"""
Issue related Summary:
Classifiied as : {result.classification}
Summary: {result.summary}
Sentiment: {result.sentiment}
Priority: {result.priority}

{jira_result}
"""
        return return_result
    except Exception as e:
        return str(e)

# print(log_issue(issue = "MARC is picking up data from old cache instead of picking from user utterance."))
# print(log_issue(issue = "MARC is overlapping two users query when testing concurrently. It has picked up my pattern picked up other users input.."))
# print(log_issue(issue = "Marc is giving overlapping results when 2 users are testing together.."))
# print(log_issue(issue = "I am getting overlapping results while testing with other users."))

# result = asyncio.run(test_agent(issue = "MARC is picking up dated from old cache instead of picking from user utterance."))
# print(result)