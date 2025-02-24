from openai import OpenAI
import os
from dotenv import load_dotenv

# Initialisation du client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

new_thread = client.beta.threads.create()

# Lister toutes les méthodes disponibles
message = client.beta.threads.messages.create(
  thread_id=new_thread.id,
  role="user",
  content="Alexandre a déjà travaillé pour google ?"
)

print(message)

run = client.beta.threads.runs.create_and_poll(
  thread_id=new_thread.id,
  assistant_id="asst_99mJpGIHpflRxtEOi6CKlrPa",
  instructions="Réponds uniquement en français"
)

if run.status == 'completed': 
  messages = client.beta.threads.messages.list(
    thread_id=new_thread.id
  )
  print(messages)
else:
  print(run.status)