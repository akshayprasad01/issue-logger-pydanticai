from app.pydantic_agent.agent import SupportDependencies, classification_agent
from app.issue_sentiment.sentiment_analysis import Sentiment

async def test_agent(*, issue = None):
    try:
        deps = SupportDependencies(
            issue = issue,
            sentiment = Sentiment()
        )

        result = await classification_agent.run(
            user_prompt=f"""
            Classify the given "{issue}" with respect to application development
            and give its sentiment analysis. Also determine its priorities and risk levels""",
            deps=deps
        )
        # print(result.data)
        return result.data
    except Exception as e:
        print(f"Error {e}")