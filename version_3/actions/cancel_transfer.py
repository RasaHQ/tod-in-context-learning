from typing import Any, Dict
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ActiveLoop


class CancelTransfer(Action):

    def name(self) -> str:
        return "action_cancel_transfer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):
        return [ActiveLoop(None), 
                SlotSet("requested_slot", None),
                SlotSet("transfer_money_amount_of_money", None),
                SlotSet("transfer_money_recipient", None)]
