# Building a Multi-Agent System

## Structure Your Agent Code

Now that you know how to build a single agent with LangGraph and the SAP Cloud SDK for AI, let's structure the code for a multi-agent system. LangGraph recommends keeping agent configuration close to code.

> "LangGraph gives you full programmatic control over your agent graph. Configuration lives in code, making it type-safe, refactorable, and IDE-friendly." — LangGraph philosophy

Unlike CrewAI's YAML-first approach, in LangGraph you define agent behaviour directly in TypeScript. This means:

- No separate config files to keep in sync with your code
- Full TypeScript type checking on your agent definitions
- IDE autocomplete and refactoring across agent configuration

👉 Create the following new files in the [`src`](/project/JavaScript/starter-project/src/) folder:

- [`agentConfigs.ts`](/project/JavaScript/starter-project/src/agentConfigs.ts) — agent system prompts
- [`investigationWorkflow.ts`](/project/JavaScript/starter-project/src/investigationWorkflow.ts) — the LangGraph workflow class
- [`main.ts`](/project/JavaScript/starter-project/src/main.ts) — the entry point

---

## Define Agent Configurations

Agent configurations in LangGraph are TypeScript objects. They can contain static strings or functions that generate system prompts dynamically based on runtime data.

### Create agentConfigs.ts

👉 Open [`/project/JavaScript/starter-project/src/agentConfigs.ts`](/project/JavaScript/starter-project/src/agentConfigs.ts) and add:

```typescript
export const AGENT_CONFIGS = {
  evidenceAnalyst: {
    systemPrompt: (suspectNames: string) => `You are an Evidence Analyst.
    You are a meticulous forensic analyst who specializes in connecting dots between various pieces of evidence.
    You have access to document repositories and excel at extracting relevant information from complex data sources.

    Your goal: Analyze all available evidence and documents to identify patterns and connections between suspects and the crime

    You have access to the call_grounding_service tool to search through evidence documents.
    Analyze the suspects: ${suspectNames}

    Search for evidence related to each suspect and identify connections to the crime.`,
  },
  leadDetective: {
    systemPrompt: (
      appraisalResult: string,
      evidenceAnalysis: string,
      suspectNames: string,
    ) =>
      `You are the lead detective on this high-profile art theft case. With years of
                experience solving complex crimes, you excel at synthesizing information from
                multiple sources and identifying the culprit based on evidence and expert analysis.

      Your goal: Synthesize all findings from the team to identify the most likely suspect and build a comprehensive case

      You have received the following information from your team:

      1. INSURANCE APPRAISAL: ${appraisalResult}
      2. EVIDENCE ANALYSIS: ${evidenceAnalysis}
      3. SUSPECTS: ${suspectNames}

      Based on all the evidence and analysis, determine:
        - Who is the most likely culprit?
        - What evidence supports this conclusion?
        - What was their motive and opportunity?
        - Summarise the insurance appraisal values of the stolen artworks.
        - Calculate the total estimated insurance value of the stolen items based on the appraisal results.
        - Provide a comprehensive summary of the case.

      Be thorough and analytical in your conclusion.`,
  },
};
```

> 💡 **Understanding the configuration:**
>
> - System prompts are **functions** (not static strings) so they can incorporate runtime data like suspect names and prior agent results. TypeScript's template literals (`` `...${variable}...` ``) make this clean and readable.
> - This is the TypeScript equivalent of CrewAI's `agents.yaml` and `tasks.yaml` — but type-safe, and co-located with the code that uses it.
> - The `leadDetective.systemPrompt` function takes three arguments: the appraisal result, evidence analysis, and suspect names. This is how inter-agent communication works in LangGraph: one node's output becomes another node's input via shared state.
>   These system prompts will be read in later code implementations of the agents themselves. The extra file is to have a clearer structure and comply to the seperation of concerns paradigm.

---

## Build the Investigation Workflow

The `InvestigationWorkflow` class encapsulates the entire LangGraph workflow: the graph definition, all agent nodes, and the execution logic.

### Step 1: Create the AgentState

👉 Update your `types.ts` file to include all state fields needed for the multi-agent workflow:

```typescript
export interface AgentState {
  payload: RPT1Payload;
  suspect_names: string;
  appraisal_result?: string;
  evidence_analysis?: string;
  final_conclusion?: string;
  messages: Array<{
    role: string;
    content: string;
  }>;
}
```

> 💡 The optional fields (`?`) start as `undefined`. Each agent node fills in its part, and LangGraph merges the partial updates into the full state. The `final_conclusion` field won't be set until the lead detective runs.

### Step 2: Create the Workflow Class

👉 Create [`/project/JavaScript/starter-project/src/investigationWorkflow.ts`](/project/JavaScript/starter-project/src/investigationWorkflow.ts):

```typescript
import { StateGraph, END, START } from '@langchain/langgraph'
import { OrchestrationClient } from '@sap-ai-sdk/orchestration'
import type { AgentState, ModelParams } from './types.js'
import { callRPT1Tool } from './tools.js'
import { AGENT_CONFIGS } from './agentConfigs.js'

export class InvestigationWorkflow {
    private orchestrationClient: OrchestrationClient
    private graph: StateGraph<AgentState>

    constructor(model: string, model_params?: ModelParams) {
        this.orchestrationClient = new OrchestrationClient(
            {
                llm: { model_name: model, model_params: model_params ?? {} },
            },
            { resourceGroup: process.env.RESOURCE_GROUP },
        )
        this.graph = this.buildGraph()
    }
```

> 💡 **The constructor:**
>
> - Takes `model` and optional `model_params`: this makes the workflow reusable with different LLMs
> - Initializes `OrchestrationClient` once for the entire class; it's reused across all LLM-based nodes
> - Calls `buildGraph()` immediately so the graph is ready when you call `kickoff()`

### Step 3: Add the Appraiser Node

The appraiser node calls SAP-RPT-1 directly (no LLM involved). It takes the payload from state, runs the prediction, and stores the result.

👉 Add the appraiser node method to your class:

```typescript
    private async appraiserNode(state: AgentState): Promise<Partial<AgentState>> {
        console.log('\n🔍 Appraiser Agent starting...')

        try {
            const result = await callRPT1Tool(state.payload)

            const appraisalResult = `Insurance Appraisal Complete: ${result}
      Summary: Successfully predicted missing insurance values and item categories for the stolen artworks.`

            console.log('✅ Appraisal complete')

            return {
                appraisal_result: appraisalResult,
                messages: [...state.messages, { role: 'assistant', content: appraisalResult }],
            }
        } catch (error) {
            const errorMsg = `Error during appraisal: ${error}`
            console.error('❌', errorMsg)
            return {
                appraisal_result: errorMsg,
                messages: [...state.messages, { role: 'assistant', content: errorMsg }],
            }
        }
    }
```

### Step 4: Build the Graph

👉 Add the `buildGraph` method:

```typescript
    private buildGraph(): StateGraph<AgentState> {
        const workflow = new StateGraph<AgentState>({
            channels: {
                payload: null,
                suspect_names: null,
                appraisal_result: null,
                evidence_analysis: null,
                final_conclusion: null,
                messages: null,
            },
        })

        workflow
            .addNode('appraiser', this.appraiserNode.bind(this))
            .addEdge(START, 'appraiser')
            .addEdge('appraiser', END)

        return workflow
    }
```

> 💡 **Understanding `.bind(this)`:**
>
> When you pass a class method as a callback, JavaScript loses the `this` context; the function no longer knows it belongs to the class. `.bind(this)` creates a new function with `this` permanently set to the class instance. This is a standard JavaScript pattern when passing class methods as callbacks.

> ⚠️ **Important — Chained API in LangGraph 0.2+:**
>
> LangGraph 0.2 changed the API for building graphs. You **must** chain `.addNode()`, `.addNode()`, `.addEdge()` calls together rather than calling them separately. Separate calls cause TypeScript type errors because node names aren't known until all nodes are registered.
>
> ```typescript
> // ✅ Correct (chained)
> workflow
>   .addNode("appraiser", this.appraiserNode.bind(this))
>   .addEdge(START, "appraiser")
>   .addEdge("appraiser", END);
>
> // ❌ Incorrect (separate calls — TypeScript errors in LangGraph 0.2+)
> workflow.addNode("appraiser", this.appraiserNode.bind(this));
> workflow.addEdge(START, "appraiser");
> ```

### Step 5: Add the kickoff Method

👉 Add the `kickoff` method to run the workflow:

```typescript
    async kickoff(inputs: { payload: any; suspect_names: string }): Promise<string> {
        console.log('🚀 Starting Investigation Workflow...\n')

        const initialState: AgentState = {
            payload: inputs.payload,
            suspect_names: inputs.suspect_names,
            messages: [],
        }

        const app = this.graph.compile()
        const result = await app.invoke(initialState)

        return result.final_conclusion || 'Investigation completed but no conclusion was reached.'
    }
}
```

### Step 6: Create main.ts

👉 Create [`/project/JavaScript/starter-project/src/main.ts`](/project/JavaScript/starter-project/src/main.ts):

```typescript
import "dotenv/config";
import { InvestigationWorkflow } from "./investigationWorkflow.js";
import { payload } from "./payload.js";

async function main() {
  const workflow = new InvestigationWorkflow(process.env.MODEL_NAME!);
  const suspectNames = "Sophie Dubois, Marcus Chen, Viktor Petrov";

  const result = await workflow.kickoff({
    payload,
    suspect_names: suspectNames,
  });

  console.log("\n📘 FINAL INVESTIGATION REPORT\n");
  console.log(result);
}

main();
```

### Step 7: Run Your Workflow

```bash
npx tsx src/main.ts
```

---

## Adding More Agents to the Workflow

Now add the **Evidence Analyst** as a second agent. This agent will search evidence documents for each suspect (we'll connect it to real documents in the next exercise; for now it uses the LLM directly).

### Step 1: Add the Evidence Analyst Node

👉 Add this method to your `InvestigationWorkflow` class:

```typescript
    private async evidenceAnalystNode(state: AgentState): Promise<Partial<AgentState>> {
        console.log('\n🔍 Evidence Analyst starting...')

        try {
            const suspects = state.suspect_names.split(',').map(s => s.trim())
            const evidenceResults: string[] = []

            for (const suspect of suspects) {
                console.log(`  Searching evidence for: ${suspect}`)
                // Placeholder — will be replaced with real grounding tool in Exercise 05
                evidenceResults.push(`Evidence for ${suspect}: No evidence documents connected yet.`)
            }

            const evidenceAnalysis = `Evidence Analysis Complete: ${evidenceResults.join('\n\n')}
      Summary: Analyzed evidence for all suspects: ${state.suspect_names}`

            console.log('✅ Evidence analysis complete')

            return {
                evidence_analysis: evidenceAnalysis,
                messages: [...state.messages, { role: 'assistant', content: evidenceAnalysis }],
            }
        } catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error)
            console.error('❌ Evidence analysis failed:', errorMsg)
            return {
                evidence_analysis: `Error during evidence analysis: ${errorMsg}`,
                messages: [...state.messages, { role: 'assistant', content: `Error during evidence analysis: ${errorMsg}` }],
            }
        }
    }
```

> 💡 **`for...of` with `await` is sequential.** Unlike JavaScript's `Promise.all`, a `for...of` loop processes suspects one at a time. This is intentional: it makes logs readable and avoids overwhelming the external services. In Exercise 05, you'll call the real grounding service inside this loop.

> 💡 **`error instanceof Error ? error.message : String(error)`** is a safe way to extract an error message. The `instanceof Error` check handles proper `Error` objects (which have `.message` and `.stack`). The `String(error)` fallback handles cases where someone throws a plain string or object.

### Step 2: Update buildGraph to Include Both Nodes

👉 Update the `buildGraph` method:

```typescript
    private buildGraph(): StateGraph<AgentState> {
        const workflow = new StateGraph<AgentState>({
            channels: {
                payload: null,
                suspect_names: null,
                appraisal_result: null,
                evidence_analysis: null,
                final_conclusion: null,
                messages: null,
            },
        })

        workflow
            .addNode('appraiser', this.appraiserNode.bind(this))
            .addNode('evidence_analyst', this.evidenceAnalystNode.bind(this))
            .addEdge(START, 'appraiser')
            .addEdge('appraiser', 'evidence_analyst')
            .addEdge('evidence_analyst', END)

        return workflow
    }
```

### Step 3: Run the Two-Agent Workflow

```bash
npx tsx src/main.ts
```

> 💡 **Note:** The Evidence Analyst currently produces placeholder output because it doesn't have access to real evidence documents yet. You'll connect it to the Grounding Service in Exercise 05.

---

## Understanding Multi-Agent Workflows

### What Just Happened?

You've built a **multi-agent LangGraph workflow** with specialized roles working in sequence:

**1. Code-Based Configuration**

- Agent system prompts live in `agentConfigs.ts` — TypeScript objects instead of YAML files
- Configuration is type-safe, refactorable, and co-located with the code that uses it

**2. Specialized Agent Nodes**

- **Appraiser Node** — Calls the SAP-RPT-1 model directly to predict insurance values
- **Evidence Analyst Node** — Will search evidence documents for each suspect

**3. Sequential Execution with Shared State**

- LangGraph executes nodes in order following the edges you defined
- Each node reads from and writes to the shared `AgentState`
- The appraiser runs first, then the evidence analyst builds on that state

### How the Execution Flow Works

When you call `workflow.kickoff(inputs)`:

1. **Initialization**: `app.invoke(initialState)` starts the graph
2. **Appraiser runs**: Calls RPT-1, stores result in `appraisal_result`
3. **Evidence Analyst runs**: Reads `suspect_names`, stores result in `evidence_analysis`
4. **Graph ends**: Returns the final state

### LangGraph vs CrewAI — Multi-Agent Architecture

| CrewAI (Python)                       | LangGraph (TypeScript)                            |
| ------------------------------------- | ------------------------------------------------- |
| `agents.yaml` + `tasks.yaml`          | `agentConfigs.ts` (TypeScript objects)            |
| `@CrewBase` class decorator           | Plain TypeScript class (`InvestigationWorkflow`)  |
| `@agent`, `@task`, `@crew` decorators | `buildGraph()` method with `.addNode().addEdge()` |
| `Process.sequential`                  | Edges define the execution order                  |
| `self.agents` auto-collected          | Nodes registered explicitly with `.addNode()`     |
| `crew.kickoff(inputs={})`             | `app.invoke(initialState)`                        |

> 💡 **LangGraph's approach gives you more explicit control.** Every transition between agents is an edge you define. There's no magic collection of agents via decorators; the graph structure is transparent and debuggable.

---

## Key Takeaways

- **LangGraph StateGraph** connects agent nodes with typed edges — the execution order is explicit
- **Code-based configuration** in `agentConfigs.ts` replaces YAML files — type-safe and co-located
- **`.bind(this)`** is required when passing class methods as LangGraph node callbacks
- **Chained API** (`.addNode().addEdge()`) is required in LangGraph 0.2+
- **`for...of` with `await`** processes items sequentially — predictable, readable, no race conditions
- **`Partial<AgentState>`** return type means nodes only update the fields they changed

**What's Next?**

The Evidence Analyst can't access actual evidence yet. In Exercise 05, you'll integrate the **Grounding Service** to give it real document access.

---

## Next Steps

1. ✅ [Understand Generative AI Hub](00-understanding-genAI-hub.md)
2. ✅ [Set up your development space](01-setup-dev-space.md)
3. ✅ [Build a basic agent](02-build-a-basic-agent.md)
4. ✅ [Add custom tools](03-add-your-first-tool.md) (RPT-1 model integration)
5. ✅ [Build a multi-agent workflow](04-building-multi-agent-system.md) (this exercise)
6. 📌 [Add the Grounding Service](05-add-the-grounding-service.md): Give your Evidence Analyst access to real documents
7. 📌 [Solve the crime](06-solve-the-crime.md): Add a Lead Detective to combine findings and crack the case

---

## Troubleshooting

**Issue**: `TypeError: this is undefined` inside node methods

- **Solution**: Ensure you're using `.bind(this)` when registering class methods as nodes: `.addNode('appraiser', this.appraiserNode.bind(this))`

**Issue**: TypeScript error on `.addEdge()`: node name not recognized

- **Solution**: Make sure you're chaining `.addNode().addNode().addEdge()` calls. In LangGraph 0.2+, calling `addEdge` before all nodes are registered causes type errors.

**Issue**: `process.env.MODEL_NAME` is `undefined`

- **Solution**: Ensure `import 'dotenv/config'` is at the top of `main.ts` (the first import). Without this, environment variables from `.env` aren't loaded.

**Issue**: Agent nodes run but state fields are undefined in later nodes

- **Solution**: Check that each node returns the correct field names matching your `AgentState` interface. Typos in field names will silently result in `undefined` in downstream nodes.

---

## Resources

- [LangGraph.js StateGraph Documentation](https://langchain-ai.github.io/langgraphjs/concepts/low_level/)
- [SAP Cloud SDK for AI (JavaScript)](https://github.com/SAP/ai-sdk-js)
- [SAP Generative AI Hub](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/generative-ai-hub-in-sap-ai-core-7db524ee75e74bf8b50c167951fe34a5)

[Next exercise](05-add-the-grounding-service.md)
