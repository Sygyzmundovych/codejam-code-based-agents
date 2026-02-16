from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
from crewai.tools import tool
from rpt_client import RPT1Client
from dotenv import load_dotenv

load_dotenv()

rpt1_client = RPT1Client()

@tool("call_rpt1")
def call_rpt1(payload: dict) -> str:
    """Function to call RPT-1 model via RPT1Client"""
    response = rpt1_client.post_request(json_payload=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"

@CrewBase
class InvestigatorCrew():
    """MurderMystery crew"""

    agents_config = "config/agents.yaml"
    tasks_config = 'config/tasks.yaml'

    @agent
    def appraiser_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['appraiser_agent'], 
            verbose=True,
            tools=[call_rpt1]
        )

    @task
    def appraise_loss_task(self) -> Task:
        return Task(
            config=self.tasks_config['appraise_loss_task'] # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # Automatically collected by the @agent decorator
            tasks=self.tasks,    # Automatically collected by the @task decorator.
            process=Process.sequential,
            verbose=True,
        )