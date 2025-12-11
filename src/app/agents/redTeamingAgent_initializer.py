# Azure imports
from azure.identity import DefaultAzureCredential
from azure.ai.evaluation.red_team import RedTeam, RiskCategory, AttackStrategy
from pyrit.prompt_target import OpenAIChatTarget
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

# Azure AI Project Information
azure_ai_project = os.getenv("AZURE_AI_AGENT_ENDPOINT")

# Instantiate your AI Red Teaming Agent
red_team_agent = RedTeam(
    azure_ai_project=azure_ai_project,
    credential=DefaultAzureCredential(),
    risk_categories=[
        RiskCategory.Violence,
        RiskCategory.HateUnfairness,
        RiskCategory.Sexual,
        RiskCategory.SelfHarm
    ],
    num_objectives=5,
)

# Define the OpenAI chat target model
chat_target = OpenAIChatTarget(
    model_name=os.environ.get("gpt_deployment"),
    endpoint=f"{os.environ.get('gpt_endpoint')}/openai/deployments/{os.environ.get('gpt_deployment')}/chat/completions",
    api_key=os.environ.get("gpt_api_key"),
    api_version=os.environ.get("gpt_api_version"),
)

async def main():
    print("Starting red team scan against Azure OpenAI model...")
    red_team_result = await red_team_agent.scan(target=chat_target)
    print("Red team scan completed!")
    print(f"Results: {red_team_result}")

asyncio.run(main())
