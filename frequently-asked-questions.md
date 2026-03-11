# Frequently Asked Questions

## Setup & Configuration

### What Python versions are compatible with CrewAI?

CrewAI requires Python 3.10, 3.11, 3.12, or 3.13. If you're using Python 3.9 or older, you'll need to upgrade. On macOS, you can use Homebrew to install a compatible version: `brew install python@3.11`.

### What's the difference between SAP AI Core and SAP AI Launchpad?

**SAP AI Core** is SAP's AI runtime where you can train models, fine-tune models, or deploy machine learning models. It's the underlying service that executes AI workloads.

**SAP AI Launchpad** is the UI/frontend for SAP AI Core. It's a multitenant SaaS application on SAP BTP where you can try out models, manage deployments, start training jobs, build orchestration pipelines, and access Generative AI Hub.

Think of it this way: AI Core is the engine, AI Launchpad is the dashboard.

### What is a resource group and why shouldn't I use 'default'?

Resource groups in SAP AI Core isolate AI resources and workloads within a tenant. They help organize deployments, configurations, and executions for different projects or teams.

For this CodeJam, you should use the `ai-agents-codejam` resource group instead of `default` to ensure:
- Your resources don't conflict with other users
- You have access to the pre-configured grounding pipeline
- Your deployments are properly isolated

### Why do I need a virtual environment?

A Python virtual environment (`venv`) provides isolated package installations, preventing conflicts between different projects. It ensures:
- Dependencies for this project don't interfere with system Python
- You can reproduce the exact environment on different machines
- Package versions remain consistent throughout the CodeJam

---

## LiteLLM & Model Selection

### What does "sap/gpt-4o" mean in the LLM parameter?

The format is `provider/model_name`. In this case:
- `sap` = the LLM provider (SAP's Generative AI Hub)
- `gpt-4o` = the specific model to use

LiteLLM uses this syntax to route requests to the correct provider. You can access over 30 models through SAP's Generative AI Hub using the `sap/` prefix.

### Can I use other LLM providers besides SAP?

Yes! LiteLLM provides a unified API for calling LLMs from multiple providers. You can use:
- **SAP models**: `sap/gpt-4o`, `sap/anthropic--claude-4.5-opus`
- **Azure OpenAI**: Use appropriate provider syntax
- **Amazon Bedrock** (including Anthropic models)
- **Google Gemini**
- Self-hosted open source models

The power of LiteLLM is that you can switch providers without changing your CrewAI code—just update the `llm` parameter.

### Can I use different LLM models for different agents?

Absolutely! Each agent can specify its own LLM in the YAML configuration:

```yaml
appraiser_agent:
  llm: sap/gpt-4o

evidence_analyst_agent:
  llm: sap/anthropic--claude-4.5-opus
```

This allows you to optimize cost and performance by choosing the best model for each agent's specific task.

---

## CrewAI Framework

### What's the difference between an Agent, Task, and Crew?

**Agent**: An AI entity with a specific role, goal, and backstory. It represents a specialist (e.g., "Loss Appraiser", "Detective"). The agent uses an LLM as its reasoning engine.

**Task**: A specific objective assigned to an agent. Tasks have a description (what to do) and expected output (what should be delivered). Tasks drive agent actions.

**Crew**: A collection of agents and their tasks working together. The crew orchestrates how agents collaborate and in what order tasks execute.

Think of it like a company: Agents are employees, Tasks are their assignments, and the Crew is the organizational structure.

### Why use YAML files instead of defining everything in Python?

According to CrewAI's official recommendation: *"Using YAML configuration provides a cleaner, more maintainable way to define agents. We strongly recommend using this approach in CrewAI projects."*

Benefits include:
- **Separation of concerns**: Configuration (YAML) vs. implementation (Python)
- **Easy modifications**: Change agent behavior without touching code
- **Readability**: Non-programmers can understand and adjust agent definitions
- **Version control**: Track configuration changes separately from logic

### What do the @tool, @agent, @task, @crew decorators do?

These are Python decorators that register components with the CrewAI framework:

- **@tool**: Converts a Python function into a tool that agents can use. The function's docstring becomes the tool description that helps the LLM understand when to use it.

- **@agent**: Marks a method as returning an Agent object. CrewAI automatically collects all @agent methods into `self.agents`.

- **@task**: Marks a method as returning a Task object. CrewAI automatically collects all @task methods into `self.tasks`.

- **@crew**: Marks a method as defining the crew configuration (agents, tasks, process type). Required for CrewAI to execute the crew.

### What's the difference between sequential and hierarchical processing?

**Sequential Processing** (`Process.sequential`):
- Tasks execute in the order they're defined
- Each task completes before the next begins
- Simple, predictable execution flow
- Example: Appraiser → Evidence Analyst → Detective (one after another)

**Hierarchical Processing** (`Process.hierarchical`):
- A manager agent coordinates and delegates tasks
- The manager decides which agents to use and in what order
- More flexible but requires a coordination agent
- Example: Manager decides if appraiser or analyst should go first based on context

For this CodeJam, we use sequential processing.

### How do agents communicate with each other?

Agents communicate through the `context` parameter in task definitions:

```python
@task
def solve_crime(self) -> Task:
    return Task(
        config=self.tasks_config['solve_crime'],
        context=[self.appraise_loss_task(), self.analyze_evidence_task()]
    )
```

This tells CrewAI that the `solve_crime` task should receive outputs from both `appraise_loss_task` and `analyze_evidence_task` as context. The Lead Detective can then use findings from both the Appraiser and Evidence Analyst.

---

## Tools & SAP-RPT-1

### What is SAP-RPT-1 and when should I use it?

**SAP-RPT-1** (SAP's Relational Pretrained Transformer) is a foundation model trained on structured data. It's designed for:
- **Classification tasks**: Predicting categories (e.g., "Painting", "Sculpture", "Jewelry")
- **Regression tasks**: Predicting numeric values (e.g., insurance values)

Use it when:
- You have tabular/structured data (CSV, JSON with rows and columns)
- You need predictive insights without building custom ML models
- You want to make predictions based on example data patterns

### What's the difference between classification and regression in RPT-1?

**Classification**: Predicts a category from a set of options
```python
{
    "name": "ITEM_CATEGORY",
    "prediction_placeholder": "'[PREDICT]'",
    "task_type": "classification"  # Predicts: "Painting", "Sculpture", etc.
}
```

**Regression**: Predicts a numeric value
```python
{
    "name": "INSURANCE_VALUE",
    "prediction_placeholder": "'[PREDICT]'",
    "task_type": "regression"  # Predicts: 45000000, 2500000, etc.
}
```

### How do I create a custom tool for my agent?

1. **Write a Python function** that implements the tool's logic
2. **Add the @tool decorator** with a descriptive name
3. **Write a clear docstring** explaining what the tool does (the LLM reads this!)
4. **Assign the tool to your agent** using `tools=[your_tool]`

Example:
```python
@tool("call_rpt1")
def call_rpt1(payload: dict) -> str:
    """Call RPT-1 model to predict missing values in the payload.
    
    Args:
        payload: A dictionary containing data with prediction placeholders.
    
    Returns:
        JSON string with predicted values.
    """
    response = rpt1_client.post_request(json_payload=payload)
    return response.json()
```

### Why does the tool need a docstring?

The docstring is critical because **the LLM reads it** to understand:
- What the tool does
- When to use it
- What parameters it needs
- What it returns

Without a clear docstring, the agent won't know when or how to use the tool. The docstring is essentially instructions for the AI agent.

---

## Grounding Service & RAG

### What is grounding and why is it important?

**Grounding** (also called RAG - Retrieval-Augmented Generation) connects LLMs to external, up-to-date data sources. It solves the **hallucination problem**:

**Without Grounding**: LLM makes up plausible-sounding "facts"
- ❌ No source citations
- ❌ Can't access private/recent data
- ❌ Unreliable for critical decisions

**With Grounding**: LLM retrieves real documents first
- ✅ Cites specific sources
- ✅ Accesses your latest documents
- ✅ Factual and auditable

Example: Instead of guessing "Marcus was probably fired for performance issues," a grounded agent can state: "According to MARCUS_TERMINATION_LETTER.txt, Marcus was terminated on 2024-01-15 for 'unauthorized access to secured areas.'"

### What's the difference between grounding and fine-tuning?

| Fine-Tuning | Grounding (RAG) |
|-------------|-----------------|
| ❌ Expensive ($1000s per training) | ✅ Cost-effective (pay per search) |
| ❌ Weeks to retrain when data updates | ✅ Instant—add/update documents |
| ❌ Black box—can't trace sources | ✅ Full transparency with citations |
| ❌ Model "memorizes" data (privacy risk) | ✅ Documents stay separate (secure) |
| ❌ Requires ML expertise | ✅ Simple API calls |

**Best Practice**: Use grounding for knowledge that changes (documents, data, evidence). Use fine-tuning for behavior/style (e.g., "always be polite").

### What are embeddings?

Embeddings are numeric representations of text (vectors—arrays of numbers, typically ~1,536 dimensions). They capture semantic meaning:

- "unauthorized access" → [0.23, -0.45, 0.87, ...]
- "broke into secure area" → [0.21, -0.43, 0.89, ...]

These vectors are similar because the phrases have similar meanings. Vector search compares embeddings to find semantically related content, even if the exact words differ.

### Why do documents need to be chunked?

Large documents are split into smaller chunks (e.g., 500-word passages) for several reasons:

1. **LLM context limits**: Models can't process entire books at once
2. **Search precision**: Smaller chunks = more targeted results
3. **Relevance scoring**: Each chunk gets its own relevance score
4. **Processing efficiency**: Faster to search and retrieve smaller pieces

Example: "MARCUS_TERMINATION_LETTER.txt" (5 pages) → 3 chunks, each searchable independently.

### What's the difference between semantic search and keyword search?

**Keyword Search** (traditional):
- Matches exact words
- "Marcus Chen termination" finds documents with those exact words
- Misses synonyms and related concepts

**Semantic Search** (vector-based):
- Understands meaning
- "Why was Marcus fired?" finds "termination letter", "dismissed", "employment ended"
- Matches conceptually related content even with different words

The grounding service uses semantic search via embeddings, making it much more powerful for finding relevant evidence.

### How does the grounding pipeline work?

**Phase 1: Document Preparation** (done once):
1. Upload documents to SAP Object Store (S3)
2. Split into chunks (~500 words each)
3. Convert chunks to embeddings (vectors)
4. Store in vector database for fast search

**Phase 2: Query Processing** (each agent query):
1. Agent asks: "What evidence exists about Marcus?"
2. Query converted to embedding vector
3. Vector database finds similar chunks (cosine similarity)
4. Top 5 most relevant chunks retrieved

**Phase 3: Context-Enhanced Response**:
1. Retrieved chunks passed to LLM as context
2. LLM generates answer based ONLY on chunks
3. Agent receives factual, grounded response

---

## Multi-Agent Systems

### When should I use multiple agents vs. a single agent?

Use **multiple agents** when:
- Tasks require different expertise (valuation vs. investigation)
- Different tools are needed (RPT-1 vs. Grounding Service)
- You want parallel processing of independent tasks
- Complex problems benefit from specialized perspectives

Use a **single agent** when:
- Task is simple and focused
- One tool/skillset is sufficient
- No need for collaboration or delegation

For this CodeJam: Loss Appraiser (RPT-1 expert) + Evidence Analyst (document search) + Lead Detective (coordinator) = better than one "do everything" agent.

### What is the task context parameter?

The `context` parameter links tasks together, allowing one task to use outputs from previous tasks:

```python
@task
def solve_crime(self) -> Task:
    return Task(
        config=self.tasks_config['solve_crime'],
        context=[self.appraise_loss_task(), self.analyze_evidence_task()]
    )
```

This means:
- `solve_crime` receives results from `appraise_loss_task` and `analyze_evidence_task`
- The Lead Detective can read what the Appraiser and Evidence Analyst found
- Enables information flow between specialized agents

---

## Best Practices

### What makes a good agent role/goal/backstory?

**Role**: Defines identity and expertise domain
- ✅ Good: "Loss Appraiser specializing in fine art"
- ❌ Bad: "Helper"

**Goal**: Specifies what to accomplish
- ✅ Good: "Predict missing insurance values using RPT-1 tool with the provided payload"
- ❌ Bad: "Do something useful"

**Backstory**: Provides context and personality
- ✅ Good: "You are an experienced insurance appraiser with 20 years of expertise in art valuation"
- ❌ Bad: "You are an AI"

**Why it matters**: The LLM reads these in natural language to understand how to behave, what to prioritize, and how to approach tasks.

### How specific should task descriptions be?

Be **very specific**. Task descriptions guide the LLM's reasoning:

✅ **Good** (specific):
```yaml
description: >
  Analyze each suspect by searching evidence documents using the call_grounding_service tool.
  For each of the three suspects, find: alibi verification, financial motives, 
  access logs, and connections to the crime. Cross-reference findings.
```

❌ **Bad** (vague):
```yaml
description: >
  Look at the evidence and figure out who did it.
```

The more explicit you are about steps, tools to use, and expected reasoning, the better the agent performs.

### When should I use f-strings vs regular strings?

Use **f-strings** (formatted strings) when your text contains template variables:

```python
goal=f"Use the RPT-1 tool with this payload: {payload}"  # ✅ f-string needed
```

Use **regular strings** for static text:

```python
role="Loss Appraiser"  # ✅ No variables, regular string fine
```

In YAML files, use `{variable_name}` placeholders without f-string syntax. CrewAI automatically interpolates them from the `inputs` dictionary passed to `kickoff()`.

---

## Need More Help?

For additional support during the CodeJam:
- Ask your instructor for clarification
- Review the exercise documentation in `/exercises/Python/`
- Check the official documentation:
  - [CrewAI Documentation](https://docs.crewai.com/)
  - [SAP AI Core Documentation](https://help.sap.com/docs/sap-ai-core)
  - [LiteLLM Documentation](https://docs.litellm.ai/)
