import pandas as pd
from app.orchestration.recommendation_api.swagger_client import SwaggerClient

import os
from dotenv import load_dotenv
load_dotenv()
SWAGGER = os.getenv("PET_SWAGGER")


def get_endpoints():
    swagger = SwaggerClient(SWAGGER)
    modules, _ = swagger.get_endpoints()
    return modules

def get_df_endpoints():
    data = get_endpoints()
    dfs = []
    for item in data:
        df = pd.DataFrame(item.get('Endpoints'))
        df["modulo"] = item.get('Modulo')
        df["description_modulo"] = item.get('description_modulo')
        dfs.append(df)

    df_endpoints = pd.concat(dfs)
    return df_endpoints

def get_docs_into_examples():
    df_endpoints = get_df_endpoints()
    examples = [
        {
            "input": f"{row['modulo']} - {row['description_modulo']} - {row['description']} - {row['properties']} - {row['response']}",
            "output": f"method: {row['method']} - path: {row['path']}"
        }
        for _, row in df_endpoints.iterrows()
    ]
    return examples

examples = get_docs_into_examples()
