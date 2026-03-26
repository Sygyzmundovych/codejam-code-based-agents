flowchart TD
    A["<b>AgentState (full)</b>
    suspect_names: 'Sophie, Marcus, ...'
    appraisal_result: undefined
    messages: []"]

    B["<b>appraiserNode</b>
    async function
    — reads state
    — calls LLM
    — builds appraisal result"]

    C["<b>Partial&lt;AgentState&gt; (returned)</b>
    appraisal_result: 'Appraisal: ...'
    messages: [{ role: 'assistant' ... }]"]

    D["<b>AgentState (full, after merge)</b>
    suspect_names: 'Sophie, Marcus, ...' ← unchanged
    appraisal_result: 'Appraisal: ...' ← updated
    messages: [{ role: 'assistant' ... }] ← updated"]

    A -->|"node receives full state"| B
    B -->|"node returns partial update"| C
    C -->|"LangGraph merges into state"| D