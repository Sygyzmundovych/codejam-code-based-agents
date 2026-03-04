# Build your first AI Agent

In any good burglary you need a loss appraiser who determines the insurance claims. That will be the first agent we build.

---

## Overview

In this exercise, you will build an agent with Python, LiteLLM and CrewAI. 

> **LiteLLM** is a library that provides a unified, provider-agnostic API for calling large language models (LLMs) and handling common tasks (completion, chat, streaming, multimodal inputs). It standardizes request/response handling and includes utilities that speed up integration with agent frameworks and tooling. Essentially it is a gateway between LLM providers and AI Agent frameworks.

That means you can use your Generative AI Hub credentials to build state of the art AI Agents with any of the models available through GenAI Hub and any of the AI Agent frameworks compatible with LiteLLM. This combination is extremely powerful because that means you can use LLMs hosted or managed by SAP (Mistral, Llama, Nvidia) and models from our partners such as Azure OpenAI, Amazon Bedrock (including Anthropic) and Gemini.

> **CrewAI** is a third-party open-source Python library. As the name suggests you can use it to build a crew of agents that have a set of tools available to accomplish certain tasks. CrewAI uses tasks to bridge the gap between high-level goals and concrete agent actions, assigning specific objectives and expected outputs. You will use CrewAI as the AI Agent framework for your agent. For now your agent will only be able to respond to incoming queries.

---

## Create a Basic Agent

### Step 1: Import Libraries and Load Environmental Variables

👉 Create a new file [`/project/Python/starter-project/agent.py`](/project/Python/starter-project/agent.py) (You can just click on the file link to create the file)

👉 Add the following lines of code to import the necessary packages and load the infos from your environment (.env) file:

```python
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

# Load environment variables
load_dotenv()
```

### Step 2: Building the Agent

Every agent needs to have at least a **role**, a **goal**, and a **backstory**. Important is also the parameter **llm**. Here you can specify which model provider and which LLM you want to use (syntax: **provider/llm**). We will specify sap as the LLM provider with over 30 models to pick from. LiteLLM is directing calls to the LLMs through the orchestration service of `Generative AI Hub`. That means you do not need to deploy your models on SAP AI Core. You only need the out of the box deployment of the orchestration service. This way you can easily switch between all the models available via the orchestration service.

👉 Below that add the code for your first agent

```python
# Create a Loss Appraiser Agent
appraiser_agent = Agent(
    role="Stolen Goods Loss Appraiser",
    goal=f"Predict the monetary value of stolen items ONLY by calling the call_rpt1 tool with payload {payload}. Do NOT invent or estimate values yourself. If the tool call fails, report the failure.",
    backstory="You are an insurance appraiser who relies strictly on model predictions. You never guess values.",
    llm="sap/gpt-4o",  # provider/llm - Using one of the models from SAP's model library in Generative AI Hub
    tools=[call_rpt1],
    verbose=True
)
```

### Step 3: Configuring a Task

Every CrewAI agent needs at least one task, otherwise the agent will be inactive. Necessary parameters to fill are **description**, **expected_output** and **agent**.

```python
# Create a task for the appraiser
appraise_loss_task = Task(
    description="Analyze the theft crime scene and predict the missing values of stolen items using the RPT-1 model via the call_rpt1 tool. Use this dict as input.",
    expected_output="JSON with predicted values for the stolen items.",
    agent=appraiser_agent
)
```

### Step 4: Create the Crew and Add Your Agent

Every crew needs to have at least one agent with at least one associated task. Both of which you defined above.

👉 Add your agent to a crew

```python
# Create a crew with the appraiser agent
crew = Crew(
    agents=[appraiser_agent],
    tasks=[appraise_loss_task],
    verbose=True
)

# Execute the crew
def main():
    result = crew.kickoff()
    print("\n" + "="*50)
    print("Insurance Appraiser Report:")
    print("="*50)
    print(result)

if __name__ == "__main__":
    main()
```

---

### Step 5: Run Your Agent

👉 Execute the basic agent:

```bash
python basic_agent.py
```

You should see:
- The appraiser agent thinking through the task
- A JSON with predicted prices being printed out.

---

## Understanding Your First Agent

### What Just Happened?

You created a basic agent that:

1. **Initialized** with a role, goal, and backstory
2. **Received** a task to process
3. **Returned** a structured response

### The Agent Workflow

```
Input → Agent Processing → LLM Call → Response → Output
```

---

## Key Takeaways

- **AI Agents** are autonomous systems that perceive, reason, and act
- **CrewAI** provides a structured framework with agents, tasks, and crews
- **LiteLLM** acts as a gateway between agent frameworks and LLM providers
- **Generative AI Hub on SAP AI Core** acts as a provider and powers agents with LLMs

---

## Next Steps

In the following exercises, you will:
1. ✅ Build a basic agent (this exercise)
2. 📌 [Add custom tools](03-add-your-first-tool.md) to your agents so they can access external data
3. 📌 Create a complete crew with multiple agents working together
4. 📌 Integrate the Grounding Service for better reasoning and fact-checking
5. 📌 Solve the museum art theft mystery using your fully-featured agent team

---

## Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'crewai'`
- **Solution**: Ensure you're in the correct Python environment: `source venv/bin/activate` and run `pip install crewai litellm`

**Issue**: Authentication error with SAP GenAI Hub
- **Solution**: Verify your `.env` file contains valid credentials from Exercise 01


---

## Resources

- [CrewAI GenAI Hub Examples](https://sap-contributions.github.io/litellm-agentic-examples/_notebooks/examples/crewai_litellm_lib.html)
- [CrewAI Documentation](https://docs.crewai.com/)
- [SAP Generative AI Hub](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/generative-ai-hub-in-sap-ai-core-7db524ee75e74bf8b50c167951fe34a5)
- [LiteLLM Documentation](https://docs.litellm.ai/)

[Next exercise](03-add-your-first-tool.md)