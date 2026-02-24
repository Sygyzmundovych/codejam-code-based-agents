# Building A Multi-Agent System

## Structure The Agent Code
Now that you know how to build a simple AI agent with LiteLLM, CrewAI and Generative AI Hub, let's work on making the code prettier and easier to understand. CrewAI recommends to keep the AI agent definition in a separate YAML file. CrewAI: "Using YAML configuration provides a cleaner, more maintainable way to define agents. We strongly recommend using this approach in your CrewAI projects." 

👉 Create a new file [`/project/Python/starter-project/config/agents.yaml`](/project/Python/starter-project/config/agents.yaml)

👉 Create a new file [`/project/Python/starter-project/config/tasks.yaml`](/project/Python/starter-project/config/tasks.yaml)

👉 Create a new file [`/project/Python/starter-project/config/crew_config.yaml`](/project/Python/starter-project/config/crew_config.yaml)

👉 Create another new file [`/project/Python/starter-project/investigator_crew.py`](/project/Python/starter-project/investigator_crew.py)


### Move Configurations to YAML Files
First we will transfer the agent configuration from [`/project/Python/starter-project/agent.py`](/project/Python/starter-project/agent.py) to the YAML file.

👉 Copy the following structure into [`/project/Python/starter-project/config/agents.yaml`](/project/Python/starter-project/config/agents.yaml) and fill it with the values from your agent built in [`02-build-a-basic-agent.md`](02-build-a-basic-agent.md).

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

### Move Code to crew.py File

Now we will move the crew to their own file as well. It will make the code more readible and easier to maintain, especially with multiple agents working together.

👉 Navigate to [`/project/Python/starter-project/investigator_crew.py`](/project/Python/starter-project/investigator_crew.py).

👉 Paste the code snippets below step by step.

#### Step 1: Import All Necessary Packages

```python
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
from crewai.tools import tool
from dotenv import load_dotenv
from rpt_client import RPT1Client
```

#### Step 2: Load Environment and Create The SAP-RPT-1 Tool

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

#### Step 3: Build The Crew Itself

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

### Step 4: Run The Crew From main.py

👉 Create a new file [`/project/Python/starter-project/main.py`](/project/Python/starter-project/main.py)

```python
from investigator_crew import InvestigatorCrew
    
def main():
    # Define the JSON payload for prediction
    payload = {
       #TODO add your payload here
    }

    result = InvestigatorCrew().crew().kickoff(inputs={'payload': payload})
    print("\n📘 Result:\n", result)


if __name__ == "__main__":
    main()
```

## Adding More Agents To The Crew

### Step 1: Adding a New Agent

We also have a lot of evidence in our evidence database. You can check the documents that are part if the evidence [here](exercises/data/documents).
To analyze the evidence and find all the information on our three suspects Sophie Dubois (the night manager who was on duty), Marcus Chen (the security technician who was recently fired) and Viktor Petrov (a shadowy figure whose name has surfaced in connection with the crime) we will now build an **Evidence Analyst Agent**. This new agent will try to find any inconsistencies in the alibis and motives of the suspects.

👉 Navigate to [`/project/Python/starter-project/config/agents.yaml`](/project/Python/starter-project/config/agents.yaml)

👉 Add the configuration for the **Evidence Analyst Agent** below your other agent.

```yaml
evidence_analyst_agent:
  role: >
    Evidence Analyst Agent
  goal: >
    Analyze the evidence of the theft that you can access via the grounding tool. Provide any insights that can help in the investigation especially
    regarding alibis. Check the evidence iteratively for all suspect names and provide an analysis for each of them.
  backstory: >
    You are an expert evidence analyser for major theft cases.
  llm: sap/gpt-4o
```

## Step 2: Add The Task For Your New Agent

👉 Navigate to [`/project/Python/starter-project/config/tasks.yaml`](/project/Python/starter-project/config/tasks.yaml)

👉 Add the configuration for the **analyze evidence task** for your new **Evidence Analyst Agent**.

```yaml
analyze_evidence_task:
  description: >
    Analyze the evidence of the theft that you can access via the grounding tool.
    Provide any insights that can help in the investigation especially regarding alibis. 
    Check the evidence iteratively for all three suspect names and provide an analysis for each of them.
  expected_output: >
    A detailed analysis of the evidence for each suspect, including any insights that can help in the investigation.
  agent: evidence_analyst_agent
```

### Step 3: Add The New Agent To The Crew

👉 Navigate to [`/project/Python/starter-project/investigator_crew.py`](/project/Python/starter-project/investigator_crew.py)

👉 Add the new agent and the new task to the crew using the code below:

```python
@agent
def evidence_analyst_agent(self) -> Agent:
    return Agent(
        config=self.agents_config['evidence_analyst_agent'], 
        verbose=True,
        tools=[call_rpt1]
    )

@task
def analyze_evidence_task(self) -> Task:
    return Task(
        config=self.tasks_config['analyze_evidence_task'] # type: ignore[index]
    )
```

👉 Run your crew to test it.

👉 Understand the output of the agents. You might realize the Evidence Analyst Agent does not yet have access to the actual evidence and is not actually using a tool yet. We will build it in the next exercise.

---

## Understanding Multi-Agent Systems

### What Just Happened?

You built a multi-agent system by:

1. **Separating Configuration** into YAML files for cleaner, more maintainable code
2. **Creating Reusable Agent Templates** with the `@agent` decorator
3. **Defining Task Assignments** with the `@task` decorator
4. **Orchestrating Multiple Agents** into a crew with sequential processing

### The Multi-Agent Workflow

```
Task 1 (Agent 1) → Task 2 (Agent 2) → Task 3 (Agent 3) → Aggregated Results
```

### Why This Architecture Matters

Multi-agent systems provide:
- **Specialization** - Each agent focuses on a specific role and task
- **Scalability** - Add new agents without modifying existing ones
- **Collaboration** - Agents can build upon each other's findings
- **Maintainability** - YAML configuration separates concerns from logic

---

## Key Takeaways

- **YAML Configuration** provides cleaner, more maintainable agent definitions
- **Decorators** (`@agent`, `@task`, `@crew`) streamline multi-agent creation in CrewAI
- **Sequential Processing** allows agents to work in order, with later agents using earlier results
- **Agent Specialization** makes systems more robust and easier to understand
- **Separation of Concerns** keeps configuration separate from implementation logic

---

## Next Steps

In the following exercises, you will:
1. ✅ Build a basic agent
2. ✅ [Add custom tools](03-add-your-first-tool.md) to your agents so they can access external data
3. ✅ Create a complete crew with multiple agents working together (this exercise)
4. 📌 Integrate the Grounding Service for better reasoning and fact-checking
5. 📌 Solve the museum art theft mystery using your fully-featured agent team

---

## Troubleshooting

**Issue**: `YAML configuration not found` or file path errors
- **Solution**: Ensure you've created all YAML files in `/project/Python/starter-project/config/` directory and verify the file paths in your Python code match exactly.

**Issue**: `Agent not found in configuration` or missing agent reference
- **Solution**: Verify that the agent name in your `agents.yaml` matches the key referenced in the `@agent` method and that the agent is added to the agents list in the crew.

**Issue**: Agents not executing in order or parallel execution
- **Solution**: Ensure you've set `process=Process.sequential` in your `@crew` method. Use `Process.hierarchical` if you need a manager agent to coordinate.

**Issue**: `ModuleNotFoundError: No module named 'crewai.project'`
- **Solution**: Ensure you're using CrewAI version 0.22.0 or higher: `pip install --upgrade crewai`

**Issue**: Tool not available to agents
- **Solution**: Verify that you're passing `tools=[call_rpt1]` to each agent that needs access to the tool in the `@agent` method.

---

## Resources

- [CrewAI Project Structure Guide](https://docs.crewai.com/en/guides/agents/crafting-effective-agents)
- [CrewAI YAML Configuration](https://docs.crewai.com/concepts/agents)
- [CrewAI Process Types](https://docs.crewai.com/concepts/processes)
- [CrewAI Decorators Documentation](https://docs.crewai.com/en/guides/agents/agent-setup)
- [CrewAI Multi-Agent Examples](https://github.com/joaomdmoura/crewai-examples)
- [CrewAI Documentation](https://docs.crewai.com/)
- [SAP Generative AI Hub](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/generative-ai-hub-in-sap-ai-core-7db524ee75e74bf8b50c167951fe34a5)