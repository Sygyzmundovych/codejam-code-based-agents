# Add Your First Tool to the Agent

You might have realized that, while the agent prompt mentions a tool call to the SAP-RPT-1 model, there is no actual tool call happening. There is also no input to actually run a prediction on. The response of the agent is totally made up.

---

## Overview

In this exercise, you will add an input variable and a tool to your agent. You will give the agent the SAP-RPT-1 model as a tool to make predictions on structured data.

> **SAP-RPT-1** [SAP's Relational Pretrained Transformer model](https://www.sap.com/products/artificial-intelligence/sap-rpt.html) is a foundation model trained on structured data. It is available in the Generative AI Hub to gain predictive insights from enterprise data without building models from scratch. The model works by uploading a couple of example data rows as .json or .csv files and can do classification as well as regression predictions on your dataset.

---

## Check out SAP-RPT-1

👉 Open the [SAP-RPT-1 Playground](https://rpt.cloud.sap/). Use one of the example files from the playground to understand how the model works.

---

## Add an Input Variable to Your Agent

### Step 1: Add an Input Variable to the Agent Prompt

In order for the agent to run predictions on actual data, you need to be able to pass input data.

👉 Add the variable payload to the goal of the agent and to the description of the task by adding {payload} to the string and converting the string to an **f-string** (formatted string) by adding `f` to the beginning of the string.

Your agent and task definition should now look like this:

```python
# Create a Loss Appraiser Agent
appraiser_agent = Agent(
    role="Loss Appraiser",
    goal=f"Predict the missing values of stolen items using the RPT-1 model via the call_rpt1 tool use this payload {payload} as input.",
    backstory="You are an expert insurance appraiser specializing in fine art valuation and theft assessment.",
    llm="sap/gpt-4o",  # provider/llm - Using one of the models from SAP's model library in Generative AI Hub
    verbose=True
)

# Create a task for the appraiser
appraise_loss_task = Task(
    description=f"Analyze the theft crime scene and predict the missing values of stolen items using the RPT-1 model via the call_rpt1 tool. Use this dict {payload} as input.",
    expected_output="JSON with predicted values for the stolen items.",
    agent=appraiser_agent
)
```

---

### Step 2: Define Input

👉 Assign your input to the variable payload

```python
# define payload
payload = {
        "prediction_config": {
            "target_columns": [
                {
                    "name": "COSTCENTER",
                    "prediction_placeholder": "'[PREDICT]'",
                    "task_type": "classification",
                },
                {
                    "name": "PRICE",
                    "prediction_placeholder": "'[PREDICT]'",
                    "task_type": "regression",
                },
            ]
        },
        "index_column": "ID",
        "rows": [
            {
                "PRODUCT": "Couch",
                "PRICE": "'[PREDICT]'",
                "ORDERDATE": "28-11-2025",
                "ID": "35",
                "COSTCENTER": "'[PREDICT]'",
            },
            {
                "PRODUCT": "Office Chair",
                "PRICE": 150.8,
                "ORDERDATE": "02-11-2025",
                "ID": "44",
                "COSTCENTER": "Office Furniture",
            },
            {
                "PRODUCT": "Server Rack",
                "PRICE": 210.0,
                "ORDERDATE": "01-11-2025",
                "ID": "108",
                "COSTCENTER": "Data Infrastructure",
            },
            {
                "PRODUCT": "Server Rack",
                "PRICE": "'[PREDICT]'",
                "ORDERDATE": "01-11-2025",
                "ID": "104",
                "COSTCENTER": "'[PREDICT]'",
            },
        ],
        "data_schema": {
            "PRODUCT": {"dtype": "string"},
            "PRICE": {"dtype": "numeric"},
            "ORDERDATE": {"dtype": "date"},
            "ID": {"dtype": "string"},
            "COSTCENTER": {"dtype": "string"},
        },
    }

```


---

### Step 3: Run the Crew with Input Variables

👉 Pass your input to the crew

```python
# Create a crew with the appraiser agent
crew = Crew(
    agents=[appraiser_agent],
    tasks=[appraise_loss_task],
    verbose=True
)

# Execute the crew
def main():
    result = crew.kickoff(inputs={'payload': payload})
    print("\n" + "="*50)
    print("Insurance Appraiser Report:")
    print("="*50)
    print(result)

if __name__ == "__main__":
    main()
```

👉 Run your crew to test it.

---

## Add SAP-RPT-1 to Your Agent

### Step 0: Build the SAP-RPT-1 Client

SAP-RPT-1 will be added to the Cloud SDK for AI but for now we will build our own client.

👉 Create a new file [`/project/Python/starter-project/rpt_client.py`](/project/Python/starter-project/rpt_client.py)

👉 Add the code below:

```python
import os
import requests

class RPT1Client:
    def __init__(self):
        # Read env vars (assume dotenv already loaded in main)
        self.client_id = os.getenv("AICORE_CLIENT_ID")
        self.client_secret = os.getenv("AICORE_CLIENT_SECRET")
        self.auth_url = os.getenv("AICORE_AUTH_URL")
        self.deployment_url = os.getenv("RPT1_DEPLOYMENT_URL")
        self.token = self._fetch_token()
        self.resource_group = os.getenv("AICORE_RESOURCE_GROUP", "default")

    # Function to fetch OAuth token
    def _fetch_token(auth_url: str | None = None, client_id: str | None = None, client_secret: str | None = None, timeout: int = 30) -> dict:
        auth_url = os.getenv("AICORE_AUTH_URL")
        if not auth_url:
            raise ValueError("AICORE_AUTH_URL must be provided (env or arg).")
        client_id = os.getenv("AICORE_CLIENT_ID")
        if not client_id:
            raise ValueError("AICORE_CLIENT_ID must be provided (env or arg).")
        client_secret = os.getenv("AICORE_CLIENT_SECRET")
        if not client_secret:
            raise ValueError("AICORE_CLIENT_SECRET must be provided (env or arg).")
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        resp = requests.post(auth_url, data=data, headers=headers, timeout=timeout)
        resp.raise_for_status()
        token = resp.json()
        access_token = token["access_token"]
        return access_token

    def post_request(self, json_payload: dict, timeout: int = 60):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "AI-Resource-Group": self.resource_group
        }

        # Send the POST request to the deployment URL
        response = requests.post(
            self.deployment_url, json=json_payload, headers=headers
        )
        return response

```

### Step 1: Build the Function for the Tool

To add a custom tool to an agent, you create a function that encapsulates the functionality you want to expose. This function will be available for the agent to call when completing its task.

👉 Import the SAP-RPT-1 client at the top of your `agent.py` file and initialize the client by adding the code below:

```python
from rpt_client import RPT1Client

rpt1_client = RPT1Client()
```

👉 Add this code above your agent definition:

```python
def call_rpt1(payload: dict) -> str:
    """Function to call RPT-1 model via RPT1Client"""
    response = rpt1_client.post_request(json_payload=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"
```

### Step 2: Make the Function a Tool

👉 Add this `from crewai.tools import tool` to your import at the top of your `agent.py` file.

👉 Add this line `@tool("call_rpt1")` above your `call_rpt1()` function. 

```python
@tool("call_rpt1")
def call_rpt1(payload: dict) -> str:
    """Function to call RPT-1 model via RPT1Client"""
    response = rpt1_client.post_request(json_payload=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"
```

### Step 3: Add the Tool to Your Agent

👉 Add this line `tools=[call_rpt1],` to your agent definition.

```python
# Create a Loss Appraiser Agent
appraiser_agent = Agent(
    role="Loss Appraiser",
    goal=f"Predict the missing values of stolen items using the RPT-1 model via the call_rpt1 tool use this payload {payload} as input.",
    backstory="You are an expert insurance appraiser specializing in fine art valuation and theft assessment.",
    llm="sap/gpt-4o",  # provider/llm - Using one of the models from SAP's model library in Generative AI Hub
    tools=[call_rpt1],
    verbose=True
)
```

👉 Your code in `agent.py` should now look like this: 

```python
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai.tools import tool
from rpt_client import RPT1Client

# Load environment variables
load_dotenv()

rpt1_client = RPT1Client()

# define payload
payload = {
        "prediction_config": {
            "target_columns": [
                {
                    "name": "COSTCENTER",
                    "prediction_placeholder": "'[PREDICT]'",
                    "task_type": "classification",
                },
                {
                    "name": "PRICE",
                    "prediction_placeholder": "'[PREDICT]'",
                    "task_type": "regression",
                },
            ]
        },
        "index_column": "ID",
        "rows": [
            {
                "PRODUCT": "Couch",
                "PRICE": "'[PREDICT]'",
                "ORDERDATE": "28-11-2025",
                "ID": "35",
                "COSTCENTER": "'[PREDICT]'",
            },
            {
                "PRODUCT": "Office Chair",
                "PRICE": 150.8,
                "ORDERDATE": "02-11-2025",
                "ID": "44",
                "COSTCENTER": "Office Furniture",
            },
            {
                "PRODUCT": "Server Rack",
                "PRICE": 210.0,
                "ORDERDATE": "01-11-2025",
                "ID": "108",
                "COSTCENTER": "Data Infrastructure",
            },
            {
                "PRODUCT": "Server Rack",
                "PRICE": "'[PREDICT]'",
                "ORDERDATE": "01-11-2025",
                "ID": "104",
                "COSTCENTER": "'[PREDICT]'",
            },
        ],
        "data_schema": {
            "PRODUCT": {"dtype": "string"},
            "PRICE": {"dtype": "numeric"},
            "ORDERDATE": {"dtype": "date"},
            "ID": {"dtype": "string"},
            "COSTCENTER": {"dtype": "string"},
        },
    }

@tool("call_rpt1")
def call_rpt1(payload: dict) -> str:
    """Function to call RPT-1 model via RPT1Client"""
    response = rpt1_client.post_request(json_payload=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"

# Create a Loss Appraiser Agent
appraiser_agent = Agent(
    role="Loss Appraiser",
    goal=f"Predict the missing values of stolen items using the RPT-1 model via the call_rpt1 tool use this payload {payload} as input.",
    backstory="You are an expert insurance appraiser specializing in fine art valuation and theft assessment.",
    llm="sap/gpt-4o",  # provider/llm - Using one of the models from SAP's model library in Generative AI Hub
    tools=[call_rpt1],
    verbose=True
)

# Create a task for the appraiser
appraise_loss_task = Task(
    description=f"Analyze the theft crime scene and predict the missing values of stolen items using the RPT-1 model via the call_rpt1 tool. Use this dict {payload} as input.",
    expected_output="JSON with predicted values for the stolen items.",
    agent=appraiser_agent
)

# Create a crew with the appraiser agent
crew = Crew(
    agents=[appraiser_agent],
    tasks=[appraise_loss_task],
    verbose=True
)

# Execute the crew
def main():
    result = crew.kickoff(inputs={'payload': payload})
    print("\n" + "="*50)
    print("Insurance Appraiser Report:")
    print("="*50)
    print(result)

if __name__ == "__main__":
    main()
```

👉 Run your crew to test it.

👉 Understand the output of the agent using SAP-RPT-1 as a tool.

> SAP-RPT-1 not only predicts missing values with the [PREDICT] placeholder but also returns a confidence score for classification tasks, indicating how confident the model is in its predictions.


---

## Understanding Tools in CrewAI

### What Just Happened?

You extended your agent with:

1. **A custom tool function** decorated with `@tool()` that encapsulates external functionality
2. **Tool assignment** by passing `tools=[call_rpt1]` to the agent, making it available for use
3. **Tool invocation** in the agent's task description, allowing the LLM to decide when and how to use it

### The Tool Flow

```
Agent Task → LLM Reasoning → Tool Decision → Tool Execution → Result → Agent Processing → Output
```

### Why This Matters

Tools are essential for agents to:
- **Access External APIs** and services (like the RPT-1 model)
- **Perform Real Actions** beyond text generation
- **Provide Grounded Responses** based on actual data and computations
- **Enable Autonomous Operation** by expanding the agent's capabilities

---

## Key Takeaways

- **Tools** extend agent capabilities beyond pure reasoning—they enable actions and external integrations
- **Decorators** like `@tool()` transform functions into CrewAI-compatible tools with descriptions
- **Tool Assignment** is crucial—agents only have access to tools explicitly passed in the `tools` parameter
- **Tool Availability** should be reflected in the agent's goal and task descriptions so the LLM knows they exist
- **Custom Clients** like `RPT1Client` encapsulate API interactions, keeping tool functions clean and focused

---

## Next Steps

In the following exercises, you will:
1. ✅ Build a basic agent
2. ✅ [Add custom tools](03-add-your-first-tool.md) to your agents so they can access external data (this exercise)
3. 📌 Create a complete crew with multiple agents working together
4. 📌 Integrate the Grounding Service for better reasoning and fact-checking
5. 📌 Solve the museum art theft mystery using your fully-featured agent team

---

## Troubleshooting

**Issue**: `AttributeError: 'Agent' object has no attribute 'tools'` or tool is not being called
- **Solution**: Ensure you've added `tools=[call_rpt1]` to your Agent definition. Without this, the agent won't have access to the tool.

**Issue**: `Tool not found` or agent ignores the tool
- **Solution**: Verify that:
  - The `@tool()` decorator is above the function definition
  - The tool is assigned to the agent via `tools=[call_rpt1]`
  - Your task description mentions the tool so the LLM knows to use it

**Issue**: `ModuleNotFoundError: No module named 'rpt_client'`
- **Solution**: Ensure you've created the `rpt_client.py` file in `/project/Python/starter-project/` and that you're in the correct directory when running the script.

**Issue**: Authentication error calling RPT-1
- **Solution**: Verify your `.env` file contains valid credentials:
  - `AICORE_CLIENT_ID`
  - `AICORE_CLIENT_SECRET`
  - `AICORE_AUTH_URL`
  - `RPT1_DEPLOYMENT_URL`
  - `AICORE_RESOURCE_GROUP` (optional, defaults to "default")

**Issue**: Tool returns error `400` or `422`
- **Solution**: Verify your payload structure matches the RPT-1 API specification. Check the [SAP-RPT-1 Playground](https://rpt.cloud.sap/) for valid payload examples.

---

## Resources

- [SAP-RPT-1 Playground](https://rpt.cloud.sap/)
- [CrewAI Tools Documentation](https://docs.crewai.com/concepts/tools)
- [CrewAI GenAI Hub Examples](https://sap-contributions.github.io/litellm-agentic-examples/_notebooks/examples/crewai_litellm_lib.html)
- [CrewAI Documentation](https://docs.crewai.com/)
- [SAP Generative AI Hub](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/generative-ai-hub-in-sap-ai-core-7db524ee75e74bf8b50c167951fe34a5)
- [LiteLLM Documentation](https://docs.litellm.ai/)
