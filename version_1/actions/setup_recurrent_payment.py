from datetime import datetime
from typing import List, Optional, Text, Any, Dict

from rasa.shared.nlu.training_data.message import Message
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import logging

from actions.check_restaurant_availability import duckling


logger = logging.getLogger(__name__)

def parse_datetime(text: str) -> Optional[datetime]:
    msg = Message.build(text)
    duckling.process([msg])
    if len(msg.data["entities"]) == 0:
        return None

    parsed_value = msg.data["entities"][0]["value"]
    if isinstance(parsed_value, dict):
        parsed_value = parsed_value["from"]

    return datetime.fromisoformat(parsed_value)


class ValidatePaymentStartDate(Action):
    def name(self) -> str:
        return "validate_recurrent_payment_start_date"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[EventType]:
        current_value = tracker.get_slot("recurrent_payment_start_date")
        if current_value is None:
            return []

        start_date = parse_datetime(current_value)
        start_date_timezone = start_date.tzinfo if start_date else None
        if start_date is None or (start_date and start_date < datetime.now(tz=start_date_timezone)):
            dispatcher.utter_message(response="utter_invalid_date")
            return [SlotSet("recurrent_payment_start_date", None)]

        return [SlotSet("recurrent_payment_start_date", start_date.isoformat())]


class ValidatePaymentEndDate(Action):
    def name(self) -> str:
        return "validate_recurrent_payment_end_date"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[EventType]:
        current_value = tracker.get_slot("recurrent_payment_end_date")
        if current_value is None:
            return []

        end_date = parse_datetime(current_value)
        if end_date is None:
            dispatcher.utter_message(response="utter_invalid_date")
            return [SlotSet("recurrent_payment_end_date", None)]

        start_date = tracker.get_slot("recurrent_payment_start_date")
        if start_date is not None and end_date < datetime.fromisoformat(start_date):
            dispatcher.utter_message(response="utter_invalid_date")
            return [SlotSet("recurrent_payment_end_date", None)]

        return [SlotSet("recurrent_payment_end_date", end_date.isoformat())]

class ValidateSetupRecurrentPayment(Action):
    def name(self) -> Text:
        return "validate_setup_recurrent_payment"

    async def validate_recurrent_payment_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        logger.error("validating recurrent payment type!")
        """Validate recurrent payment type value."""

        if slot_value.lower() in ["direct debit", "standing order"]:
            return {"recurrent_payment_type": slot_value}
        else:
            dispatcher.utter_message(response = "utter_categorical_slot_rejection")
            return {"recurrent_payment_type": None}

class ExecutePayment(Action):
    def name(self) -> str:
        return "action_execute_recurrent_payment"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[EventType]:
        # set-up payment logic here
        return [SlotSet("setup_recurrent_payment_successful", True)]
