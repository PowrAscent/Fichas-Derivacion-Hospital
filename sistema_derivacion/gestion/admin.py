from django.contrib import admin

from gestion.models import HistorialModificacion
from django.utils.html import format_html
from django.urls import reverse
@admin.register(HistorialModificacion)
class HistorialModificacionAdmin(admin.ModelAdmin):


    list_display = (
        'derivacion_link',
        'usuario_modificador',
        'fecha_modificacion',
        )


    readonly_fields = ('derivacion', 'usuario_modificador', 'fecha_modificacion')
    ordering = ['-fecha_modificacion']

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


    def derivacion_link(self, obj):
        try:
            # Construye el enlace de edición para la Derivacion
            url = reverse('admin:gestion_derivacion_change', args=[obj.derivacion.id])
            return format_html('<a href="{}">Ficha #{}</a>', url, obj.derivacion.id)
        except:
            return f'Ficha #{obj.derivacion.id}'

    derivacion_link.short_description = 'ID Ficha'