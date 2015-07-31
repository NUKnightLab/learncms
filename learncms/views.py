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
        self._resolve_zooming_image_refs(element)
        self._resolve_lesson_refs(element)
        return tostring(element,encoding='unicode')

    def _resolve_zooming_image_refs(self, element):
        for i,elem in enumerate(element.findall('.//zooming-image')):
            if elem.attrib.has_key('ref'):
                matches = ZoomingImage.objects.filter(slug=elem.attrib['ref'])
                if len(matches) == 0:
                    elem.getparent().append(Comment("Invalid slug ref for zooming-image #{}".format(i)))
                    elem.getparent().remove(elem)
                else:
                    elem.attrib['src'] = matches[0].thumbnail.url
                    elem.attrib['fullSrc'] = matches[0].image.url

    def _resolve_lesson_refs(self, element):
        for i,elem in enumerate(element.findall('.//lesson-ref')):
            if elem.attrib.has_key('ref'):
                matches = Lesson.objects.filter(slug=elem.attrib['ref'])
                if len(matches) == 0:
                    elem.getparent().append(Comment("Invalid slug ref for lesson-ref #{}".format(i)))
                    elem.getparent().remove(elem)
                else:
                    elem.attrib['image'] = matches[0].banner_image.url
                    elem.attrib['title'] = matches[0].title
                    elem.attrib['url'] = matches[0].get_absolute_url()
                    elem.text = matches[0].reference_blurb
