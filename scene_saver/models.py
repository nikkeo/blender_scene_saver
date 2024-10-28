from django.db import models


class ScaneSaverInfo(models.Model):
    username = models.CharField(max_length=100)
    save_time = models.DateTimeField()
    file_path = models.TextField()

    def __str__(self):
        return f"{self.username} - {self.save_time}"
