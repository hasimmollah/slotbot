from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import json
import logging

from backend.prompt.utils import parse_intent_from_prompt

logger = logging.getLogger('slotbot')


class ChatView(APIView):
    def post(self, request):
        logger.debug("This is chat view.")
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt", "")
            return parse_intent_from_prompt(prompt)
        except Exception as e:
            logger.error("Error while processing request Error: %s", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
