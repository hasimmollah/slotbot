from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import logging

from backend.models import InterviewSlot
from backend.slot.slotutils import fetch_all_slots, delete_slot


logger = logging.getLogger('slotbot')


class SlotListView(APIView):
    def get(self, request):
        logger.debug("This is slots view.")
        return fetch_all_slots()

class SlotDetailView(APIView):
    def delete(self, request, slot_id):
        logger.debug("This is delete view.")
        try:
            return delete_slot(slot_id)
        except InterviewSlot.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
