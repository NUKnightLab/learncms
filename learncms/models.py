from django.db import models

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    banner_image = models.ImageField(upload_to='lessons')
    content = models.TextField(blank=True)

class Block(models.Model):
    lesson = models.ForeignKey(Lesson)
    position = models.IntegerField(help_text='Index of this block among all blocks of a lesson')
    content = models.TextField()

    class Meta:
        ordering = ['position']