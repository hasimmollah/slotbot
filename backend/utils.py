from backend.intents import parse_intent
from backend.slotutils import generate_save_slots
from django.http import JsonResponse
import re

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

    return company, days, duration_in_minutes


def parse_intent_from_prompt(prompt):
    # Replace with actual TinyLLaMA inference call
    """
    if "add" in prompt:
        return "🗓️ Added event to calendar!"
    elif "remove" in prompt:
        return "🗑️ Removed event from calendar."
    elif "show" in prompt or "display" in prompt:
        return "📋 Showing upcoming events."
    """
    if is_slot_add_request(prompt):
        company, days, duration_in_minutes = parse_slots_prompt(prompt)
        return generate_save_slots(company, days, duration_in_minutes)
    else:
        return JsonResponse({"response": parse_intent(prompt)})