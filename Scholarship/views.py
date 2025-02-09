from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.urls import reverse
import requests

from bs4 import BeautifulSoup

from Scholarship.models import Scholarship

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .scraper import scraper_masters,wemakescholarships
    # url = "https://www.scholarshipsads.com" 200
    # url = "https://www.scholarshipsads.com/search/?nationality%5B%5D=279&country%5B%5D=&degree%5B%5D=&subject%5B%5D=&funding%5B%5D=" 200
    # url="https://www.daad.pk" 200
    # 1 "https://www.studyabroad.pk/scholarships/"
    
    # ----------------------------- #
    
    #  https://www.scholarshipsads.com/search/?nationality%5B%5D=&country%5B%5D=135&degree%5B%5D=441&subject%5B%5D=&funding%5B%5D=
    # https://www.mastersportal.com/search/scholarships/master/united-kingdom/computer-science-it 
    
    # ----------------------------- #

def response(request):
    all_scholarship_listings = Scholarship.objects.all()

    # Paginate
    paginator = Paginator(all_scholarship_listings, 15)  # 15 items per page
    page = request.GET.get('page', 1)  # Default to page 1 if not provided

    try:
        scholarship_listings = paginator.page(page)
    except PageNotAnInteger:
        scholarship_listings = paginator.page(1)
    except EmptyPage:
        scholarship_listings = paginator.page(paginator.num_pages)

    total_scholarship = paginator.count  # Total count of scholarships
    current_page = scholarship_listings.number  # Get the current page number
    total_pages = paginator.num_pages  # Total pages

    # Adjust pagination range for navigation
    if current_page <= 3:
        limited_page_range = range(1, min(total_pages, 5) + 1)
    else:
        limited_page_range = range(current_page - 2, min(total_pages, current_page + 2) + 1)

    response_data = {
        'scholarships': list(scholarship_listings.object_list.values()),  # Convert QuerySet to list of dicts
        'total_scholarship': total_scholarship,
        'limited_page_range': list(limited_page_range),
        'has_next': scholarship_listings.has_next(),
        'has_previous': scholarship_listings.has_previous(),
        'current_page': current_page,
        'total_pages': total_pages
    }

    return JsonResponse(response_data, safe=True)

    

def masters_portal(request):
    level = request.POST.get('level', '').lower()  # Convert to lowercase
    if level.endswith('s'):  
        level = level[:-1]  # Remove last character if it's 's'
    
    department = '-'.join(request.POST.get('department', '').split(' '))  
    country = '-'.join(request.POST.get('country', '').lower().split(' '))  # Convert to lowercase
    
    scraper_masters(level, department, country)
    return response(request)



def wemakescholars_portal(request):
    try:
        if request.method == 'POST':
            Scholarship.objects.all().delete()
            level = request.POST.get('level')
            department = request.POST.get('department')
            country = request.POST.get('country')
            wemakescholarships(level,department,country)
            redirect_url = reverse('scholarships') + f'?level={level}&department={department}&country={country}'
            return redirect(redirect_url)
        return redirect('scholarships')
    except Exception as e:
        print(f"Error: {str(e)}")
        return render(request, 'scholarship/scholarships.html', {'error': "An error occurred while fetching scholarships."})



def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'

def scholarships_data(request):
    level = request.GET.get('level', '')
    department = request.GET.get('department', '').replace('-', ' ')  # Convert back to normal text
    country = request.GET.get('country', '').replace('-', ' ')  
    print(level, department, country)

    # Fetch all scholarships (No Filtering)
    all_scholarship_listings = Scholarship.objects.all()

    # Paginate
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

    # Adjust the pagination range
    if current_page <= 3:
        limited_page_range = range(1, min(paginator.num_pages, 5) + 1)
    else:
        limited_page_range = range(current_page - 2, min(paginator.num_pages, current_page + 2) + 1)

    # Construct query string only if all parameters exist
    context = {
        'scholarships': scholarship_listings,
        'total_scholarship': total_scholarship,
        'limited_page_range': limited_page_range,
    }

    if level and department and country:
        query_params = {
            'level': level,
            'department': department,
            'country': country,
        }
        # query_string = '&'.join(f"{key}={value}" for key, value in query_params.items() if value)
        context['query'] = query_params  # Add query string to context

    # Check if the request is AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('scholarship/scholarship_list.html', context)
        return JsonResponse({'html': html})

    return render(request, 'scholarship/scholarships.html', context)

def scholarships_ads(request):
    print("response",request.POST.get('country'))
    country=request.POST.get('country')
    return JsonResponse({'status': 'success', 'country': country})
#     # try:
#         # url = "https://www.scholarshipsads.com/search/?nationality%5B%5D=&country%5B%5D=135&degree%5B%5D=441&subject%5B%5D=&funding%5B%5D="
#         # response = requests.get(url)
        
        
#         # if response.status_code == 200:
#         #     # Parse the HTML content using BeautifulSoup
#         #     soup = BeautifulSoup(response.text, 'html.parser')
#         #     scholarships = soup.find_all("div", class_="scholarship-card")
            
#         #     # Extract scholarship titles and other data
#         #     scholarships_Data = []
#         #     for scholarship in scholarships:
#         #         title_tag = scholarship.find("a", class_="no-hover")
#         #         if title_tag:  # Ensure the tag exists to avoid AttributeError
#         #             scholarships_Data.append(title_tag.text.strip())
            
#         #     # Return the extracted data as JSON
#         #     return JsonResponse({'status': 'success', 'scholarships': scholarships_Data,"length":len(scholarships_Data)}, status=200)
#         # else:
#         #     # Handle non-200 status codes
#         #     return JsonResponse({'status': 'error', 'message': f"Failed to fetch data. HTTP Status: {response.status_code}"}, status=response.status_code)
#     # except requests.RequestException as e:
#     #     # Handle connection errors or other exceptions
#     #     return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
