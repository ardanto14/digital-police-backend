from django.shortcuts import render
from rest_framework.views import APIView
from .models import History
from .serializers import HistorySerializer
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status

class HistoryView(APIView):

    # 1. List all
    def get(self, request, id, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        try:
            history = History.objects.get(id=id)
        except History.DoesNotExist:
            raise NotFound()
        serializer = HistorySerializer(history)

        return Response(serializer.data, status=status.HTTP_200_OK)

# TODO
class VideoView(APIView):
    pass