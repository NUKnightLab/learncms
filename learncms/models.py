from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class Lesson(models.Model):
    PUBLISHED = 'published'
    DRAFT = 'draft'
    LESSON_STATUS_CHOICES = (
        (PUBLISHED,'Published'), # value, label
        (DRAFT, 'Draft'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text="Don't edit this, let it be automatically assigned. Must be unique.")
    banner_image = models.ImageField(upload_to='lessons')
    status = models.CharField(choices=LESSON_STATUS_CHOICES, default=DRAFT, max_length=50)
    reference_blurb = models.CharField(max_length=500, blank=True, help_text="The text which appears when a reference to this lesson is included in some other. Don't use markup.")
    content = models.TextField(blank=True,help_text="The body of the lesson, marked up with web component magic.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True, blank=True, related_name='creator')
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name='updater')


    def get_absolute_url(self):
        return reverse('lesson-detail', args=(self.slug,))

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


    def __str__(self):
        return self.title


class ZoomingImage(models.Model):
    slug = models.SlugField(unique=True, help_text="You choose. Lowercase letters and numbers and - characters only please.")
    image = models.ImageField(upload_to='zimages',help_text="Upload the full-size version of the image. The system will create the thumbnail.")
    thumbnail = ImageSpecField(source='image',
                               processors=[ResizeToFill(313, 207)],
                               format='JPEG',
                               options={'quality': 60})

    def get_absolute_url(self):
        return self.image.url


    def __str__(self):
        return self.slug

class CapsuleUnit(models.Model):
    title = models.CharField(max_length=200, help_text="")
    slug = models.SlugField(unique=True, help_text="Don't edit this, let it be automatically assigned. Must be unique.")
    image = models.ImageField(upload_to='capsules')
    content = models.TextField(blank=True, help_text="HTML is OK")

    def __str__(self):
        return self.title
