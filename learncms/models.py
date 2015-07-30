from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    banner_image = models.ImageField(upload_to='lessons')
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title


class ZoomingImage(models.Model):
    lessons = models.ManyToManyField(Lesson, related_name='zimages')
    slug = models.SlugField()
    image = models.ImageField(upload_to='zimages')
    thumbnail = ImageSpecField(source='image',
                               processors=[ResizeToFill(313, 207)],
                               format='JPEG',
                               options={'quality': 60})
    def __str__(self):
        return self.slug



class Block(models.Model):
    lesson = models.ForeignKey(Lesson)
    position = models.IntegerField(help_text='Index of this block among all blocks of a lesson')
    content = models.TextField()

    class Meta:
        ordering = ['position']