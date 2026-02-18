# Add the Grounding service

## Understand the Grounding Service


## Add the Grounding Service to your Agent Crew

### Step 4: Build the Grounding Tool

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
        dataRepositories=["bb5bd2b6-299d-44d4-9c00-3a248bee03a3"],
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
