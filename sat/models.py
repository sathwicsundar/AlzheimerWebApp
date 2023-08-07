from django.db import models

# Create your models here.
class Question(models.Model):
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    def __str__(self):
        return self.image.name