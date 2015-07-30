from django.conf import settings

from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.http import Http404

from lxml.etree import Comment
from lxml.html import fromstring, tostring

from .models import Lesson, ZoomingImage
import os.path

# Create your views here.
class LessonDetailView(DetailView):

    model = Lesson
    template_name = "lesson-detail.html"

    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        lesson = self.object
        context['title'] = lesson.title
        context['lesson'] = lesson
        context['evaluated_content'] = self.evaluate_content()
        return context

    def evaluate_content(self):
        """Convert any convenience markup (such as object references) into the ideal markup
           for delivering to the page.
        """
        content = self.object.content
        element = fromstring(content)
        self._resolve_zooming_images(element)
        return tostring(element,encoding='unicode')

    def _resolve_zooming_images(self, element):
        for i,zi in enumerate(element.findall('.//zooming-image')):
            if zi.attrib.has_key('ref'):
                matches = ZoomingImage.objects.filter(slug=zi.attrib['ref'])
                if len(matches) == 0:
                    zi.getparent().append(Comment("Invalid slug ref for zooming-image #{}".format(i)))
                    zi.getparent().remove(zi)
                else:
                    zi.attrib['src'] = matches[0].thumbnail.url
                    zi.attrib['fullSrc'] = matches[0].image.url

