from openai import OpenAI
from dotenv import load_dotenv
import os

def chatBot(message:str, account):
  load_dotenv()

  client = OpenAI(
    api_key=os.getenv("API_KEY")
  )

  completion = client.chat.completions.create(
    model="ft:gpt-4o-mini-2024-07-18:matcron:matcron-model:B8Xhh4sa",
    store=True,
    messages=[
      {"role": "user", "content": message}
    ],
    user=account
  )

  return completion.choices[0].message.content
