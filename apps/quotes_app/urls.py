from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^main$', views.landing),
	url(r'^logout$', views.logout),
	url(r'^login$', views.login),
	url(r'^quotes$', views.dashboard),
	url(r'^users$', views.user_quotes),
	url(r'^users/create$', views.user_create),
	url(r'^user/favorites$', views.user_add_favorite),
	url(r'^user/favorites/remove$', views.user_remove_favorite),
	url(r'^user/submit$', views.submit_quote),
	url(r'^users/(?P<id>\d+)$', views.user_quotes),
]