from django.shortcuts import render
from login.utils.tools import role_client_check
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test


class Client:
    @method_decorator(user_passes_test(role_client_check()))
    def index(self, request):
        return render(request, 'frontend/actors/client/categories.html')
