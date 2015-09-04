from django.conf import settings

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.views.generic.detail import DetailView
from django.http import Http404

from lxml.etree import Comment
from lxml.html import fromstring, tostring

from .models import Lesson, GlossaryTerm
from .refresolvers import evaluate_content
import os.path

# from django.forms import TextInput, Textarea
# from django.db import models

# boilerplate
from django.shortcuts import render_to_response
from django.template import RequestContext


def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

class JSONResponse(HttpResponse):
    def __init__(self,payload):
        if isinstance(payload,str):
            json_str = payload
        else:
            json_str = json.dumps(payload)
        super(JSONResponse,self).__init__(json_str,content_type="application/json")




# Create your views here.
class LessonDetailView(DetailView):

    model = Lesson
    template_name = "lesson-detail.html"

    def is_editor(self):
        return self.request.user.is_authenticated()

    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        lesson = self.object
        if (lesson.status != Lesson.PUBLISHED and not self.is_editor()):
            raise Http404
        context['title'] = lesson.title
        context['lesson'] = lesson
        elem = fromstring(lesson.content)
        evaluate_content(elem,strip_bad_references=(lesson.status == Lesson.PUBLISHED))
        context['evaluated_content'] = tostring(elem)


        context['og_title'] = lesson.title
        context['og_url'] = "{}{}".format(settings.URL_ROOT, lesson.get_absolute_url())
        context['og_image'] = "{}{}".format(settings.URL_ROOT, lesson.banner_image.url)
        context['og_description'] = lesson.reference_blurb


        return context

def glossary_json(request):
    terms = dict((gt.lemma, gt.definition) for gt in GlossaryTerm.objects.all())
    return JSONResponse(terms)
