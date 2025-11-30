"""
URL configuration for task_analyzer project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.views.static import serve
from pathlib import Path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]

# Serve frontend static files in development
if settings.DEBUG:
    frontend_dir = Path(settings.BASE_DIR.parent) / 'frontend'
    urlpatterns += [
        path('styles.css', serve, {'document_root': str(frontend_dir), 'path': 'styles.css'}),
        path('script.js', serve, {'document_root': str(frontend_dir), 'path': 'script.js'}),
    ]

