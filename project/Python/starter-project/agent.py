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
    result = crew.kickoff()
    print("\n" + "="*50)
    print("Insurance Appraiser Report:")
    print("="*50)
    print(result)

if __name__ == "__main__":
    main()