from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from views.home import home, create, board_state, destroy


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chess.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^game/(?P<game_id>[0-9]+)/move/(?P<move_index>[0-9]+)$', board_state),
    url(r'^$', home),
    url(r'^create$', create),
    url(r'^destroy', destroy),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
