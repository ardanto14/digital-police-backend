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
from firebase_admin import storage
import uuid
import json
import datetime
from django.utils import timezone

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
        histories = History.objects.all().order_by('-created_at')

        serializer = HistorySerializer(histories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class HistoryTodayView(APIView):

    def get(self, request, *args, **kwargs):
        today = datetime.date.today() 
        histories = History.objects.filter(created_at__gt=today)

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


class TokenPostView(APIView):

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        device = FCMDevice.objects.filter(registration_id=body['token'])

        if not device:
            FCMDevice.objects.create(registration_id=body['token'], type='android', name=str(uuid.uuid1()))
            created = True
        else:
            created = False

        if created:
            statuss = 'created'
        else:
            statuss = 'not created'

        return Response({"status": statuss}, status=status.HTTP_200_OK)


        



# TODO
class VideoView(APIView):
    def get(self, request, *args, **kwargs):
        
        devices = FCMDevice.objects.all()

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

        if is_anomaly:

            history = History()
            history.anomaly_type = 'ANOMALY'
            dummy_cctv = CCTV.objects.filter(name='dummy')
            if not dummy_cctv:
                cctv = CCTV()
                cctv.name = 'dummy'
                cctv.latitude = 0
                cctv.longitude = 0

                dummy_city = City.objects.filter(city_name='dummy')

                if not dummy_city:
                    city = City()
                    city.city_name = 'dummy'
                    city.save()

                    dummy_city = city
                else:
                    dummy_city = dummy_city.first()

                cctv.city = dummy_city
                cctv.save()

                dummy_cctv = cctv

            else:
                dummy_cctv = dummy_cctv.first()

            history.cctv = dummy_cctv

            # history.video_link = 'https://google.com/'

            file_uuid = uuid.uuid1()

            bucket = storage.bucket()
            blob = bucket.blob(str(file_uuid) + '.mp4')

            blob.upload_from_filename('output.mp4')

            blob.make_public()

            history.video_link = blob.public_url

            # history.video_link = 'test.com'

            history.save()


            print(timezone.localtime(history.created_at))
            devices = FCMDevice.objects.all()
            devices.send_message(title="Crime detected", body="Crime detected at CCTV {} in {} at {}".format(history.cctv.name, history.cctv.city.city_name, timezone.localtime(history.created_at)), data={'historyId': history.id})

            

        os.remove('output.mp4')

        return render(request, 'main/main.html', {'is_anomaly': is_anomaly})
    return render(request, 'main/main.html')