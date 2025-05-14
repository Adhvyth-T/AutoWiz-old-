from langchain_community.chat_models import ChatOllama

llm = ChatOllama(model="tinydolphin", format="json", temperature=0)
from langchain_core.messages import HumanMessage

messages = [
    HumanMessage(
        content="What color is the sky at different times of the day?Respond using JSON"
    )
]

chat_model_response = llm.invoke(messages)
print(chat_model_response)