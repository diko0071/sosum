from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.callbacks import get_openai_callback
from .serializers import PromptLogSerializer
import os

def openai_call(system_message, user_message):
    llm = ChatOpenAI(model_name="gpt-4-0613", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_message)
    ]

    with get_openai_callback() as cb:
        response = llm.invoke(messages)
        cost = cb.total_cost
        input_tokens = cb.prompt_tokens
        output_tokens = cb.completion_tokens

        log_data = {
            "system_message": system_message,
            "user_message": user_message, 
            "response": response.content,
            "cost": cost,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens
        }

    serializer = PromptLogSerializer(data=log_data)

    if serializer.is_valid():
        prompt_log = serializer.save()

    return response.content 