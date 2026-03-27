import os

from openai import AzureOpenAI
from pydantic import BaseModel


client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)


# response format
class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

# call model
completion = client.beta.chat.completions.parse(
    model=os.getenv("AZURE_GPT4O_MINI_DEPLOYMENT"),
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday.",
        },
    ],
    response_format=CalendarEvent,
)

# Parse the response
event = completion.choices[0].message.parsed
event.name
event.date
event.participants