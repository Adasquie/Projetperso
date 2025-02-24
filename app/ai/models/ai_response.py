from dataclasses import dataclass
from typing import Optional

@dataclass
class AIResponse:
    action: str
    reponse: str
    raison: Optional[str] = None

    def to_dict(self):
        return {
            'action': self.action,
            'reponse': self.reponse,
            'raison': self.raison
        }

    @classmethod
    def from_assistant_response(cls, response: str):
        if "perso" in response.lower():
            return cls(
                action="ignorer",
                raison="Email personnel"
            )
        return cls(
            action="répondre",
            reponse=response
        ) 