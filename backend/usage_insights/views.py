from rest_framework.views import APIView
from rest_framework.response import Response

class EventIngestionView(APIView):
    def post(self, request):
        return Response({"status": "not implemented"})

class UsageDashboardView(APIView):
    def get(self, request):
        return Response({"status": "not implemented"})
