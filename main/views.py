from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .models import CCTV, History, City
from .serializers import HistorySerializer, CitySerializer
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

    def get(self, request, id, *args, **kwargs):
        try:
            history = History.objects.get(id=id)
        except History.DoesNotExist:
            raise NotFound()
        serializer = HistorySerializer(history)

        return Response(serializer.data, status=status.HTTP_200_OK)

class HistoryView(APIView):

    def get(self, request, *args, **kwargs):
        histories = History.objects.all()

        serializer = HistorySerializer(histories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class HistoryFilterByCity(APIView):
    def get(self, request, city_id, *args, **kwargs):
        city = City.objects.get(id=city_id)
        cctvs = CCTV.objects.filter(city=city)
        histories = History.objects.filter(cctv__in=cctvs)

        serializer = HistorySerializer(histories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CityView(APIView):
    def get(self, request, *args, **kwargs):
        cities = City.objects.all()

        serializer = CitySerializer(cities, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CitySpecificView(APIView):
    def get(self, request, id, *args, **kwargs):
        city = City.objects.get(id=id)

        serializer = CitySerializer(city)

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

        prediction_model.load_weights('classify_weights_tf.h5')

        model = tf.keras.Sequential([
            feature_extractor,
            tf.keras.layers.Flatten(),
            prediction_model
        ])
        batch_size = 32
        ln = 0
        ln_btch = 0
        all_batch = []
        all_frame = []
        is_anomaly = False
        while True:
            
            ret, frame = cap.read()
            if not ret:
                break

            all_frame.append(frame)
            ln += 1

            if ln == 16:
                x = preprocess_input(np.array(all_frame))
                x = np.squeeze(x)
                
                all_batch.append(x)
                ln_btch += 1

                if ln_btch == batch_size:
                    prediction = model.predict(np.array(all_batch))

                    prediction = prediction > 0.5

                    if prediction.any():
                        is_anomaly = True

                    all_batch = []
                    ln_btch = 0
                
                
                
                all_frame = []
                ln = 0

        if ln_btch > 0:
            prediction = model.predict(np.array(all_batch))

            prediction = prediction > 0.5

            if prediction.any():
                is_anomaly = True

            all_batch = []
            ln_btch = 0

        cap.release()

        os.remove('output.mp4')

        return render(request, 'main/main.html', {'is_anomaly': is_anomaly})
    return render(request, 'main/main.html')