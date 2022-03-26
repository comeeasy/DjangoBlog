from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    contents = models.TextField()

    head_image = models.ImageField(upload_to="blog/images/%Y/%m/%d/", blank=True)
    attached_file = models.FileField(upload_to="blog/files/%Y/%m/%d/", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.pk}] {self.title}"

    def get_absolute_path(self):
        return f"{self.pk}"