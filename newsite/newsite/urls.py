from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'newsite.views.home', name='home'),
    # url(r'^newsite/', include('newsite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include('admin.site.urls')),
	url(r'^newsite/(?P<page_name>[^/]+)/edit/$', 'wiki.views.edit_page'),
	url(r'^newsite/(?P<page_name>[^/]+)/save/$', 'wiki.views.save_page'),
	url(r'^newsite/(?P<page_name>[^/]+)/$', 'wiki.views.view_page'),
)
