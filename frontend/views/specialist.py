from django.shortcuts import render
from login.utils.tools import role_specialist_check
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

class Specialist:
    @method_decorator(user_passes_test(role_specialist_check()))
    def index(self, request):
        return render(request, 'frontend/actors/specialist/index.html')