from django.conf import settings

from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.http import Http404

from django.template import Template, Context

from .models import Lesson

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
        context['zimages'] = dict((z.slug, z) for z in lesson.zimages.all())
        t = Template(lesson.content)
        context['evaluated_content'] = t.render(Context(context))
        return context
