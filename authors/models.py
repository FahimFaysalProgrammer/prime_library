from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    phone_no = models.CharField(max_length=11)
    email = models.EmailField(blank = True, null = True, verbose_name = 'Contact Email (Optional)')

    def __str__(self):
        return self.name