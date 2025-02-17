from django.shortcuts import render
import random
from Scholarship.models import Scholarship

def index(request):
    scholarships = list(Scholarship.objects.order_by('?')[:8])  # Get 8 random scholarships
    print(len(scholarships))  # Prints the number of scholarships retrieved

    return render(request, 'scholarship/index.html', {'scholarships': scholarships})



def about(request):
    return render(request, 'scholarship/about.html')

def contact(request):
    return render(request, 'scholarship/contact.html')

def scholarships(request):
    return render(request, 'scholarship/scholarships.html')