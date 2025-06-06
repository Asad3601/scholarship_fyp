import requests # type: ignore
import math,time
from bs4 import BeautifulSoup
from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Scholarship.models import Scholarship






def chrome_options_args():
    chrome_options = Options()

    # Disable headless mode (run in visible browser for human-like behavior)
    chrome_options.add_argument("--headless")  # Comment this out for visible browser

    # Disable GPU acceleration (useful for headless mode)
    chrome_options.add_argument("--disable-gpu")

    # Disable sandboxing (for Linux environments)
    chrome_options.add_argument("--no-sandbox")

    # Start maximized (to mimic user behavior)
    chrome_options.add_argument("start-maximized")

    # Disable infobars (e.g., "Chrome is being controlled by automated software")
    chrome_options.add_argument("--disable-infobars")

    # Disable shared memory usage (useful for Docker or CI environments)
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set a custom user agent (mimic a real user's browser)
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

    # Disable automation flags (to avoid detection by anti-bot systems)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--ignore-certificate-errors")
    # Disable notifications (to mimic a clean user session)
    chrome_options.add_argument("--disable-notifications")

    # Disable extensions (to avoid unnecessary overhead)
    chrome_options.add_argument("--disable-extensions")

    # Disable pop-up blocking (to allow all pop-ups)
    chrome_options.add_argument("--disable-popup-blocking")

    # Disable password manager (to avoid saving credentials)
    chrome_options.add_argument("--disable-password-manager-reauthentication")

    # Disable translation (to avoid unnecessary network requests)
    chrome_options.add_argument("--disable-translate")

    # Disable background networking (to reduce resource usage)
    chrome_options.add_argument("--disable-background-networking")

    # Disable logging (to reduce console noise)
    chrome_options.add_argument("--log-level=3")

    # Disable WebRTC (to avoid IP leaks)
    chrome_options.add_argument("--disable-webrtc")

    # Disable WebGL (to reduce GPU usage)
    chrome_options.add_argument("--disable-webgl")

    # Disable 2D canvas (to reduce rendering overhead)
    chrome_options.add_argument("--disable-2d-canvas-clip-aa")

    # Disable 3D APIs (to reduce rendering overhead)
    chrome_options.add_argument("--disable-3d-apis")

    # Disable audio (to reduce resource usage)
    chrome_options.add_argument("--mute-audio")

    # Disable remote fonts (to reduce network requests)
    chrome_options.add_argument("--disable-remote-fonts")

    # Disable software rasterizer (to reduce CPU usage)
    chrome_options.add_argument("--disable-software-rasterizer")

    # Block ads by disabling features related to ads
    chrome_options.add_argument("--disable-features=PreloadMediaEngagementData,AutoplayIgnoreWebAudio,MediaEngagementBypassAutoplayPolicies")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # Optionally disable images to block image-based ads

    # Initialize the WebDriver with the configured options
    service = Service('chromedriver.exe')  # Update path to chromedriver if needed
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver
def add_scholarship_to_db(title, description, location, due_date, link,degrees="Masters,Bachelors,Phd"):
    """
    Check if the scholarship already exists in the database.
    If it does not exist, add it.
    """
    if not Scholarship.objects.filter(title=title, link=link).exists():
        Scholarship.objects.create(
            title=title,
            description=description,
            location=location,
            due_date=due_date,
            link=link,
            degrees=degrees,
        )
        print(f"Added scholarship: {title}")
    else:
        print(f"Skipped duplicate scholarship: {title}")


# def wemakescholarships(level, department, country):
#     print("country",country)
#     base_url = "https://www.wemakescholars.com"
#     url = "https://www.wemakescholars.com/scholarship?nationality=83"
#     driver = chrome_options_args()
#     driver.get(url)
#     wait = WebDriverWait(driver, 10)
#     time.sleep(5)  # Allow page to load

#     # Select "Level of Study"
#     wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='adv-filter-list']/ul/li[2]/span/span[1]"))).click()
#     time.sleep(2)
#     wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{level}')]"))).click()

#     # Select "Country"
#     wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='adv-filter-list']/ul/li[3]/div[2]/span/span[1]/span/ul/li/input"))).click()
#     time.sleep(2)
#     wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{country}')]"))).click()
#     time.sleep(3)

#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     valid_scholarships = [
#         base_url + s.find("h2").find('a')['href']
#         for s in soup.find_all("div", class_="post")
#         if not (s.find('div', class_='form-group pull-right') and 'Expired' in s.text)
#     ]

#     print(f"Found {len(valid_scholarships)} active scholarships.")

#     for index, scholarship_url in enumerate(valid_scholarships):
#         print(f"Scraping {index + 1}/{len(valid_scholarships)}: {scholarship_url}")
#         driver.get(scholarship_url)
#         time.sleep(5)

#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         title = soup.find("h1", class_='clrwms fw4 font18').text.strip() if soup.find("h1") else "No Title Found"
#         details = soup.find_all('span', class_='text-line-value')
#         deadline = details[2].text.strip() if len(details) > 2 else "N/A"
#         provider = details[3].text.strip() if len(details) > 3 else "N/A"
#         article = soup.find('article', class_='more-about-scholarship')
#         description = article.find('p').text.strip() if article else "No Description"

#         add_scholarship_to_db(title, description, provider, deadline, scholarship_url)
#         driver.back()
#         time.sleep(3)

#     driver.quit()

def wemake():
    base_url = "https://www.wemakescholars.com"
    url = "https://www.wemakescholars.com/scholarship?nationality=83"
    driver = chrome_options_args()
    driver.get(url)
    
    wait = WebDriverWait(driver, 10)
    # time.sleep(5)  # Allow page to load

    click_count = 0  # Track number of clicks
    while click_count < 20:
        try:
            load_more_button = wait.until(
                EC.element_to_be_clickable((By.ID, "load-more"))  # Adjust XPATH if needed
            )
            print(f"Clicking 'Load More' button... ({click_count + 1}/{2})")
            driver.execute_script("arguments[0].click();", load_more_button)
            time.sleep(3)  # Wait for new scholarships to load
            click_count += 1  # Increment click count
        except Exception as e:
            print("No more scholarships to load or button not found.")
            break

    # Get list of scholarships
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    scholarships = soup.find_all("div", class_="post")
    valid_scholarships = []  # To store non-expired scholarships

    for scholarship in scholarships:
        expire_tag = scholarship.find('div', class_='form-group pull-right')
        if expire_tag and 'Expired' in expire_tag.text:
            continue  # Skip expired scholarships

        h2_title = scholarship.find("h2", class_="post-title")
        a_tag = h2_title.find('a').get('href')
        scholarship_url = base_url + a_tag
        valid_scholarships.append(scholarship_url)

    # print(f"Found {len(valid_scholarships)} active scholarships.")

    # Visit each scholarship page
    for index, scholarship_url in enumerate(valid_scholarships):
        # print(f"Scraping {index + 1}/{len(valid_scholarships)}: {scholarship_url}")
        
        # Open the scholarship details page
        driver.get(scholarship_url)
        time.sleep(3)  # Allow page to load

        # Scrape details (Example: Get scholarship title)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        title = soup.find("h1",class_='clrwms fw4 font18').text.strip() if soup.find("h1") else "No Title Found"
        degrees=soup.find_all('span',class_='text-line-value')[0].text.strip()
        deadline=soup.find_all('span',class_='text-line-value')[2].text.strip()
        provider=soup.find_all('span',class_='text-line-value')[3].text.strip()
        article=soup.find('article',class_='more-about-scholarship')
        description=article.find('p').text.strip()
        add_scholarship_to_db(title, description, provider, deadline, scholarship_url,degrees)

        # Go back to the main page
        driver.back()
        time.sleep(3)  # Allow time to return to the list page

    driver.quit()
    
    
def scraper_masters():
    base_url = "https://www.mastersportal.com"
    search_url = "https://www.mastersportal.com/search/scholarships/master"
    driver = chrome_options_args()
    driver.get(search_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".SearchResultItem")))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    pages_element = soup.find("span", class_="SearchSummaryDesktop")
    if pages_element:
        scholarships_text = pages_element.text.strip()
        scholarships_number = int(''.join(filter(str.isdigit, scholarships_text)))  
    else:
        print("Scholarship count not found, defaulting to 1 page.")
        scholarships_number = 20  # Default to at least one page

    total_pages = math.ceil(scholarships_number / 20)
    print("pages ",total_pages)

    driver.quit()
    page=1
    while page<=2:
        print(f"Scraping page {page}")
        url=f"https://www.mastersportal.com/search/scholarships/master?page={page}"
        driver = chrome_options_args()
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".SearchResultItem")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        scholarships = soup.find_all("li", class_="SearchResultItem")
        for scholarship in scholarships:
            href = scholarship.find("a", class_="ScholarshipCard").get('href')
            full_url = base_url + href
            driver = chrome_options_args()
            driver.get(full_url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ScholarshipName")))

            scholarship_soup = BeautifulSoup(driver.page_source, 'html.parser')
            title = scholarship_soup.find('h1', class_="ScholarshipName").get_text(strip=True)
            university = scholarship_soup.find("a", class_="Name TextLink Connector js-organisation-info-link")
            university_text = university.get_text(strip=True) if university else "No University Info"
            location = scholarship_soup.find("span", class_="LocationItems")
            location_text = location.get_text(strip=True) if location else "No Location Info"
            articles = scholarship_soup.find_all("article", class_="ArticleContainer")
            description_text = ' '.join(p.get_text(strip=True) for p in articles[1].find_all('p')) if len(articles) >= 2 else "No Description"
            deadline = scholarship_soup.find_all("div", class_="Title")[3]
            deadline_text = deadline.get_text(strip=True) if deadline else "No Deadline Info"
            button = driver.find_element(By.CLASS_NAME, "js-cypressEligibilityButton")
            button.click()
            time.sleep(3)
            degrees=driver.find_element(By.XPATH,"//*[@id='SwitchableContent']/div[2]/article/div[1]/section/article[2]/div/div[4]/div/span").text
            # title, description, location, due_date, link,degrees
            add_scholarship_to_db(title,description_text,location_text,deadline_text,full_url)
            
            # requirements = article_eligibility.find("div", class_="ArticleSection RequirementsFacts")
            # print("requirements",requirements)
            # if requirements:
            #     div_tags = requirements.find_all("div")  # Find all div elements
            #     if len(div_tags) > 3:  # Ensure there are enough divs before accessing index 3
            #         div_tag = div_tags[3]
            #         degrees = div_tag.find("span").text.strip()  # Corrected spelling
            #         print(f"Degrees: {degrees}")
            #     else:
            #         print("Not enough <div> elements found inside requirements.")
            # else:
            #     print("Requirements section not found.")

            
            
            
            driver.quit()
            time.sleep(1)

        driver.quit()
        page=page+1
    driver.quit()
    
def scholarship_ads():
    url = "https://www.scholarshipsads.com/search/?nationality%5B%5D=279&page=1"
    driver = chrome_options_args()
    driver.get(url)


    # Allow the page to load and interact with the advanced search button

    wait = WebDriverWait(driver, 5)


    wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'title-heading')]")))
    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    page_heading = soup.find('h1').text
    count = int(page_heading.split(" ")[0])
    pages = math.ceil(count / 15)
    print(f"Total pages: {pages}")
    # Find all scholarships entries


    # Iterate over each scholarship and follow the link
    page_no=1
    while (page_no<=pages):
        print("scraping on page ",page_no)
        url=f'https://www.scholarshipsads.com/search/?nationality%5B%5D=279&page={page_no}'
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        scholarships = soup.find_all("div", class_="card-warp")
        scholarship_urls = []
        for scholarship in scholarships:
            expire_tag = scholarship.find('div', class_='card-deal expired')
            if not (expire_tag and expire_tag.text.strip() == 'Expired'):
                title = scholarship.find('h3')
                if title:
                    href = title.find('a').get('href')  # Get the href of the link
                    if href:
                        scholarship_urls.append(href)
        # Iterate over all scholarship URLs and extract details
        for url in scholarship_urls:
            driver.get(url)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title-heading")))  # Wait for the scholarship title to load
            
            # Extract the scholarship details on this page
            scholarship_page_soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Example: Extracting scholarship title and description from the individual page
            scholarship_title = scholarship_page_soup.find("div",class_="title-heading")
            if scholarship_title:
                title_text=scholarship_title.text.strip()
            scholarship_detail=scholarship_page_soup.find("div",class_="card-info col-md-8 col-lg-8 col-xs-12")
            ul=scholarship_detail.find('ul')
            if ul:
                school = ul.find_all('li')[1].text if len(ul.find_all('li')) > 1 else "School not found"
                degrees = ul.find_all('li')[2].text if len(ul.find_all('li')) > 2 else "School not found"
                country = ul.find_all('li')[5].text if len(ul.find_all('li')) > 5 else "Country not found"
                due_date = ul.find_all('li')[6].text if len(ul.find_all('li')) > 6 else "Due date not found"
                provider = f"{school} {country}"
                # print(f"Degrees: {degrees}")
            item = scholarship_page_soup.find_all("div", class_="scholarship-item")[0]  # Adjust selector as needed
            description=item.find_all('p')[1].text if len(item.find_all('p')) > 1 else "Description not exist"
            add_scholarship_to_db(title_text,description,provider,due_date,url,degrees)
            
            # Sleep to avoid making requests too quickly
            time.sleep(2)
        page_no+=1
    # Close the WebDriver
    driver.quit()


def studyaboardpk():
    # Navigate to the website
    base_url = "https://www.studyabroad.pk"
    url = "https://www.studyabroad.pk/scholarships/"
    driver=chrome_options_args()
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    time.sleep(5)  # Allow page to load

    # Get list of scholarships
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find("table")

    valid_scholarships = []  # Store non-expired scholarships

    if table:
        scholarships = table.find_all("tr")
        print(f"Total scholarships found: {len(scholarships)}")

        for scholarship in scholarships:
            td = scholarship.find('td')
            if td:
                a_tag = td.find('a')
                if a_tag and a_tag.get('href'):
                    scholarship_url = base_url + a_tag.get('href')
                    valid_scholarships.append(scholarship_url)

    print(f"Found {len(valid_scholarships)} active scholarships.")

    # Visit each scholarship page
    for index, scholarship_url in enumerate(valid_scholarships):
        print(f"Scraping {index + 1}/{len(valid_scholarships)}: {scholarship_url}")
        
        driver.get(scholarship_url)
        time.sleep(5)  # Allow page to load

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Check for the apply button
        apply_button = soup.find('p', class_='linkp')
        if not apply_button:
            print("Skipping expired scholarship...")
            continue  # Skip expired scholarships

        # Extract title
        title = soup.find("h1").text.strip() if soup.find("h1") else "No Title Found"

        # Extract provider
        provider = "Unknown Provider"
        table = soup.find("table")
        if table:
            tr_list = table.find_all('tr')
            if len(tr_list) > 0:
                tr0 = tr_list[0]
                country_td = tr0.find_all('td')
                if len(country_td) > 1:
                    country = country_td[1].text.strip()
            if len(tr_list) > 1:
                tr1 = tr_list[1]
                provider_td = tr1.find_all('td')
                if len(provider_td) > 1:
                    univerity = provider_td[1].text.strip()
            if len(tr_list) > 2:
                tr1 = tr_list[2]
                degree_td = tr1.find_all('td')
                if len(degree_td) > 1:
                    degrees = degree_td[1].text.strip()
            if len(tr_list)>4:
                tr1 = tr_list[4]
                deadline_td = tr1.find_all('td')
                if len(deadline_td) > 1:
                    deadline = deadline_td[1].text.strip()
            else:
                tr1 = tr_list[3]
                deadline_td = tr1.find_all('td')
                if len(deadline_td) > 1:
                    deadline = deadline_td[1].text.strip()
                
        provider=f"{univerity} {country}"
        # Extract description
        description = "No description found"
        article = soup.find('div', class_='postText')
        if article:
            paragraphs = article.find_all('p')
            if len(paragraphs) > 1:
                description = paragraphs[1].text.strip()
        add_scholarship_to_db(title,description,provider,deadline,url,degrees)
        # print(f"Title: {title}")
        # print(f"Provider: {provider}") 
        # print(f"DueDate: {deadline}") 
        # print(f"degrees: {degrees}") 
        # print(f"Description: {description}")
        # print("-" * 50)

    # Close the browser
    driver.quit()
    