import os
import logging
import json
import time
from openai import OpenAI, AssistantEventHandler
from dotenv import load_dotenv
from typing_extensions import override

# Charger les variables d'environnement
load_dotenv()

# Configurer le logger
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Vérifier si les variables sont bien chargées
api_key = os.getenv("OPENAI_API_KEY")
vector_store_id = os.getenv("VECTOR_STORE_ID")
assistant_id = os.getenv("ASSISTANT_ID")
thread_id = "thread_SNXnNSXlS3xhTvXvtt1vNk5t"  # On garde un thread fixe

instructions = (
    "It is mandatory that you only call a function if all required parameters can be inferred directly from the user's request. "
    "If any parameter is missing or ambiguous, you must first ask follow-up questions to clarify before calling the function. "
    "Strictly follow this rule."
)

# Initialiser le client OpenAI
client = OpenAI(api_key=api_key)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="envoie un mail à katia@example.com avec le sujet 'test' et le message 'bonjour'."
)



class EventHandler(AssistantEventHandler):
    @override
    def on_event(self, event):
      # Retrieve events that are denoted with 'requires_action'
      # since these will have our tool_calls
      if event.event == 'thread.run.requires_action':
        run_id = event.data.id  # Retrieve the run ID from the event data
        self.handle_requires_action(event.data, run_id)
 

    def send_email(self, tool):
        """Simule l'envoi d'un email."""
        arguments = json.loads(tool.function.arguments)
        to = arguments.get("to", "inconnu")
        subject = arguments.get("subject", "Aucun sujet")
        body = arguments.get("body", "Pas de contenu")
            
        print(f"\n📩 Envoi de l'email à {to} | Sujet: {subject} | Contenu: {body}")
        return "Email envoyé avec succès"

    def handle_requires_action(self, data, run_id):
      tool_outputs = []
        
      for tool in data.required_action.submit_tool_outputs.tool_calls:
        if tool.function.name == "send_email":
          result = self.send_email(tool)
          tool_outputs.append({"tool_call_id": tool.id, "output": result})
        elif tool.function.name == "search_invoice":
          tool_outputs.append({"tool_call_id": tool.id, "output": "facture trouvée"})
        
      # Submit all tool_outputs at the same time
      self.submit_tool_outputs(tool_outputs, run_id)


    def submit_tool_outputs(self, tool_outputs, run_id):
      # Use the submit_tool_outputs_stream helper
      with client.beta.threads.runs.submit_tool_outputs_stream(
        thread_id=self.current_run.thread_id,
        run_id=self.current_run.id,
        tool_outputs=tool_outputs,
        event_handler=EventHandler(),
      ) as stream:
        for text in stream.text_deltas:
          print(text, end="", flush=True)
        print()
 
 
with client.beta.threads.runs.stream(
  thread_id=thread.id,
  assistant_id=assistant_id,
  event_handler=EventHandler()
) as stream:
  stream.until_done()