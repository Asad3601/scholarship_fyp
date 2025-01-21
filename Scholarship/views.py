from django.shortcuts import render
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

            base_url = "https://www.mastersportal.com"
            search_url = f"{base_url}/search/scholarships/{level}/{country}/{department}"

            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Run in headless mode
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("start-maximized")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("enable-automation")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

            service = Service('chromedriver.exe')  # Update path to chromedriver if needed

            # Initialize the WebDriver
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get(search_url)

            # Wait for the search results to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".SearchResultItem")))

            # Parse the initial page to determine the total number of pages
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            page_heading = soup.find('span', class_="SearchSummaryDesktop").text
            count = int(page_heading.split(" ")[0])
            pages = math.ceil(count / 20)
            driver.quit()

            scholarships_data = []

            for page_no in range(1, pages+1):
                print(f"Scraping page {page_no}")
                paginated_url = f"{search_url}?page={page_no}"

                # Initialize a new WebDriver instance for each page
                driver = webdriver.Chrome(service=service, options=chrome_options)
                driver.get(paginated_url)

                # Wait for the search results to load
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".SearchResultItem")))

                # Parse the current page
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                scholarships = soup.find_all("li", class_="SearchResultItem")

                for scholarship in scholarships:
                    href = scholarship.find("a", class_="ScholarshipCard").get('href')
                    full_url = base_url + href
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                    driver.get(full_url)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ScholarshipName")))

                    scholarship_page_source = driver.page_source
                    scholarship_soup = BeautifulSoup(scholarship_page_source, 'html.parser')

                    try:
                        title = scholarship_soup.find('h1', class_="ScholarshipName").get_text(strip=True)
                        university = scholarship_soup.find("a", class_="Name TextLink Connector js-organisation-info-link")
                        university_text = university.get_text(strip=True) if university else "No University Info"

                        location = scholarship_soup.find("span", class_="LocationItems")
                        location_text = location.get_text(strip=True) if location else "No Location Info"

                        description = scholarship_soup.find("article", class_="ArticleContainer")
                        description_text = description.get_text(strip=True) if description else "No Description"

                        deadline = scholarship_soup.find_all("div", class_="Title")[3]
                        deadline_text = deadline.get_text(strip=True) if deadline else "No Deadline Info"

                        scholarships_data.append({
                            'title': title,
                            'description': description_text,
                            'location': f"{university_text} {location_text}",
                            'due_date': deadline_text
                        })
                        driver.quit()
                    except Exception as e:
                        print(f"Error scraping {full_url}: {e}")
                        continue

                    time.sleep(1)  # Short delay to avoid overwhelming the server

                driver.quit()

            return render(request, 'scholarship/scholarships.html', {'scholarships': scholarships_data, "count": len(scholarships_data)})

        return render(request, 'scholarship/scholarships.html', {'scholarships': [], "count": 0})

    except Exception as e:
        print(f"Error: {str(e)}")
        return render(request, 'scholarship/scholarships.html', {'error': "An error occurred while fetching scholarships."})


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
