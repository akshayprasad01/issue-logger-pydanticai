# Issue Logger Agent

This Agent is written to log an issue with MARC if you gface any problem.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the required libraries mentioned in the requirements.txt file.

```bash
pip install -r requirements.txt
```

## Environment Variables to setup this agent

Set all the environment variables as mentioned below. Do not change any keys. copy paste the keys as it is and assign new values accordingly. Anything not in <> should not be changed.

```bash
OPENAI_API_KEY = <Your OPENAI_API_KEY >
JIRA_API_KEY = <JIRA_API_KEY >
JIRA_URL = https://stg.jsw.ibm.com
JIRA_EMAIL = <your email id >
JIRA_PROJECT_ID = MAISSLOG1
TRANSFORMERS_CACHE = transformers_cache
```

## Entry Point to Agent

> 1. File name : main.py
> 2. Function name : log_issue()

>Parameters for function
>    1. issue: str (Write down you issue in normal words)

>Parameters for function Example
>    1. issue: MARC is not letting me onboard any of the agents. The agent onboarding seems to be broken.