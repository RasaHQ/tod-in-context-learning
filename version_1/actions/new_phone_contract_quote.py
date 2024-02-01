from typing import Any, Dict
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class NewPhoneContractQuote(Action):

    def name(self) -> str:
        return "new_phone_contract_quote"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):
        dispatcher.utter_message(f"I can offer you 10 Gb for $20/month.")
