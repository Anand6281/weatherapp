from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path('', include('apps.main.urls')),
    path('account/', include('apps.users.urls')),
    path('admin/', admin.site.urls),
]


# Serve static and media files
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT,
    }),
]

# admin.site.enable_nav_sidebar = False 
admin.site.site_header = "JojMo Dashboard"
admin.site.site_title = "JojMo Admin Portal"
# admin.site.index_title = "JojMo | Dashboard"