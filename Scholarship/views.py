from django.shortcuts import render
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

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
            level = request.POST.get('level')
            department = '-'.join(request.POST.get('department', '').split(' '))
            country = '-'.join(request.POST.get('country', '').split(' '))

            
            url = f"https://www.mastersportal.com/search/scholarships/{level}/{country}/{department}"
            print(url)
            # Configure Selenium WebDriver
            chrome_options = Options()
            # chrome_options.add_argument("--headless")  # Run in headless mode
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("start-maximized")
            chrome_options.add_argument("enable-automation")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            # Specify the path to the chromedriver
            service = Service('chromedriver.exe')  # Update path to chromedriver
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Access the URL
            driver.get(url)
            
            # Extract page source
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            time.sleep(8)
            # Extract scholarship data
            scholarships = soup.find_all("li", class_="SearchResultItem")
            scholarships_Data = []
            # Collect scholarship names
            time.sleep(3)
            for scholarship in scholarships:
                title_tag = scholarship.find("h2", class_="ScholarshipName")
                if title_tag:
                    scholarships_Data.append(title_tag.text.strip())
            
            # Close the browser
            driver.quit()
            
            # Debugging: Print scholarships data
            print("length of scholarships_Data",len(scholarships_Data))
            
            # Return the data to the template
            return render(request, 'scholarship/scholarships.html', {'scholarships': scholarships_Data, "count": len(scholarships_Data)})
        return render(request, 'scholarship/scholarships.html', {'scholarships': [], "count": 0})
    except Exception as e:
        # Print the exception for debugging
        print(f"Error: {str(e)}")
        
         



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
