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
    Find the thief among the suspects by activating the evidence analyst agent and instructing them to look for information on each of the three suspects
    using the grounding tool. They should find information on alibis and motives and return a report for you to analyze.
  expected_output: >
    The name of the thief and the total value of the stolen goods for the insurance.
  agent: lead_detective_agent
```

### Step 3: Add the Agent to the Crew

👉 Add this code to your [project/Python/starter-project/investigator_crew.py](project/Python/starter-project/investigator_crew.py)

```python
@task
def solve_crime(self) -> Task:
    return Task(
        config=self.tasks_config['solve_crime'],
        context=[self.appraise_loss_task(), self.analyze_evidence_task()] # this line will make sure that the other to agents run their tasks beforehand and the lead detective can use the output of those tasks.
    )

@agent
def lead_detective_agent(self) -> Agent:
    return Agent(
        config=self.agents_config['lead_detective_agent'], 
        verbose=True
    )
```



### Step 4: Update the Crew Configuration

👉 Update your crew in [project/Python/starter-project/investigator_crew.py](project/Python/starter-project/investigator_crew.py) to run the tasks sequentially by adding the process line below:

```python
@crew
def crew(self) -> Crew:
    return Crew(
        agents=self.agents,  # Automatically collected by the @agent decorator
        tasks=self.tasks,    # Automatically collected by the @task decorator.
        process=Process.sequential,
        verbose=True
    )
```

👉 Ensure your `main()` function kicks off the crew with the appropriate inputs.

---

## Solve the Crime

👉 Run your crew!
```bash
python project/Python/starter-project/main.py
```

👉 Call for the instructor and tell them your suspect.

👉 Is it correct? If yes: Congratulations!, if not: Update your prompt and try again.

---

## Understanding Multi-Agent Orchestration

### What Just Happened?

You created a complete multi-agent system where:

1. **The Lead Detective Agent** orchestrates the investigation by delegating tasks
2. **The Evidence Analyst Agent** retrieves and analyzes evidence from documents
3. **The Loss Appraiser Agent** predicts financial values of stolen items
4. **Agent Communication** flows through task delegation and result aggregation
5. **Reasoning Integration** combines evidence, alibis, motives, and values to solve the crime

### The Investigation Flow

```
Lead Detective → Evidence Analysis → Grounding Search → Suspect Investigation
              ↓
         Loss Appraisal → RPT-1 Predictions → Value Determination
              ↓
         Crime Resolution → Suspect Identification → Final Report
```

### Why This Matters

Multi-agent systems are powerful because they:
- **Distribute Responsibilities** across specialized agents with distinct roles
- **Enable Collaboration** through task delegation and information sharing
- **Improve Reasoning** by combining multiple expert perspectives
- **Handle Complexity** by breaking down large problems into manageable subtasks
- **Scale Efficiently** as new agents and tools can be added without disrupting existing ones

---

## Key Takeaways

- **Multi-Agent Systems** decompose complex problems into specialized, collaborative agents
- **Task Delegation** allows agents to coordinate work and share results through the CrewAI framework
- **Tool Integration** across multiple agents (RPT-1, Grounding Service) provides comprehensive capabilities
- **Agent Prompts** must be carefully crafted to guide reasoning and ensure correct tool usage
- **Crew Orchestration** handles sequencing, communication, and result aggregation between agents
- **Iterative Refinement** of agent prompts and task descriptions improves investigation accuracy

---

## Next Steps

In the following exercises, you will:
1. ✅ Build a basic agent
2. ✅ Add custom tools to your agents so they can access external data
3. ✅ Create a complete crew with multiple agents working together
4. ✅ Integrate the Grounding Service for better reasoning and fact-checking
5. ✅ Solve the museum art theft mystery using your fully-featured agent team (this exercise)

Congratulations on completing the code jam! You've successfully built a sophisticated multi-agent AI system that can:
- Analyze evidence from documents
- Predict financial values using ML models
- Coordinate between multiple specialized agents
- Solve complex real-world problems through collaborative reasoning

---

## Troubleshooting

**Issue**: Agent is not using the Grounding Service tool
- **Solution**: Ensure the Evidence Analyst Agent has `tools=[call_grounding_service]` in its definition and the task description explicitly mentions searching for evidence

**Issue**: Lead Detective Agent doesn't delegate to other agents
- **Solution**: Verify that:
  - All agents are included in the crew: `agents=[appraiser_agent, evidence_analyst_agent, lead_detective_agent]`
  - Tasks are assigned to the correct agents
  - Task descriptions clearly indicate which agents should be consulted

**Issue**: RPT-1 tool is not returning predictions
- **Solution**: Ensure:
  - The Loss Appraiser Agent has `tools=[call_rpt1]` assigned
  - Your `.env` file contains valid RPT-1 deployment URL and credentials
  - The payload structure matches the RPT-1 API specification

**Issue**: Grounding search returns no relevant documents
- **Solution**: Check that:
  - The pipeline ID is correct
  - Documents are properly indexed in SAP AI Launchpad
  - Your search query is descriptive and targets the right evidence type
  - The `maxChunkCount` parameter is appropriate

**Issue**: Agent is hallucinating or not finding the correct suspect
- **Solution**: Refine your Lead Detective Agent's prompt to:
  - Be more specific about what evidence to look for
  - Include explicit instructions to cross-reference alibis and motives
  - Ask the agent to provide reasoning before concluding
  - Consider adjusting the task description to guide the investigation more clearly

**Issue**: CrewAI raises errors about task assignment or agent delegation
- **Solution**: Verify that:
  - All task configurations in `tasks.yaml` match task method names
  - All agent configurations in `agents.yaml` match agent method names
  - Tasks are assigned to agents using the `agent` field in the YAML
  - The crew includes all agents in the correct order

---

## Resources

- [CrewAI Multi-Agent Documentation](https://docs.crewai.com/)
- [CrewAI Task Management](https://docs.crewai.com/concepts/tasks)
- [CrewAI Crew Orchestration](https://docs.crewai.com/concepts/crews)
- [SAP-RPT-1 Playground](https://rpt.cloud.sap/)
- [SAP AI Launchpad Grounding Management](https://help.sap.com/docs/sap-ai-launchpad)
- [SAP Cloud SDK for AI (Python)](https://help.sap.com/doc/generative-ai-hub-sdk/CLOUD/en-US/_reference/README_sphynx.html)
- [CrewAI GenAI Hub Examples](https://sap-contributions.github.io/litellm-agentic-examples/_notebooks/examples/crewai_litellm_lib.html)
- [SAP Generative AI Hub](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/generative-ai-hub-in-sap-ai-core-7db524ee75e74bf8b50c167951fe34a5)
- [LiteLLM Documentation](https://docs.litellm.ai/)
