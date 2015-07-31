from django.contrib import admin
import reversion
from learncms.models import Lesson, ZoomingImage

class LessonAdmin(reversion.VersionAdmin):
    list_display = ('title',)
    prepopulated_fields = {"slug": ("title",)}

class ZoomingImageAdmin(admin.ModelAdmin):
    list_display = ('slug',)

admin.site.register(Lesson, LessonAdmin)
admin.site.register(ZoomingImage, ZoomingImageAdmin)

