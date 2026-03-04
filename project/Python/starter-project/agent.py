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
                    "name": "INSURANCE_VALUE",
                    "prediction_placeholder": "'[PREDICT]'",
                    "task_type": "regression",
                },
                {
                    "name": "ITEM_CATEGORY",
                    "prediction_placeholder": "'[PREDICT]'",
                    "task_type": "classification",
                },
            ]
        },
        "index_column": "ITEM_ID",
        "rows": [
            {
                "ITEM_ID": "ART_001",
                "ITEM_NAME": "Water Lilies - Series 1",
                "ARTIST": "Claude Monet",
                "ACQUISITION_DATE": "1987-03-15",
                "INSURANCE_VALUE": 45000000,
                "ITEM_CATEGORY": "Painting",
                "DIMENSIONS": "200x180cm",
                "CONDITION_SCORE": 9,
                "RARITY_SCORE": 9,
                "PROVENANCE_CLARITY": 8,
            },
            {
                "ITEM_ID": "ART_002",
                "ITEM_NAME": "Japanese Bridge at Giverny",
                "ARTIST": "Claude Monet",
                "ACQUISITION_DATE": "1995-06-22",
                "INSURANCE_VALUE": 42000000,
                "ITEM_CATEGORY": "Painting",
                "DIMENSIONS": "92x73cm",
                "CONDITION_SCORE": 8,
                "RARITY_SCORE": 8,
                "PROVENANCE_CLARITY": 9,
            },
            {
                "ITEM_ID": "ART_003",
                "ITEM_NAME": "Irises",
                "ARTIST": "Vincent van Gogh",
                "ACQUISITION_DATE": "2001-11-08",
                "INSURANCE_VALUE": "'[PREDICT]'",
                "ITEM_CATEGORY": "Painting",
                "DIMENSIONS": "71x93cm",
                "CONDITION_SCORE": 7,
                "RARITY_SCORE": 9,
                "PROVENANCE_CLARITY": 8,
            },
            {
                "ITEM_ID": "ART_004",
                "ITEM_NAME": "Starry Night Over the Rhone",
                "ARTIST": "Vincent van Gogh",
                "ACQUISITION_DATE": "1998-09-14",
                "INSURANCE_VALUE": 48000000,
                "ITEM_CATEGORY": "Painting",
                "DIMENSIONS": "73x92cm",
                "CONDITION_SCORE": 8,
                "RARITY_SCORE": 9,
                "PROVENANCE_CLARITY": 9,
            },
            {
                "ITEM_ID": "ART_005",
                "ITEM_NAME": "The Birth of Venus",
                "ARTIST": "Sandro Botticelli",
                "ACQUISITION_DATE": "1992-04-30",
                "INSURANCE_VALUE": 55000000,
                "ITEM_CATEGORY": "Painting",
                "DIMENSIONS": "172x278cm",
                "CONDITION_SCORE": 6,
                "RARITY_SCORE": 10,
                "PROVENANCE_CLARITY": 10,
            },
            {
                "ITEM_ID": "ART_006",
                "ITEM_NAME": "Primavera",
                "ARTIST": "Sandro Botticelli",
                "ACQUISITION_DATE": "1989-02-19",
                "INSURANCE_VALUE": 52000000,
                "ITEM_CATEGORY": "Painting",
                "DIMENSIONS": "203x314cm",
                "CONDITION_SCORE": 7,
                "RARITY_SCORE": 10,
                "PROVENANCE_CLARITY": 10,
            },
            {
                "ITEM_ID": "ART_007",
                "ITEM_NAME": "Girl with a Pearl Earring",
                "ARTIST": "Johannes Vermeer",
                "ACQUISITION_DATE": "2003-07-11",
                "INSURANCE_VALUE": "'[PREDICT]'",
                "ITEM_CATEGORY": "Painting",
                "DIMENSIONS": "44x39cm",
                "CONDITION_SCORE": 8,
                "RARITY_SCORE": 10,
                "PROVENANCE_CLARITY": 9,
            },
            {
                "ITEM_ID": "ART_008",
                "ITEM_NAME": "The Music Lesson",
                "ARTIST": "Johannes Vermeer",
                "ACQUISITION_DATE": "1994-05-20",
                "INSURANCE_VALUE": 38000000,
                "ITEM_CATEGORY": "Painting",
                "DIMENSIONS": "64x73cm",
                "CONDITION_SCORE": 8,
                "RARITY_SCORE": 9,
                "PROVENANCE_CLARITY": 9,
            },
            {
                "ITEM_ID": "ART_009",
                "ITEM_NAME": "The Persistence of Memory",
                "ARTIST": "Salvador Dalí",
                "ACQUISITION_DATE": "2005-03-10",
                "INSURANCE_VALUE": 35000000,
                "ITEM_CATEGORY": "'[PREDICT]'",
                "DIMENSIONS": "24x33cm",
                "CONDITION_SCORE": 9,
                "RARITY_SCORE": 9,
                "PROVENANCE_CLARITY": 10,
            },
            {
                "ITEM_ID": "ART_010",
                "ITEM_NAME": "Metamorphosis of Narcissus",
                "ARTIST": "Salvador Dalí",
                "ACQUISITION_DATE": "1996-08-12",
                "INSURANCE_VALUE": 32000000,
                "ITEM_CATEGORY": "Painting",
                "DIMENSIONS": "51x78cm",
                "CONDITION_SCORE": 8,
                "RARITY_SCORE": 8,
                "PROVENANCE_CLARITY": 8,
            },
            {
                "ITEM_ID": "ART_011",
                "ITEM_NAME": "The Bronze Dancer",
                "ARTIST": "Auguste Rodin",
                "ACQUISITION_DATE": "1991-07-22",
                "INSURANCE_VALUE": 8500000,
                "ITEM_CATEGORY": "Sculpture",
                "DIMENSIONS": "Height: 1.8m",
                "CONDITION_SCORE": 9,
                "RARITY_SCORE": 7,
                "PROVENANCE_CLARITY": 8,
            },
            {
                "ITEM_ID": "ART_012",
                "ITEM_NAME": "The Thinker",
                "ARTIST": "Auguste Rodin",
                "ACQUISITION_DATE": "2000-11-05",
                "INSURANCE_VALUE": "'[PREDICT]'",
                "ITEM_CATEGORY": "Sculpture",
                "DIMENSIONS": "Height: 1.9m",
                "CONDITION_SCORE": 9,
                "RARITY_SCORE": 7,
                "PROVENANCE_CLARITY": 9,
            },
            {
                "ITEM_ID": "ART_013",
                "ITEM_NAME": "Hope Diamond Replica - Royal Cut",
                "ARTIST": "Unknown Jeweler",
                "ACQUISITION_DATE": "1988-02-19",
                "INSURANCE_VALUE": 12000000,
                "ITEM_CATEGORY": "Jewelry",
                "DIMENSIONS": "Width: 15cm",
                "CONDITION_SCORE": 10,
                "RARITY_SCORE": 10,
                "PROVENANCE_CLARITY": 7,
            },
            {
                "ITEM_ID": "ART_014",
                "ITEM_NAME": "Cartier Ruby Necklace - 1920s",
                "ARTIST": "Cartier",
                "ACQUISITION_DATE": "2002-09-11",
                "INSURANCE_VALUE": 9500000,
                "ITEM_CATEGORY": "Jewelry",
                "DIMENSIONS": "Length: 45cm",
                "CONDITION_SCORE": 9,
                "RARITY_SCORE": 8,
                "PROVENANCE_CLARITY": 9,
            },
        ],
        "data_schema": {
            "ITEM_ID": {"dtype": "string"},
            "ITEM_NAME": {"dtype": "string"},
            "ARTIST": {"dtype": "string"},
            "ACQUISITION_DATE": {"dtype": "date"},
            "INSURANCE_VALUE": {"dtype": "numeric"},
            "ITEM_CATEGORY": {"dtype": "string", "categories": ["Painting", "Sculpture", "Jewelry"]},
            "DIMENSIONS": {"dtype": "string"},
            "CONDITION_SCORE": {"dtype": "numeric", "range": [1, 10], "description": "1=Poor to 10=Pristine"},
            "RARITY_SCORE": {"dtype": "numeric", "range": [1, 10], "description": "1=Common to 10=Extremely Rare"},
            "PROVENANCE_CLARITY": {"dtype": "numeric", "range": [1, 10], "description": "1=Unknown to 10=Perfect Documentation"},
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
    role="Stolen Goods Loss Appraiser",
    goal=f"Predict the monetary value of stolen items ONLY by calling the call_rpt1 tool with payload {payload}. Do NOT invent or estimate values yourself. If the tool call fails, report the failure.",
    backstory="You are an insurance appraiser who relies strictly on model predictions. You never guess values.",
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