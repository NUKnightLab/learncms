"""learncms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.views.generic.list import ListView
from django.views.generic import RedirectView
from django.views.generic.base import TemplateView

from .models import Lesson
from .views import LessonDetailView, HomepageView, glossary_json, lesson_json, handler404, handler500

admin.site.site_header = "Learn.KnightLab.com admin"

from filebrowser.sites import site
from grappelli import urls as grapelli_urls
from os.path import abspath, dirname, join, normpath

urlpatterns = patterns(
    '',
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include(grapelli_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^lesson/(?P<slug>[a-z\-]+)/$', LessonDetailView.as_view(), name='lesson-detail'),
    url(r'^glossary.json$', glossary_json, name='glossary-json'),
    url(r'^lesson.json$', lesson_json, name='lesson-json'),
    url(r'^index.html?$', RedirectView.as_view(url='/', permanent=True), name='index_html'),
    url(r'^404(.html|/)?$', TemplateView.as_view(template_name="404.html"), name='show-404'),
    url(r'^500(.html|/)?$', TemplateView.as_view(template_name="500.html"), name='show-500'),
    url(r'^/?$', HomepageView.as_view(), name='homepage'),
)

# these only work if the URL does not have a protocol (i.e. local)
# otherwise, Django will save us
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# these two need to be managed with nginx in AWS.
urlpatterns += static(settings.FILEBROWSER_URL, document_root=settings.FILEBROWSER_ROOT)
urlpatterns += static('/legacy/', document_root=normpath(join(settings.PROJECT_ROOT, 'legacy')))
