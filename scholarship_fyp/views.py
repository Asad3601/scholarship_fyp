from django.shortcuts import render

def index(request):
    return render(request, 'scholarship/index.html')


def about(request):
    return render(request, 'scholarship/about.html')

def contact(request):
    return render(request, 'scholarship/contact.html')

def scholarships(request):
    return render(request, 'scholarship/scholarships.html')