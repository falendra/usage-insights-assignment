from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EventPayloadSerializer
from .services.event_service import EventService

class EventIngestionView(APIView):
    def post(self, request):
        serializer = EventPayloadSerializer(data=request.data)
        if serializer.is_valid():
            try:
                EventService.process_event(serializer.validated_data)
                return Response({"status": "success"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                # Catch integrity errors like foreign key constraints
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsageDashboardView(APIView):
    def get(self, request):
        return Response({"status": "not implemented"})
