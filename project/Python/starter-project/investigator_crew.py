from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
from crewai.tools import tool
from rpt_client import RPT1Client
from grounding_tool import mock_grounding_service
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


@tool("call_grounding_service")
def call_grounding_service(user_question: str) -> str:
    """Function to call the grounding service and retrieve relevant information based on the user's question."""
    """retrieval_client = RetrievalAPIClient()

    search_filter = RetrievalSearchFilter(
        id="vector",
        dataRepositoryType=DataRepositoryType.VECTOR.value,
        dataRepositories=["8b852a13-013b-4578-977c-dced211bd612"], #piprline s3 grounding codejam
        searchConfiguration={
            "maxChunkCount": 2
        },
    )

    search_input = RetrievalSearchInput(
        query=user_question,
        filters=[search_filter],
    )

    response = retrieval_client.search(search_input)

    response_dict = json.dumps(response.model_dump(), indent=2)"""
    response_dict = mock_grounding_service(user_question)
    return response_dict


@CrewBase
class InvestigatorCrew():
    """MurderMystery crew"""

    agents_config = "config/agents.yaml"
    tasks_config = 'config/tasks.yaml'

    @agent
    def appraiser_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['appraiser_agent'], 
            tools=[call_rpt1],
            #verbose=True
        )
    
    @agent
    def evidence_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['evidence_analyst_agent'], 
            tools=[call_grounding_service],
            #verbose=True
        )
    
    @agent
    def lead_detective_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_detective_agent'], 
            allow_delegation=True,
            #verbose=True
        )

    @task
    def appraise_loss_task(self) -> Task:
        return Task(
            config=self.tasks_config['appraise_loss_task'] # type: ignore[index]
        )
    
    @task
    def analyze_evidence_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_evidence_task'] # type: ignore[index]
        )
    
    @task
    def solve_crime(self) -> Task:
        return Task(
            config=self.tasks_config['solve_crime'], # type: ignore[index]
            context=[self.appraise_loss_task(), self.analyze_evidence_task()]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # Automatically collected by the @agent decorator
            tasks=self.tasks,    # Automatically collected by the @task decorator.
            process=Process.sequential,
            #manager_agent=self.lead_detective_agent(),
            verbose=True
        )