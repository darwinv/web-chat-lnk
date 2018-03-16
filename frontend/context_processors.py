"""Archivo para procesar Contexto en Templates."""


def roles(request):
    """Lista de Roles de usuarios."""
    return {'ROLES': {'ROLE_ADMIN': 1, 'ROLE_CLIENT': 2, 'ROLE_SPECIALIST': 3, 'ROLE_SELLER': 4}}
