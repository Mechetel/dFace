from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ResearchView(TemplateView):
    template_name = 'researches/index.html'

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(ResearchView, self).dispatch(request, *args, **kwargs)
