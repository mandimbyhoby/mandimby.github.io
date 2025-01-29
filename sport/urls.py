from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gymapp.urls')),        # URL pour l'application gym
    path('', include('contactapp.urls')), # URL pour l'application contact
    path('', include('schedulesapp.urls')),
    path('favicon.ico', lambda request: HttpResponse(status=204)),  # No Content
    path('', include('classapp.urls')),
    #path('', include('register_user.urls')),
      # URL pour l'application schedules
    # path('classes/', include('classapp.urls')),  # Décommente si tu as une application 'classapp'
]

# Activer la gestion des fichiers médias en mode DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
