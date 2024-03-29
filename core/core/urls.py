from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('website.urls')),
    path('api/', include('api.urls')),
    path('docs/', include_docs_urls(title='DLCF APP API DOCS')),
    path('dashboard/', include('dashboard.urls')),
    path('api-docs/', include('documentation.urls')),
]

# rest_framework auth
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

# Let django serve static files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
