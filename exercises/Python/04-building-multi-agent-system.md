# Building a multi-agent system

## Structure the Agent Code
Now that you know how to build a simple AI agent with LiteLLM, CrewAI and Generative AI Hub, let's work on making the code prettier and easier to understand. CrewAI recommends to keep the AI agent definition in a separate YAML file. CrewAI: "Using YAML configuration provides a cleaner, more maintainable way to define agents. We strongly recommend using this approach in your CrewAI projects." 

👉 Create a new file [`/project/Python/starter-project/config/agents.yaml`](/project/Python/starter-project/config/agents.yaml)

👉 Create a new file [`/project/Python/starter-project/config/tasks.yaml`](/project/Python/starter-project/config/tasks.yaml)

👉 Create a new file [`/project/Python/starter-project/config/crew_config.yaml`](/project/Python/starter-project/config/crew_config.yaml)

👉 Create another new file [`/project/Python/starter-project/investigator_crew.py`](/project/Python/starter-project/investigator_crew.py)


### Move configurations to YAML files
First we will transfer the agent configuration from [`/project/Python/starter-project/agent.py`](/project/Python/starter-project/agent.py) to the YAML file.

👉 Copy the following structure into [`/project/Python/starter-project/config/agents.yaml`](/project/Python/starter-project/config/agents.yaml) and fill it with the values from your agent built in [`exercises/Python/02-build-a-basic-agent.md`](02-build-a-basic-agent.md).

```yaml
# agents.yaml
appraiser_agent:
  role: >
    Loss Appraiser
  goal: >
    Predict...
  backstory: >
    You are...
  llm: sap/gpt-4o
```

👉 Do the same for the tasks.

```yaml
# task.yaml
inspection_task:
  description: >
    Analyze...
  expected_output: >
    JSON...
  agent: ???
```

👉 Do the same for the crew itself.

```yaml
# crew_config.yaml
agents:
  - theft_crime_scene_agent

tasks:
  - inspection_task

verbose: true
```

### Move code to crew.py file

Now we will move the crew to their own file as well. It will make the code more readible and easier to maintain, especially with multiple agents working together.

👉 Navigate to [`/project/Python/starter-project/investigator_crew.py`](/project/Python/starter-project/investigator_crew.py).

👉 Paste the code snippets below step by step.

#### Step 1:
Import all encessary packages.

```python
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
from crewai.tools import tool
from dotenv import load_dotenv
from rpt_client import RPT1Client
```

#### Step 1:
Import all encessary packages.

```python
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
from crewai.tools import tool
from dotenv import load_dotenv
from rpt_client import RPT1Client
```
#### Step 2:
Load environment and create the SAP-RPT-1 tool.

```python
rpt1_client = RPT1Client()

@tool("call_rpt1")
def call_rpt1(payload: dict) -> str:
    """Function to call RPT-1 model via RPT1Client"""
    response = rpt1_client.post_request(json_payload=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"

```
#### Step 3:
Build the crew itself.

```python
@CrewBase
class MurderMystery():
    """MurderMystery crew"""

    agents_config = "config/agents.yaml"
    tasks_config = 'config/tasks.yaml'

    @agent
    def appraiser_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['####'], # TODO fill with relevant agent
            verbose=True,
            tools=[call_rpt1]
        )

    @task
    def appraise_loss_task(self) -> Task:
        return Task(
            config=self.tasks_config['####'] # TODO fill with relevant task
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # Automatically collected by the @agent decorator
            tasks=self.tasks,    # Automatically collected by the @task decorator.
            process=Process.sequential,
            verbose=True,
        )
```

### Run crew from main.py

👉 Create a new file [`/project/Python/starter-project/main.py`](/project/Python/starter-project/main.py)

```python

```





# More information
https://docs.crewai.com/en/guides/agents/crafting-effective-agents