# Use your AI Agents to solve the crime

The only thing missing now is your **Lead Detective Agent**. This agent will then use the information retrieved from the other two agents to solve the crime and determine the value of the stolen items.

## Build Your Lead Detective Agent

### Step 1: Add the Agent Configuration

👉 Navigate to [`/project/Python/starter-project/config/agents.yaml`](/project/Python/starter-project/config/agents.yaml)

👉 Add the configuration for the **Lead Detective Agent** below your other agent.

```yaml
lead_detective_agent:
  role: >
    Lead Detective Agent
  goal: >
    Solve the crime by determining which of the three suspects stole the painting.
  backstory: >
    You are a lead detective, solving burglaries.
  llm: sap/gpt-4o
```

### Step 2: Add Tasks for your Agent

👉 Navigate to [`/project/Python/starter-project/config/tasks.yaml`](/project/Python/starter-project/config/tasks.yaml)

👉 Add the configuration for the **solve crime** for your new **Lead Detective Agent**.

```yaml
solve_crime:
  description: >
    Find the thief from, the suspects by activating the evidence investigator agent and instructing him to look for the three suspects
    using the grounding tool. He should find information on alibies and motives and return a report for you to analyze.
  expected_output: >
    The name of the thief.
  agent: lead_detective_agent


determine_insurance_loss:
  description: >
    Ask the loss appraiser agent to determine the missing values using the rpt-1 tool and then return the value of the painting.
  expected_output: >
    The value of the stolen painting.
  agent: lead_detective_agent

```

### Step 3: Add the Agent to the Crew

👉 Add this code to your [project/Python/starter-project/investigator_crew.py](project/Python/starter-project/investigator_crew.py)

```python
@task
def solve_crime(self) -> Task:
    return Task(
        config=self.tasks_config['solve_crime'] # type: ignore[index]
    )

@task
def determine_insurance_loss(self) -> Task:
    return Task(
        config=self.tasks_config['determine_insurance_loss'] # type: ignore[index]
    )

@agent
def lead_detective_agent(self) -> Agent:
    return Agent(
        config=self.agents_config['lead_detective_agent'], 
        verbose=True
    )
```



### Step 4: Edit Your Detective's Agent Prompt


## Solve the Crime

👉 Run your crew!

👉 Call for the instructor and tell them your suspect.

👉 Is it correct? If yes: Congratulations!, if not: Update your prompt and try again.

