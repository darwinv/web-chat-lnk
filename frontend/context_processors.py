"""Archivo para procesar Contexto en Templates."""


def roles(request):
    """Lista de Roles de usuarios."""
    return {'ROLES': {'admin': 1, 'client': 2, 'specialist': 3, 'seller': 4}}
