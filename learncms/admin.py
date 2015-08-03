from django.contrib import admin
import reversion
from learncms.models import Lesson, ZoomingImage, CapsuleUnit

class LessonAdmin(reversion.VersionAdmin):
    list_display = ('title', 'slug', 'updated_at', 'updated_by')
    exclude = ('created_at', 'updated_at', 'created_by', 'updated_by')
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        if obj.created_by is None:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()    

class ZoomingImageAdmin(admin.ModelAdmin):
    list_display = ('slug',)

class CapsuleUnitAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Lesson, LessonAdmin)
admin.site.register(ZoomingImage, ZoomingImageAdmin)
admin.site.register(CapsuleUnit, CapsuleUnitAdmin)
