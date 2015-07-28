from django.contrib import admin
from learncms.models import Lesson

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Lesson, LessonAdmin)

