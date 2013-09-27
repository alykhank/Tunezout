from django.conf.urls import patterns, url

from songs import views

urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
	url(r'^year/(?P<year>\d+)/$', views.YearView.as_view(), name='year'),
	url(r'^submit/$', views.submit, name='submit'),
)
