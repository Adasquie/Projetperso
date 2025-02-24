from openai import OpenAI
import logging
from openai import AssistantEventHandler
from typing_extensions import override
from app.ai.tools.function_calls import send_email
logger = logging.getLogger(__name__)
import json
        
class EventHandler(AssistantEventHandler):
    @override
    def __init__(self, client, thread_id, assistant_id):
        super().__init__()
        self.client = client
        self.thread_id = thread_id
        self.assistant_id = assistant_id
        self.tool_outputs = []

    def on_event(self, event):
        """Récupère les tool_calls et exécute la fonction correspondante."""
        if event.event == 'thread.run.requires_action':
            run_id = event.data.id  
            self.handle_requires_action(event.data, run_id)

    def handle_requires_action(self, data, run_id):
        
        for tool in data.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == "send_email":
                logger.info(f"📨 Tool call détecté : {tool.function.name}")
                self.tool_outputs.append(send_email(tool))
                  # 🔥 Appel direct de ta fonction depuis functions.py
            else:
                self.tool_outputs.append(None)
        # 🔥 Soumettre les résultats des tools à OpenAI
        self.submit_tool_outputs(self.tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
      # Use the submit_tool_outputs_stream helper
      with self.client.beta.threads.runs.submit_tool_outputs_stream(
        thread_id=self.current_run.thread_id,
        run_id=self.current_run.id,
        tool_outputs=tool_outputs,
        event_handler=EventHandler(self.client,self.thread_id,self.assistant_id),
      ) as stream:
        for text in stream.text_deltas:
          print(text, end="", flush=True)
        print()