
from django.shortcuts import render
from frontend.forms import ContactForm

class Client:
    def contact(self, request):
        form = ContactForm()
        return render(request, 'frontend/actors/client/contact.html', {'form': form})

class Specialist:
    def contact(self, request):
        form = ContactForm()
        return render(request, 'frontend/actors/specialist/contact.html', {'form': form})
