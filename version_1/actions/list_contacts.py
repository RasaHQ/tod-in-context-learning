from typing import Any, Dict
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from actions.db import get_contacts, add_contact, Contact


class ListContacts(Action):

    def name(self) -> str:
        return "list_contacts"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):
        contacts = get_contacts(tracker.sender_id)
        if len(contacts) > 0:
            contacts_list = "".join([f"- {c.name} ({c.handle}) \n" for c in contacts])
            return [SlotSet("contacts_list", contacts_list)]
        else:
            return [SlotSet("contacts_list", None)]
