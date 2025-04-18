from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import logging

from backend.slot.slotutils import fetch_all_slots
from backend.prompt.utils import parse_intent_from_prompt

logger = logging.getLogger('slotbot')

def home_view(request):
    return render(request, 'index.html')


@csrf_exempt
def slots_view(request):
    logger.debug("This is slots view.")
    return fetch_all_slots()


@csrf_exempt
def chat_view(request):
    logger.debug("This is chat view.")
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt", "")
            return parse_intent_from_prompt(prompt)
        except Exception as e:
            logger.error("Error while processing request Error: %s", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    # Handle non-POST requests (like OPTIONS)
    return JsonResponse({"detail": "Method not allowed"}, status=405)
