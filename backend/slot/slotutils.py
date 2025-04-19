import logging
from datetime import datetime, timedelta, time

from rest_framework import status
from rest_framework.response import Response

from django.http import JsonResponse

from backend.models import InterviewSlot
from typing import List

logger = logging.getLogger('slotbot')

def format_slots(slots: List[InterviewSlot]) -> List[dict]:
    formatted_slots = [
        {
            'id' : slot.id,
            'company': slot.company,
            'date': slot.date.strftime("%Y-%m-%d"),  # Ensure date is a string
            'start': slot.start_time.strftime('%H:%M'),  # Format time
            'end': slot.end_time.strftime('%H:%M'),
        }
        for slot in slots
    ]
    logger.info(formatted_slots)
    # Return the formatted data in the JSON response
    return formatted_slots

def fetch_all_slots():
    slots = InterviewSlot.objects.all()
    logger.info("Count of slots : %d ", slots.count())
    return Response({"response_type": "slots", "slots": format_slots(slots)}, status=status.HTTP_200_OK)


def delete_slot(slot_id: int):
    logger.info("Deleting slot with id : %d ", slot_id)
    slot = InterviewSlot.objects.get(id=slot_id)
    slot.delete()
    return Response( status=status.HTTP_204_NO_CONTENT)

def generate_save_slots(company_name: str = "", days: int = 7, duration_in_minutes: int = 60):
    slots = generate_slots(company_name, days, duration_in_minutes)
    created_slots = save_slots(slots)
    return Response({"response_type": "slots", "slots": format_slots(created_slots)}, status=status.HTTP_200_OK)


def save_slots(slots):
    return InterviewSlot.objects.bulk_create(slots)

def confirmed_slot(company_name, date_obj, start_time_obj, end_time_obj):
    InterviewSlot.objects.filter(
        company=company_name,
        date=date_obj,
        start_time=start_time_obj,
        end_time=end_time_obj
    ).update(is_booked=True)
    InterviewSlot.objects.filter(
        company=company_name,
        is_booked=False
    ).delete()
    return Response({"response_type": "slot_confirmed", "slots": format_slots(InterviewSlot.objects.all()) , "response": "slot confirmed successfully"}, status=status.HTTP_200_OK)

def generate_slots(company_name: str = "", days: int = 7, duration_in_minutes: int = 60, daily_limit: int = 3, start_date: str = None):
    slots = []
    date = datetime.strptime(start_date, "%d-%m-%Y") if start_date else datetime.today()
    AVAILABLE_HOURS = [8, 9, 10, 11, 13, 14, 16, 17]

    for i in range(days):
        current_day = date + timedelta(days=i)
        if current_day.weekday() >= 5:  # Skip weekends
            continue

        taken_slots = InterviewSlot.objects.filter(date=current_day.date())
        taken_time_ranges = [
            (slot.start_time, slot.end_time)
            for slot in taken_slots
        ]
        used_hours = set(slot.start_time.hour for slot in taken_slots)

        selected_hours = []
        for hour in AVAILABLE_HOURS:
            start_time = time(hour, 0)
            end_time = (datetime.combine(current_day.date(), start_time) + timedelta(minutes=duration_in_minutes)).time()
            overlap = any(
                start_time < existing_end and end_time > existing_start
                for existing_start, existing_end in taken_time_ranges
            )
            if len(selected_hours) >= daily_limit:
                break
            if overlap:
                continue
            if hour in used_hours:
                continue
            if selected_hours and abs(hour - selected_hours[-1]) == 1:
                continue  # avoid consecutive if possible
            selected_hours.append(hour)

        if len(selected_hours) < daily_limit:
            for hour in AVAILABLE_HOURS:
                start_time = time(hour, 0)
                end_time = (datetime.combine(current_day.date(), start_time) + timedelta(minutes=duration_in_minutes)).time()
                overlap = any(
                    start_time < existing_end and end_time > existing_start
                    for existing_start, existing_end in taken_time_ranges
                )
                if overlap:
                    continue
                if hour in used_hours or hour in selected_hours:
                    continue
                selected_hours.append(hour)
                if len(selected_hours) >= daily_limit:
                    break

        for hour in selected_hours:
            start = time(hour=hour, minute=0)
            end = (datetime.combine(current_day.date(), start) + timedelta(minutes=duration_in_minutes)).time()
            slots.append(InterviewSlot(
                company=company_name,
                date=current_day.date(),
                start_time=start,
                end_time=end
            ))
    return slots