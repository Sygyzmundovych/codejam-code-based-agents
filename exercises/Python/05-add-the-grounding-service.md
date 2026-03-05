# Add The Grounding Service

## Overview

In this exercise, you will add a grounding service tool to your evidence analyst agent. The grounding service retrieves relevant information from evidence documents to help the agent analyze the crime. You'll learn how to integrate external data sources with your agents using SAP AI Launchpad's grounding management system.

---

## Understand The Grounding Service

👉 Go to [SAP AI Launchpad](https://genai-codejam-luyq1wkg.ai-launchpad.prod.eu-central-1.aws.ai-prod.cloud.sap/aic/index.html#/workspaces&/a/detail/TwoColumnsMidExpanded/?workspace=api-connection&resourceGroup=s3-grounding) 

☝️ In this subaccount the connection between the SAP AI Core service instance and the SAP AI Launchpad application is already established. Otherwise you would have to add a new AI runtime using the SAP AI Core service key information.

### Select The Resource Group Code-Based-Agent-Codejam

SAP AI Core tenants use [resource groups](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/resource-groups) to isolate AI resources and workloads. Scenarios (e.g. `foundation-models`) and executables (a template for training a model or creation of a deployment) are shared across all resource groups within the instance.

>DO NOT USE THE DEFAULT `default` RESOURCE GROUP!

👉 Go to **Workspaces**.

👉 Select your workspace (like `codejam-YYY`) and your resource group `ai-agent-codejam`.

👉 Make sure it is set as a context. The proper name of the context, like `codejam-YYY (ai-agent-codejam)` should show up at the top next to SAP AI Launchpad.

👉 Go to the `Generative AI Hub > Grounding Management` tab and open the existing pipeline. 

👉 Have a look around. You can also run a search by clicking the `Run Search` button.

☝️ You will need the pipeline ID in the next step!

---

## Add The Grounding Service To Your Agent Crew

### Step 1: Build The Grounding Tool

The evidence analyst agent is still missing the grounding tool. Let's build it!

👉 To the [`/project/Python/starter-project/investigator_crew.py`](/project/Python/starter-project/investigator_crew.py) you will add the code below:

```python
@tool("call_grounding_service")
def call_grounding_service(user_question: str) -> str:
    """Function to call the grounding service and retrieve relevant information based on the user's question."""
    retrieval_client = RetrievalAPIClient()

    search_filter = RetrievalSearchFilter(
        id="vector",
        dataRepositoryType=DataRepositoryType.VECTOR.value,
        dataRepositories=["YOUR REPO ID HERE"], # pipeline ID from Grounding Management in SAP AI Launchpad
        searchConfiguration={
            "maxChunkCount": 5
        },
    )

    search_input = RetrievalSearchInput(
        query=user_question,
        filters=[search_filter],
    )

    response = retrieval_client.search(search_input)

    response_dict = json.dumps(response.model_dump(), indent=2)
    return response_dict
```

### Step 2: Get The Pipeline ID From SAP AI Launchpad

👉 Navigate back to `Workspaces` and select the resource group `ai-agents-codejam`

👉 Navigate to Grounding Management and select the pipeline ID from there.

### Step 3: Import Missing Libraries

You might realize that you are missing some libraries.

👉 First you need to install the [Cloud SDK for AI (Python)](https://help.sap.com/doc/generative-ai-hub-sdk/CLOUD/en-US/_reference/README_sphynx.html). Open the terminal in your .venv environment and run this command: 
> `pip install sap-ai-sdk-gen`

👉 You will need to add this code at the top of the file to import the necessary packages:

```python
import json

from gen_ai_hub.document_grounding.client import RetrievalAPIClient
from gen_ai_hub.document_grounding.models.retrieval import (
    RetrievalSearchInput,
    RetrievalSearchFilter,
)
from gen_ai_hub.orchestration.models.document_grounding import DataRepositoryType
```

### Step 4: Add The Tool To Your Agent

👉 Still in [`/project/Python/starter-project/investigator_crew.py`](/project/Python/starter-project/investigator_crew.py) add this line `tools=[call_grounding_service],` to your agent creation in [project/Python/starter-project/investigator_crew.py](project/Python/starter-project/investigator_crew.py).

👉 The **Criminal Evidence Analyst** should look like this now:

```python
@agent
def evidence_analyst_agent(self) -> Agent:
    return Agent(
        config=self.agents_config['evidence_analyst_agent'], 
        verbose=True,
        tools=[call_grounding_service]
    )
```

👉 Run your crew to test it.

👉 Understand the output of the agents. You might realize the Evidence Analyst Agent does not yet have access to the actual evidence and is not actually using a tool yet. We will build it in the next exercise.

---

## Understanding the Grounding Service

### What Just Happened?

You integrated a grounding service tool with your agent that:

1. **Connects** to SAP AI Launchpad's document grounding capabilities
2. **Searches** indexed evidence documents using vector similarity
3. **Retrieves** relevant chunks of information to support the agent's analysis
4. **Provides** context for the agent to make informed decisions

### The Grounding Flow

```
User Query → Agent Processing → Grounding Tool Call → Vector Search → Document Chunks → Agent Analysis → Output
```

### Why This Matters

Grounding services are essential for agents to:
- **Access External Knowledge** from documents and data repositories
- **Provide Factual Responses** grounded in actual evidence
- **Reduce Hallucinations** by tethering reasoning to real data
- **Enable Scalability** by managing large document collections efficiently

---

## Key Takeaways

- **Grounding Services** extend agents' knowledge by connecting them to external document repositories
- **Vector Search** enables semantic search across documents, finding contextually relevant information
- **Document Pipelines** in SAP AI Launchpad manage document indexing and retrieval
- **Tool Integration** is key—grounding tools must be explicitly passed to agents via the `tools` parameter
- **Repository IDs** identify which document collection to search, allowing agents to target specific data sources

---

## Next Steps

In the following exercises, you will:
1. ✅ Build a basic agent
2. ✅ Add custom tools to your agents so they can access external data
3. ✅ Create a complete crew with multiple agents working together
4. ✅ Integrate the Grounding Service for better reasoning and fact-checking (this exercise)
5. 📌 [Solve the museum art theft mystery](06-solve-the-crime.md) using your fully-featured agent team

---

## Troubleshooting

**Issue**: `AttributeError: 'module' object has no attribute 'RetrievalAPIClient'`
- **Solution**: Ensure you've installed the SAP AI SDK with `pip install sap-ai-sdk-gen` and that all imports are correct

**Issue**: `Pipeline not found` or authentication error with grounding service
- **Solution**: Verify that:
  - Your resource group is set to `ai-agent-codejam` in SAP AI Launchpad
  - The pipeline ID is correct and matches the one from Grounding Management
  - Your `.env` file contains valid SAP AI Core credentials

**Issue**: `RetrievalAPIClient` initialization fails
- **Solution**: The client uses your environment variables for authentication. Ensure your `.env` file contains:
  - `AICORE_CLIENT_ID`
  - `AICORE_CLIENT_SECRET`
  - `AICORE_AUTH_URL`
  - `AICORE_BASE_URL`

**Issue**: No results returned from grounding service
- **Solution**: Verify that:
  - The pipeline ID is correct and contains indexed documents
  - Your search query is sufficiently descriptive
  - The `maxChunkCount` parameter is appropriate for your use case (try increasing it if results are too sparse)

**Issue**: `ModuleNotFoundError: No module named 'gen_ai_hub'`
- **Solution**: Ensure you've installed the SAP Cloud SDK for AI with `pip install sap-ai-sdk-gen`

---

## Resources

- [SAP AI Launchpad Documentation](https://help.sap.com/docs/sap-ai-launchpad)
- [SAP AI Core Grounding Management](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/document-grounding)
- [SAP Cloud SDK for AI (Python)](https://help.sap.com/doc/generative-ai-hub-sdk/CLOUD/en-US/_reference/README_sphynx.html)
- [CrewAI Tools Documentation](https://docs.crewai.com/concepts/tools)
- [CrewAI Documentation](https://docs.crewai.com/)
- [SAP Generative AI Hub](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/generative-ai-hub-in-sap-ai-core-7db524ee75e74bf8b50c167951fe34a5)

[Next exercise](06-solve-the-crime.md)