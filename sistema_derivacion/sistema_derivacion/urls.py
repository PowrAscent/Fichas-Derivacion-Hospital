from django.contrib import admin
from django.urls import path
from gestion import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path ('logout/', views.logout),
    path('', views.login),
    path('panel/', views.panel),
    path('registrar/', views.registrar),
    path('modificar/<int:id>/', views.modificar),
    path('listar/', views.listar),
    path('derivacion/<int:id>/detalle/', views.detalle_derivacion),
    path('pacientes/', views.listar_pacientes),
    path('paciente/<int:id>/historial/', views.historial_derivaciones),
]
