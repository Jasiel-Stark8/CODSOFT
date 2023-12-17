"""Assistants Module"""

import os
import asyncio
from pathlib import Path
from openai import AsyncOpenAI
client = AsyncOpenAI(api_key="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")

async def assistant_reponse():
    """Assistant Response"""
    assistant = await client.beta.assistants.create(
        name="Math Tutor",
        instructions="You are a personal math tutor. Write and run code to answer math questions.",
        tools=[ { "type" : "code_interpreter"}, { "type" : "retrieval"} ],
        model="gpt-3.5-turbo-1106"
    )

    thread = await client.beta.threads.create()
    # print(thread)

    messages = await client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
    )

    # print(message)

    run = await client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id=assistant.id
    )

    run = await client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

    messages = await client.beta.threads.messages.list(
        thread_id=thread.id
    )

    for message in reversed(messages.data):
        print(message.role + ":" + message.content[0].text.value)




    # File Upload feature

    file = await client.files.create(
        file=Path("gpt-4.pdf"),
        purpose="assistants"
    )

    # print(file)

    assistant = await client.beta.assistants.create(
        name="Machine Learning Researcher",
        instructions="You are a Machine Learning researcher, \
                    answer all questions on the research paper \
                    you will use your memory to answer questions",
        tools=[ {"type": "code_interpreter"}, {"type": "retrieval"} ],
        model="gpt-3.5-turbo-1106",
        file_ids=[file.id]
    )
    # print(assistant.file_ids)

    thread = await client.beta.threads.create()
    # print(thread)

    messages = await client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="How large is GPTs training data?"
    )

    run = await client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    run = await client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

    messages = await client.beta.threads.messages.list(
        thread_id=thread.id
    )
    return messages

async def main():
    """Await response"""
    messages = await assistant_reponse()
    for message in reversed(messages.data):
        print(message.role + ":" + message.content[0].text.value)

asyncio.run(main())
