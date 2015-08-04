from django.conf import settings

from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.http import Http404

from lxml.etree import Comment
from lxml.html import fromstring, tostring

from .models import Lesson
from .refresolvers import REF_RESOLVERS
import os.path

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
        context['evaluated_content'] = self.evaluate_content(strip_bad_references=(lesson.status == Lesson.PUBLISHED))
        return context


    def evaluate_content(self,strip_bad_references=False):
        """Convert any convenience markup (such as object references) into the ideal markup
           for delivering to the page. Optionally remove from DOM elements which have ref 
           attributes which don't resolve to actual objects. (Do this in production but show them in draft/editing mode.)
        """
        content = self.object.content
        element = fromstring(content)
        for elem in element.findall('.//*[@ref]'):
            try:
                REF_RESOLVERS[elem.tag].resolve_ref(elem,strip_bad_references)
            except KeyError:
                self.note_error(elem,"Unrecognized ref type", strip_bad_references)

        return tostring(element,encoding='unicode')

