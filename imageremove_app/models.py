# models.py
from django.db import models
from accounts_app.models import CustomUser  # Import the CustomUser model
class Image(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to the user who uploaded the image
    original = models.ImageField(upload_to='original/')
    processed = models.ImageField(upload_to='processed/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image {self.id}"