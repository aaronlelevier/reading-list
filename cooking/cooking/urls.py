from django.conf.urls import patterns, include, url
from django.contrib import admin

# Commented Out => because had error when changing admin.py form
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cooking.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # url(r'^books/', include('books.urls', namespace='books')),
	url('', include('books.urls', namespace='books')),

    )