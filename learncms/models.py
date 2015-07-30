from django.db import models
from django.core.urlresolvers import reverse

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text="Don't edit this, let it be automatically assigned. Must be unique.")
    banner_image = models.ImageField(upload_to='lessons')
    reference_blurb = models.CharField(max_length=500, blank=True, help_text="The text which appears when a reference to this lesson is included in some other. Don't use markup.")
    content = models.TextField(blank=True,help_text="The body of the lesson, marked up with web component magic.")

    def get_absolute_url(self):
        return reverse('lesson-detail', args=(self.slug,))

    def __str__(self):
        return self.title


class ZoomingImage(models.Model):
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='zimages')
    thumbnail = ImageSpecField(source='image',
                               processors=[ResizeToFill(313, 207)],
                               format='JPEG',
                               options={'quality': 60})

    def get_absolute_url(self):
        return self.image.url


    def __str__(self):
        return self.slug
