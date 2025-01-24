from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
import requests
import math
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Scholarship.models import Scholarship
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .scraper import scraper_masters
    # url = "https://www.scholarshipsads.com" 200
    # url = "https://www.scholarshipsads.com/search/?nationality%5B%5D=279&country%5B%5D=&degree%5B%5D=&subject%5B%5D=&funding%5B%5D=" 200
    # url="https://www.daad.pk" 200
    # 1 "https://www.studyabroad.pk/scholarships/"
    
    # ----------------------------- #
    
    #  https://www.scholarshipsads.com/search/?nationality%5B%5D=&country%5B%5D=135&degree%5B%5D=441&subject%5B%5D=&funding%5B%5D=
    # https://www.mastersportal.com/search/scholarships/master/united-kingdom/computer-science-it 
    
    # ----------------------------- #


def masters_portal(request):
    try:
        if request.method == 'POST':
            Scholarship.objects.all().delete()
            level = request.POST.get('level')
            department = '-'.join(request.POST.get('department', '').split(' '))
            country = '-'.join(request.POST.get('country', '').split(' '))
            scraper_masters(level,department,country)
            return redirect('scholarships')
        return redirect('scholarships')
    except Exception as e:
        print(f"Error: {str(e)}")
        return render(request, 'scholarship/scholarships.html', {'error': "An error occurred while fetching scholarships."})




def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'

def scholarships_data(request):
    query = request.GET.get('q', '')
    
    # Filter scholarships based on the query if provided
    all_scholarship_listings = Scholarship.objects.all()
    if query:
        all_scholarship_listings = all_scholarship_listings.filter(title__icontains=query)  # Example filter

    paginator = Paginator(all_scholarship_listings, 15)  # 15 items per page
    page = request.GET.get('page')

    try:
        scholarship_listings = paginator.page(page)
    except PageNotAnInteger:
        scholarship_listings = paginator.page(1)
    except EmptyPage:
        scholarship_listings = paginator.page(paginator.num_pages)

    total_scholarship = Scholarship.objects.count()  # Total count of scholarships

    # Determine the current page number
    current_page = scholarship_listings.number

    # Adjust the limit based on the current page number
    if current_page <= 3:
        limited_page_range = range(1, min(paginator.num_pages, 5) + 1)
    else:
        limited_page_range = range(current_page - 2, min(paginator.num_pages, current_page + 2) + 1)

    context = {
        'scholarships': scholarship_listings,
        'total_scholarship': total_scholarship,
        'limited_page_range': limited_page_range,
        'query': query
    }

    # Check if the request is AJAX
    if is_ajax(request):  # Call your custom is_ajax function here
        html = render_to_string('scholarship/scholarship_list.html', context)
        return JsonResponse({'html': html})

    return render(request, 'scholarship/scholarships.html', context)

def scholarships_ads(request):
    try:
        url = "https://www.scholarshipsads.com/search/?nationality%5B%5D=&country%5B%5D=135&degree%5B%5D=441&subject%5B%5D=&funding%5B%5D="
        response = requests.get(url)
        
        
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            scholarships = soup.find_all("div", class_="scholarship-card")
            
            # Extract scholarship titles and other data
            scholarships_Data = []
            for scholarship in scholarships:
                title_tag = scholarship.find("a", class_="no-hover")
                if title_tag:  # Ensure the tag exists to avoid AttributeError
                    scholarships_Data.append(title_tag.text.strip())
            
            # Return the extracted data as JSON
            return JsonResponse({'status': 'success', 'scholarships': scholarships_Data,"length":len(scholarships_Data)}, status=200)
        else:
            # Handle non-200 status codes
            return JsonResponse({'status': 'error', 'message': f"Failed to fetch data. HTTP Status: {response.status_code}"}, status=response.status_code)
    except requests.RequestException as e:
        # Handle connection errors or other exceptions
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
