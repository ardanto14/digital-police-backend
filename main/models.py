from django.db import models

# Create your models here.
class CCTV(models.Model):
    name = models.CharField(max_length=256)
    latitude = models.IntegerField()
    longitude = models.IntegerField()


class History(models.Model):
    id_cctv = models.ForeignKey(CCTV, on_delete=models.CASCADE)
    anomaly_type = models.IntegerField()
    video_link = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)