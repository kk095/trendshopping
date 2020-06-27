from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
admin.site.site_header="Trend Shopping - Admin"
admin.site.site_title="Trend Shopping|admin panel"
admin.site.index_title="Welcome to Trend Shopping admin panel!"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

