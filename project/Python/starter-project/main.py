from investigator_crew import InvestigatorCrew
    
def main():
    # Define the JSON payload for prediction
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


    result = InvestigatorCrew().crew().kickoff(inputs={'payload': payload})
    print("\n📘 Result:\n", result)


if __name__ == "__main__":
    main()