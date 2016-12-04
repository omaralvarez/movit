from django.http import HttpResponse
from django.template import loader

from .models import Episode

from django.views.generic.base import TemplateView
from django.contrib import messages

#from .forms import ContactForm, FilesForm, ContactFormSet

# class HomePageView(TemplateView):
#     template_name = 'frontend/index.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(HomePageView, self).get_context_data(**kwargs)
#         latest_episode_list = Episode.objects.order_by('-dl_date')[:5]
#         context['latest_episode_list'] = latest_episode_list
#         messages.info(self.request, 'hello http://example.com')
#         return context

# class DefaultFormsetView(FormView):
#     template_name = 'frontend/formset.html'
#     form_class = ContactFormSet
#
#
# class DefaultFormView(FormView):
#     template_name = 'frontend/form.html'
#     form_class = ContactForm
#
#
# class DefaultFormByFieldView(FormView):
#     template_name = 'frontend/form_by_field.html'
#     form_class = ContactForm

def index(request):
    latest_episode_list = Episode.objects.order_by('-dl_date')[:5]
    template = loader.get_template('frontend/index.html')
    context = {
        'latest_episode_list': latest_episode_list,
    }
    return HttpResponse(template.render(context, request))

def detail_ep(request, episode_id):
    return HttpResponse("You're looking at episode %s." % episode_id)

def detail_show(request, tv_show_id):
    response = "You're looking at the results of tv show %s."
    return HttpResponse(response % tv_show_id)
