from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /frontend/
    #url(r'^$', views.HomePageView.as_view(), name='home'),
    # url(r'^formset$', DefaultFormsetView.as_view(), name='formset_default'),
    # url(r'^form$', DefaultFormView.as_view(), name='form_default'),
    # url(r'^form_by_field$', DefaultFormByFieldView.as_view(), name='form_by_field'),
    url(r'^$', views.index, name='index'),
    # ex: /frontend/tvshow/5/
    url(r'^tvshow/(?P<tv_show_id>[0-9]+)/$', views.detail_show, name='detail tv show'),
    # ex: /frontend/5/results/
    url(r'^episode/(?P<episode_id>[0-9]+)/$', views.detail_ep, name='detail episode'),
]
