from django.conf.urls import patterns, url

from songs import views

urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
	url(r'^genre/(?P<genre>\d+)/$', views.GenreView.as_view(), name='genre'),
	url(r'^year/(?P<year>\d+)/$', views.YearView.as_view(), name='year'),
	url(r'^submit/$', views.submit, name='submit'),
	url(r'^rate/(?P<pk>\d+)/(?P<rating>\d)/(?P<genre>\d+)/$', views.rate, name='rate'),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^register/$', views.register, name='register'),
	url(r'^twitter/login/$', views.twitter_login, name='twitter_login'),
	url(r'^twitter/success/$', views.twitter_success, name='twitter_success'),
)
