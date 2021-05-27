from django.db import models

# Create your models here.

class City(models.Model):
    city_name = models.CharField(max_length=255)

class CCTV(models.Model):
    name = models.CharField(max_length=256)
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)

class History(models.Model):
    cctv = models.ForeignKey(CCTV, on_delete=models.CASCADE)
    anomaly_type = models.CharField(max_length=255)
    video_link = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)


