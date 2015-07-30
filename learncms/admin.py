from django.contrib import admin
from learncms.models import Lesson, ZoomingImage

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {"slug": ("title",)}

class ZoomingImageAdmin(admin.ModelAdmin):
    list_display = ('slug',)

admin.site.register(Lesson, LessonAdmin)
admin.site.register(ZoomingImage, ZoomingImageAdmin)

