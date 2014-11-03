from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from views.home import home


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chess.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', home),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
