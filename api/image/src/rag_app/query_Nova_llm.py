import boto3
import json
from pydantic import BaseModel

from rag_app.query_database import query_database
from rag_app.prompts import SYSTEM_PROMPT

class QueryResponse(BaseModel):
    response_text: str 
    history: list

client = boto3.client("bedrock-runtime")

model_id = "arn:aws:bedrock:ap-southeast-2:087484586207:inference-profile/apac.amazon.nova-lite-v1:0"

inf_params = {"maxTokens": 300, "topP": 0.9, "temperature": 0.3}

def format_user(text: str):
    return {
        "role": "user",
        "content": [{"text": text}]
    } 

def format_assistant(text: str):
    return {
        "role": "assistant",
        "content": [{"text": text}]
    }

def format_system_prompt(text: str):
    return [{
        "text": text
    }]

def query_rag(message: str, history: list=[]):
    user_message = format_user(message)
    history.append(user_message)
    context = query_database(message)

    if (context != ""):
        formated_context = format_assistant(context)
        history.append(formated_context)

    response = query_llm(history)
    formated_response = response["output"]["message"]
    history.append(formated_response)
    return QueryResponse(response_text=formated_response["content"][0]["text"], history=history)

def query_llm(history: list):
    body=json.dumps(
        {
            "messages": history,
            "system": format_system_prompt(SYSTEM_PROMPT),
            "inferenceConfig": inf_params
        }
    )

    response = client.invoke_model(body=body, modelId=model_id)
    response_body = json.loads(response.get('body').read())

    return response_body
