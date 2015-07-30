from django.contrib import admin
from learncms.models import Lesson, ZoomingImage

class ZoomingImageInline(admin.TabularInline):
    model = ZoomingImage.lessons.through

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ ZoomingImageInline ]

class ZoomingImageAdmin(admin.ModelAdmin):
    inlines = [ ZoomingImageInline ]    
    exclude = ('lesson', )

admin.site.register(Lesson, LessonAdmin)
admin.site.register(ZoomingImage, ZoomingImageAdmin)

