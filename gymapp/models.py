from django.db import models

class Program(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='program_images/')

    def __str__(self):
        return self.title

# Create your models here.
