from typing import Text, List, Optional

from rasa_sdk.forms import FormValidationAction

class ValidateReplaceCardForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_replace_card_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        updated_slots = domain_slots.copy()
        if tracker.slots.get("replacement_reason") == "damaged":
            updated_slots.remove("was_card_used_fraudulently")
        return updated_slots        
