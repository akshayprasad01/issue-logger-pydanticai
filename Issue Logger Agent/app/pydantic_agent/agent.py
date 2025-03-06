from dataclasses import dataclass
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel, Field, field_validator
import pandas as pd
from app.issue_sentiment.sentiment_analysis import Sentiment

@dataclass
class SupportDependencies:
    issue: str
    sentiment : Sentiment

class OutputStructure(BaseModel):
    classification: str = Field(description="Classify the given issue with respect to application development with its subtypes.")
    summary: str = Field(description="Describe the given issue in brief.", min_length = 40)
    sentiment: str = Field(description="Classify it as a postive or negetive sentiment")
    priority: int = Field(description="Set the priority. 1 being the most prioritized task and 4 being the least prioritized task", ge=1, le=4)
    risk_level: int = Field(description="Risk of loosing revenue due to service being inoperable", ge=1, le=10)

classification_agent = Agent(
    model="openai:gpt-3.5-turbo",
    deps_type = SupportDependencies,
    result_type = OutputStructure,
    system_prompt="""
                You are a SaaS support expert. Analyse the issue faces by the user and 
                classify the issues under appropriate banners and determine its priority and risk level"""
)

@classification_agent.tool
async def getSentimentAnalysis(ctx: RunContext[SupportDependencies]) -> str:
    """Gets Sentiment Analysis for the given Issue"""
    sentiment_analysis = ctx.deps.sentiment.analyze_sentiment_bert(text = ctx.deps.issue)
    return sentiment_analysis

