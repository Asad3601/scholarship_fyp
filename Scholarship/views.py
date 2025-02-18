from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.http import JsonResponse,request
from django.urls import reverse
import requests,schedule,time

from bs4 import BeautifulSoup
from urllib.parse import unquote
import threading
from Scholarship.models import Scholarship
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .scraper import scraper_masters,wemake,scholarship_ads
from concurrent.futures import ThreadPoolExecutor
from django.db.models import Q
    # url = "https://www.scholarshipsads.com" 200
    # url = "https://www.scholarshipsads.com/search/?nationality%5B%5D=279&country%5B%5D=&degree%5B%5D=&subject%5B%5D=&funding%5B%5D=" 200
    # url="https://www.daad.pk" 200
    # 1 "https://www.studyabroad.pk/scholarships/"
    
    # ----------------------------- #
    
    #  https://www.scholarshipsads.com/search/?nationality%5B%5D=&country%5B%5D=135&degree%5B%5D=441&subject%5B%5D=&funding%5B%5D=
    # https://www.mastersportal.com/search/scholarships/master/united-kingdom/computer-science-it 
    
    # ----------------------------- #


def scholarships_portal(request):
    try:
        if request.method == 'POST':
            # Scholarship.objects.all().delete()
            level = request.POST.get('level')
            department = request.POST.get('department')
            country = request.POST.get('country')
            redirect_url = reverse('scholarships') + f'?level={level}&department={department}&country={country}'
            return redirect(redirect_url)
        return redirect('scholarships')
    except Exception as e:
        print(f"Error: {str(e)}")
        return render(request, 'scholarship/scholarships.html', {'error': "An error occurred while fetching scholarships."})


# def masters_portal(request):
#     print("Request is comming");
#     level = request.POST.get('level', '').lower()  # Convert to lowercase
#     if level.endswith('s'):  
#         level = level[:-1]  # Remove last character if it's 's'
    
#     department = '-'.join(request.POST.get('department', '').split(' '))  
#     country = '-'.join(request.POST.get('country', '').lower().split(' '))  # Convert to lowercase
#     scraper_masters(level, department, country)
#     return response(request)



    

    

def scholarships_data(request):
    level = request.GET.get('level', '')
    department = request.GET.get('department', '').replace('-', ' ')  # Convert back to normal text
    country = request.GET.get('country', '').replace('-', ' ')  
    print(level, department, country)

    # Fetch all scholarships (No Filtering)
    all_scholarship_listings = list(Scholarship.objects.all())
    random.shuffle(all_scholarship_listings)


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

    return render(request, 'scholarship/scholarships.html', context)







def get_scholarship_by_title(request, title):
    # Decode URL-encoded title
    decoded_title = unquote(title)
    

    if decoded_title:
        scholarship = Scholarship.objects.filter(title__icontains=decoded_title).first()  # Get first matching scholarship
        if scholarship:
            return render(request, 'scholarship/scholarship_detail.html', {'scholarship': scholarship})
        else:
            return render(request, 'scholarship/scholarship_detail.html', {'error': 'Scholarship not found'})

    return render(request, 'scholarship/scholarship_detail.html', {'error': 'No title provided'})


def scholarships_get(request):
    print("Request method:", request.method)
    if request.method =='POST':
        print("request is comming...")
        # Get filter values from POST data
        level = request.POST.get('level', '').strip()
        department = request.POST.get('department', '').replace('-', ' ').strip()
        country = request.POST.get('country', '').replace('-', ' ').strip()

        print(f"Level: {level}, Department: {department}, Country: {country}")

        # Start with the base queryset
        scholarships_queryset = Scholarship.objects.all()
        print(f"Initial scholarship count: {len(scholarships_queryset)}")

        # Apply filters based on the provided criteria
        if department and level and country:
            # If all three filters are provided, apply only one based on priority
            scholarships_queryset = scholarships_queryset.filter(
                Q(title__icontains=department) |
                Q(description__icontains=department) |
                Q(location__icontains=department)
            )
        elif department and level:
            # If department and level are provided, apply both filters
            scholarships_queryset = scholarships_queryset.filter(
                Q(title__icontains=department) |
                Q(description__icontains=department) |
                Q(location__icontains=department)
            ).filter(
                degrees__icontains=level
            )
        elif department and country:
            # If department and country are provided, apply both filters
            scholarships_queryset = scholarships_queryset.filter(
                Q(title__icontains=department) |
                Q(description__icontains=department) |
                Q(location__icontains=department)
            ).filter(
                location__icontains=country
            )
        elif level and country:
            # If level and country are provided, apply both filters
            scholarships_queryset = scholarships_queryset.filter(
                degrees__icontains=level
            ).filter(
                location__icontains=country
            )
        elif department:
            # If only department is provided, apply department filter
            scholarships_queryset = scholarships_queryset.filter(
                Q(title__icontains=department) |
                Q(description__icontains=department) |
                Q(location__icontains=department)
            )
        elif level:
            # If only level is provided, apply level filter
            scholarships_queryset = scholarships_queryset.filter(
                degrees__icontains=level
            )
        elif country:
            # If only country is provided, apply country filter
            scholarships_queryset = scholarships_queryset.filter(
                location__icontains=country
            )

        print(f"Filtered scholarship count: {len(scholarships_queryset)}")

        # Convert to list for shuffling
        all_scholarship_listings = list(scholarships_queryset)

        # Shuffle the filtered scholarships
        random.shuffle(all_scholarship_listings)

        # Pagination logic (unchanged)
        if len(all_scholarship_listings) > 0:
            paginator = Paginator(all_scholarship_listings, 10)
            page = request.GET.get('page', 1)
            try:
                page = int(page)
            except ValueError:
                page = 1

            try:
                scholarship_listings = paginator.page(page)
            except PageNotAnInteger:
                scholarship_listings = paginator.page(1)
            except EmptyPage:
                scholarship_listings = paginator.page(paginator.num_pages)

            total_scholarship = len(all_scholarship_listings)  # Total count of filtered scholarships

            # Adjust the pagination range
            current_page = scholarship_listings.number
            if current_page <= 3:
                limited_page_range = range(1, min(paginator.num_pages, 5) + 1)
            else:
                limited_page_range = range(current_page - 2, min(paginator.num_pages, current_page + 2) + 1)

            # Prepare context for rendering
            context = {
                'scholarships': scholarship_listings,
                'total_scholarship': total_scholarship,
                'limited_page_range': limited_page_range,
            }
        else:
            # If no scholarships were found
            context = {'scholarships': [], 'total_scholarship': 0}

        return render(request, 'scholarship/scholarships.html', context)











def run_scrapper():
    try:
        print("Running scrapers in parallel...")

        # Run scrapers concurrently
        with ThreadPoolExecutor() as executor:
            executor.submit(wemake)
            executor.submit(scraper_masters)
            executor.submit(scholarship_ads)

        print("Scraping completed.")
    except Exception as e:
        print(f"Error in run_scrapper: {e}")

def start_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Schedule the scraper every 1 day
schedule.every(5).minutes.do(run_scrapper)

# Run scheduler in a separate thread
scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
scheduler_thread.start()

print("Scheduler started...")

