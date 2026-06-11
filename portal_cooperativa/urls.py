from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cooperados/', include('cooperados.urls')),
    path('', include('autenticacao.urls')),
]
