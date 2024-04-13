import chainlit as cl
from openai import AsyncOpenAI
import ast
import os, json
from chainlit.playground.providers.openai import stringify_function_call
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig

load_dotenv()

# Create an instance of the OpenAI client
client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY_PERSONAL"])

@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="Harshit",
            markdown_description="",
            icon="https://picsum.photos/200",
        ),
        cl.ChatProfile(
            name="Chetana",
            markdown_description="",
            icon="https://picsum.photos/250",
        ),
    ]
    
@cl.on_chat_start
async def start_chat():
    model = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY_PERSONAL"], streaming=True)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a friendly assistant that answers user's question accurately",
            ),
            ("human", "{question}"),
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)

@cl.on_message
async def message(message):
    runnable = cl.user_session.get("runnable")  # type: Runnable
    msg = cl.Message(content="")
    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()