from django.conf.urls import patterns, url

from books import views

urlpatterns = patterns('',
	# ex: /books/
	url(r'^$', views.index, name='index'),
	# ex: /books/5/
	url(r'^detail/(?P<book_requested>(\w+\-)*\w+)/$', views.detail, name='detail'),

	url(r'^edit_a_book/(?P<book_requested>(\w+\-)*\w+)/$', views.edit_a_book, name='edit_a_book'),

	url(r'^book_list/$', views.book_list, name='book_list'),

	url(r'^contact/$', views.contact, name='contact'),

	url(r'^thanks/$', views.thanks, name='thanks'),

	url(r'^profile/$', views.profile, name='profile'),

	url(r'^logout/$', views.logout, name='logout'),

	url(r'^loggedout/$', views.loggedout, name='loggedout'),

	url(r'^login/$', views.login_view, name='login_view'),

	url(r'^loggedin/$', views.loggedin, name='loggedin'),

	url(r'^loginfail/$', views.loginfail, name='loginfail'),

	url(r'^create/account/$', views.createUser, name='createUser'),

	url(r'^profile_update/$', views.updated, name='updated'),

	url(r'^book_updated/$', views.book_updated, name='book_updated'),

	url(r'^reset_password/$', views.reset_password, name='reset_password'),

	url(r'^change_password/$', views.change_password, name='change_password'),

	url(r'^password_updated/$', views.password_updated, name='password_updated'),

	url(r'^email_sent/$', views.email_sent, name='email_sent'),

	url(r'^take_notes/$', views.take_notes, name='take_notes'),

	url(r'^take_specific_notes/(?P<book_id>\d+)$', views.take_specific_notes, name='take_specific_notes'),

	url(r'^add_a_book/$', views.add_a_book, name='add_a_book'),

	url(r'^mission/$', views.mission, name='mission'),

	url(r'^search_results/$', views.search_results, name='search_results'),

	)
