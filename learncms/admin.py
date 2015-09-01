from django.contrib import admin
import reversion
from learncms.models import Lesson, ZoomingImage, CapsuleUnit, GeneralImage, GlossaryTerm
from django.forms import widgets
from django import forms

from django.db import models
from filebrowser.widgets import FileInput
from filebrowser.storage import S3BotoStorageMixin
from storages.backends.s3boto import S3BotoStorage

from django.template.loader import get_template


class S3FileBrowserStorage(S3BotoStorage,S3BotoStorageMixin):
    pass

class LessonContentWidget(widgets.Widget):
    class Media:
        css = {
            'all': ('css/lesson_content_widget.css',)
        }
        js = ('js/lesson_content_widget.js',)

    def render(self, name, value, attrs=None):
        template = get_template("admin/lesson_content_widget.html")
        context = {"content":value, "name":name}
        if attrs is not None:
            context.update(attrs)
        return template.render(context=context)

class LessonForm(forms.ModelForm):
    reference_blurb = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
    content = forms.CharField(widget=LessonContentWidget())

    class Meta:
        model = Lesson
        exclude = ('created_at', 'updated_at', 'created_by', 'updated_by')

class LessonAdmin(reversion.VersionAdmin):
    def view_link(obj):
      return u"<a href='{}' target='_blank' style='word-wrap:none'><span class='ui-icon ui-icon-extlink'>View</span></a>".format(obj.get_absolute_url())

    view_link.short_description = 'View'
    view_link.allow_tags = True

    def save_model(self, request, obj, form, change):
        if obj.created_by is None:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()

    form = LessonForm
    list_display = ('title', view_link, 'slug', 'status', 'updated_at', 'updated_by')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title', 'reference_blurb', 'content']
    save_on_top = True
    formfield_overrides = {
        models.ImageField: {'widget': FileInput},
    }


class ZoomingImageAdmin(admin.ModelAdmin):
    list_display = ('slug',)

class CapsuleUnitAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title', 'reference_blurb', 'content']

class GeneralImageAdmin(admin.ModelAdmin):
    list_display = ('url', 'description')
    search_fields = ['description']

admin.site.register(Lesson, LessonAdmin)
admin.site.register(ZoomingImage, ZoomingImageAdmin)
admin.site.register(CapsuleUnit, CapsuleUnitAdmin)
admin.site.register(GeneralImage, GeneralImageAdmin)
admin.site.register(GlossaryTerm)
