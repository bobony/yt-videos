from django.conf import settings

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
   (r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
    url(r'^$', 'cfe.views.cfevideos', name='videos'),
   	url(r'^videos/(?P<id>.*)$', 'playlist.views.plist_items', name='plist_items'),
    url(r'^admin/', include(admin.site.urls)),
)
