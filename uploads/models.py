# # uploads/models.py

# from django.db import models

# class ImageUpload(models.Model):
#     image = models.ImageField(upload_to='images/')

#     def __str__(self):
#         return self.image.url + " = \n" + self.image.name

# uploads/models.py
from django.db import models

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='images/')  # Uploads to AWS S3

    def __str__(self):
        return self.image.name
