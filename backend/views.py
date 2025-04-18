from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

from backend.slotutils import fetch_all_slots
from backend.utils import parse_intent_from_prompt
from django.http import HttpResponse
def home_view(request):
    return render(request, 'index.html')


@csrf_exempt
def slots_view(request):
    return fetch_all_slots()


@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt", "")

            # TODO: Replace with actual model logic
            return parse_intent_from_prompt(prompt)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # Handle non-POST requests (like OPTIONS)
    return JsonResponse({"detail": "Method not allowed"}, status=405)
