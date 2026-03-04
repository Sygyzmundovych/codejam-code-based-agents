# Add the Grounding service

## Understand the Grounding Service

👉 Go to [SAP AI Launchpad](https://genai-codejam-luyq1wkg.ai-launchpad.prod.eu-central-1.aws.ai-prod.cloud.sap/aic/index.html#/workspaces&/a/detail/TwoColumnsMidExpanded/?workspace=api-connection&resourceGroup=s3-grounding) 

👉 And follow the isntructions [here](https://github.com/SAP-samples/generative-ai-codejam/blob/main/exercises/07-orchestration-service-UI-S3-grounding.md) to get to know the grounding service.

## Add the Grounding Service to your Agent Crew

### Step 1: Build the Grounding Tool

The new agent is still missing the grounding tool. Let's build it!

👉 To the [`/project/Python/starter-project/investigator_crew.py`](/project/Python/starter-project/investigator_crew.py) you will add the code below:

```python
@tool("call_grounding_service")
def call_grounding_service(user_question: str) -> str:
    """Function to call the grounding service and retrieve relevant information based on the user's question."""
    retrieval_client = RetrievalAPIClient()

    search_filter = RetrievalSearchFilter(
        id="vector",
        dataRepositoryType=DataRepositoryType.VECTOR.value,
        dataRepositories=["YOUR REPO ID HERE"], #pipeline s3 grounding codejam
        searchConfiguration={
            "maxChunkCount": 2
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

### Step 2: Get the pipeline ID from SAP AI Launchpad

👉 Navigate back to `Workspaces`and select the resource groups `ai-agents-codejam`

👉 Navigate to Grounding Management and select the pipeline ID from there.

### EMEGERNCY STEP: mock the grounding service
Unfortunately, there is an issue with the grounding service right now and we will have to use this mock service instead:

```python
@tool("call_grounding_service")
def call_grounding_service(user_question: str) -> str:
    """Function to call the grounding service and retrieve relevant information based on the user's question."""
    response_dict = mock_grounding_service(user_question)
    return response_dict
```

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

### Step 4: Add the Tool to Your Agent

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

[Next exercise](06-solve-the-crime.md)