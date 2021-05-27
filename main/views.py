from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .models import History
from .serializers import HistorySerializer
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from fcm_django.models import FCMDevice
import cv2
import os
from .c3d import C3D
from tensorflow.keras import Model
from .sports1M_utils import preprocess_input
import numpy as np
import tensorflow as tf

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
        vid = request.FILES.get('video', None).read()
        # print(vid)
        f = open('output.mp4', 'wb')
        f.write(vid)
        f.close()
        cap = cv2.VideoCapture('output.mp4')

        all_frame = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            all_frame.append(frame)
        cap.release()

        ln = len(all_frame)
        
        base_model = C3D(weights='sports1M')
        feature_extractor = Model(inputs=base_model.input, outputs=base_model.get_layer('fc6').output)


        prediction_model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(4096,)),
            tf.keras.layers.Dropout(0.6),
            tf.keras.layers.Dense(512, kernel_initializer='glorot_normal', kernel_regularizer=tf.keras.regularizers.L2(0.001), activation='relu'),
            tf.keras.layers.Dropout(0.6),
            tf.keras.layers.Dense(32, kernel_initializer='glorot_normal', kernel_regularizer=tf.keras.regularizers.L2(0.001)),
            tf.keras.layers.Dropout(0.6),
            tf.keras.layers.Dense(1, kernel_initializer='glorot_normal', kernel_regularizer=tf.keras.regularizers.L2(0.001), activation='sigmoid'),
        ])

        prediction_model.load_weights('test_model.h5')

        model = tf.keras.Sequential([
            feature_extractor,
            tf.keras.layers.Flatten(),
            prediction_model
        ])

        # Select 16 frames from video
        start = 0
        is_anomaly = False
        while True:
            if start + 16 > ln:
                break

            vid = np.array(all_frame[start:start+16])
            start += 16

            x = preprocess_input(vid)

            features = model.predict(x)

            if features[0][0] > 0.5:
                is_anomaly = True
                break
            print(features)


        os.remove('output.mp4')

        return render(request, 'main/main.html', {'is_anomaly': is_anomaly})
    return render(request, 'main/main.html')