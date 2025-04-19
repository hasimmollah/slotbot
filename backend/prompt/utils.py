from backend.ai.intents import parse_intent
from backend.slot.slotutils import generate_save_slots, confirmed_slot
from django.http import JsonResponse
from datetime import datetime
import re
import logging

logger = logging.getLogger('slotbot')

def extract_days(prompt: str) -> int:
    match = re.search(r"(\d+)\s+day[s]?", prompt)
    if match:
        return int(match.group(1))
    return 7

def extract_company_name(prompt: str) -> str:
    # Try to extract between "for" and "for X days"
    match = re.search(r"for\s+([a-zA-Z0-9_]+)(?:\s+for\s+\d+\s+days)?", prompt)
    if match:
        return match.group(1)
    return "unknown"

def is_slot_add_request(prompt: str) -> bool:
    keywords = ["available slots", "interview slots", "show slots", "meeting slots"]
    return any(kw in prompt.lower() for kw in keywords)

def is_slot_confirmed_request(prompt: str) -> bool:
    keywords = ["confirmed slot", "Confirmed slot", "Slot confirmed", "slot confirmed"]
    return any(kw in prompt.lower() for kw in keywords)

def parse_slots_prompt(prompt: str):
    # Extracting company, days, and duration
    company_match = re.search(r"for\s+([a-zA-Z0-9_]+)(?:\s+for\s+\d+\s+days)?", prompt)
    days_match = re.search(r"for\s+(\d+)\s+day[s]?", prompt)
    duration_match = re.search(r"for\s+duration\s+(\d{1,2}):(\d{2})\s+hours", prompt)

    company = company_match.group(1) if company_match else "unknown"
    days = int(days_match.group(1)) if days_match else 7  # Default to 7 days if not found
    duration_hours = int(duration_match.group(1)) if duration_match else 1  # Default to 1 hour if not found
    duration_minutes = int(duration_match.group(2)) if duration_match else 0  # Default to 0 minutes if not found

    duration_in_minutes = (duration_hours * 60) + duration_minutes
    logger.info("Company :  %s , days : %s , duration hours : %d , duration minutes : %d ", company, days, duration_hours, duration_minutes)

    return company, days, duration_in_minutes

def parse_confirmed_slot_prompt(prompt):
    pattern = r"(?:[Cc]onfirmed\s*slot|[Ss]lot\s*confirmed) for (\w+) on (\d{2}-\d{2}-\d{4}) at (\d{2}:\d{2} (?:AM|PM)) - (\d{2}:\d{2} (?:AM|PM))"
    match = re.search(pattern, prompt)
    if match:
        company_name = match.group(1)
        date_str = match.group(2)
        start_time_str = match.group(3)
        end_time_str = match.group(4)

        # Parse the date and time into Python objects
        date_obj = datetime.strptime(date_str, "%d-%m-%Y").date()
        start_time_obj = datetime.strptime(start_time_str, "%I:%M %p").time()
        end_time_obj = datetime.strptime(end_time_str, "%I:%M %p").time()
        return company_name, date_obj, start_time_obj, end_time_obj
    else:
        logger.info("No match found.")
        return None, None, None, None


def parse_intent_from_prompt(prompt):
    if is_slot_add_request(prompt):
        company, days, duration_in_minutes = parse_slots_prompt(prompt)
        return generate_save_slots(company, days, duration_in_minutes)
    elif is_slot_confirmed_request(prompt):
        company_name, date_obj, start_time_obj, end_time_obj = parse_confirmed_slot_prompt(prompt)
        return confirmed_slot(company_name, date_obj, start_time_obj, end_time_obj)

    else:
        return JsonResponse({"response": parse_intent(prompt)})