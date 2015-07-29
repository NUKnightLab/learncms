from django.conf import settings

from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.http import Http404

from .models import Lesson

import os.path

# Create your views here.
class LessonDetailView(DetailView):

    model = Lesson
    template_name = "lesson-detail.html"

    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        context['title'] = self.object.title
        context['lesson'] = self.object
        try:
            path = os.path.join(settings.PROJECT_ROOT,'lessons',"{}.html".format(self.object.slug))
            context['content'] = open(path).read()
        except FileNotFoundError:
            raise Http404("No lesson {}".format(slug))
        return context
