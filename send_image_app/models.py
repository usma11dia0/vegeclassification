from django.db import models

class ModelFile(models.Model):
    image = models.ImageField(upload_to='documents/')