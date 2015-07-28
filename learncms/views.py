from django.conf import settings

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import Http404

import os.path

# Create your views here.
class LessonView(TemplateView):
    template_name = "lesson.html"

    def get_context_data(self, slug, **kwargs):
        context = super(LessonView, self).get_context_data(**kwargs)
        try:
            path = os.path.join(settings.PROJECT_ROOT,'lessons',"{}.html".format(slug))
            context['content'] = open(path).read()
        except FileNotFoundError:
            raise Http404("No lesson {}".format(slug))
        return context
