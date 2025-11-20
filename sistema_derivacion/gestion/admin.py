from django.contrib import admin
from django.contrib.auth.hashers import make_password
from gestion.models import HistorialModificacion
from gestion.models import Usuario
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


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('correo', 'nombre', 'rol')
    list_filter = ('rol',)
    search_fields = ('correo', 'nombre')

    fieldsets = (
        (None, {'fields': ('correo', 'nombre', 'contraseña', 'rol')}),
    )


    def save_model(self, request, obj, form, change):

        if obj.pk:
            try:
                original_obj = Usuario.objects.get(pk=obj.pk)
                old_password = original_obj.contraseña
            except Usuario.DoesNotExist:
                old_password = None
        else:
            old_password = None


        if obj.contraseña != old_password and not obj.contraseña.startswith('pbkdf2_sha256$'):


            obj.contraseña = make_password(obj.contraseña)


        super().save_model(request, obj, form, change)