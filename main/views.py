from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .models import History
from .serializers import HistorySerializer
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from fcm_django.models import FCMDevice
import cv2

class HistorySpecificView(APIView):

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

class HistoryView(APIView):

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''

        history = History.objects.all()

        serializer = HistorySerializer(history, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# TODO
class VideoView(APIView):
    def get(self, request, *args, **kwargs):
        
        devices = FCMDevice.objects.all()

        print(devices)

        devices.send_message(title="Title", body="Message")

        return Response()

def video_view(request):
    if request.method == 'POST':
        vid = request.POST['video']
        cap = cv2.VideoCapture(vid)

        print(type(vid))

        return redirect('main')
    return render(request, 'main/main.html')