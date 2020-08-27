from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import pandas as pd

class GlassdoorScrapper:

    def __init__(self):
        self.browser = 'chrome'

    def get_webdriver_instance(self, driver_path, url):
        '''
        Get WebDriver instance based on the browser configuration
        Args :
            None
        Returns :
            Webdriver instance
        '''

        if self.browser == "firefox":
            driver = webdriver.Firefox(executable_path=driver_path)
        elif self.browser == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            driver = webdriver.Chrome(executable_path=driver_path, options=options)
        elif self.browser == "ie":
            driver = webdriver.Ie()
        else:
            driver = webdriver.Chrome(executable_path=driver_path)
        
        driver.maximize_window()
        # Driver implicit timeout for an element, change it if your connection is slow
        driver.implicitly_wait(5)
        driver.get(url)
        return driver

    def print_verbose(self, job_title, job_description, employer_name, location, rating, salary_estimate):
        '''
        Printing collected data in case of verbose mode is set
        Args :
            job_title : Job title
            job_description : Job description upto 500 character
            employer_name : Company name
            location : Location of company
            rating : Rating of company
            salary_estimate : Salary estimate
        Returns :
            None
        '''        

        print("Job Title: {}".format(job_title))
        print("Job Description: {}".format(job_description[:500]))
        print("Employer Name: {}".format(employer_name))
        print("Location: {}".format(location))
        print("Rating: {}".format(rating))
        print("Salary Estimate: {}".format(salary_estimate))

    def print_company_details(self, headquarters, size, founded, type_of_ownership, industry, sctor, revenue, competitors):
        '''
        Printing collected data about company in case of verbose mode is set
        Args :
            headquarters : Company headquarters
            size : Employee size of company
            founded : Founded year
            type_of_ownership : Type of ownership of company
            industry : Industry details
            sector : Company sector
            revenue : Company revenue
            competitors : Competitors name 
        Returns :
            None
        '''

        print("Headquarters: {}".format(headquarters))
        print("Size: {}".format(size))
        print("Founded: {}".format(founded))
        print("Type of Ownership: {}".format(type_of_ownership))
        print("Industry: {}".format(industry))
        print("Sector: {}".format(sector))
        print("Revenue: {}".format(revenue))
        print("Competitors: {}".format(competitors))

    def get_job_details(self, driver_path, profile, iteration, verbose):
        '''
        Scrap data from Glassdoor and save jobs as pandas dataframe
        Args :
            driver_path : Webdriver binary path
            profile : Specific keyword for a job profile
            iteration : Number of posted jobs to scrap
            verbose : If set, display the details
        Returns :
            df : Dataframe of job_details 
        '''

        job_details = []

        #url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="+profile+"&sc.keyword="+profile+"&locT=&locId=&jobType="
        url = "https://www.glassdoor.co.in/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="+profile+"&sc.keyword="+profile+"&locT=&locId=&jobType="
        driver = self.get_webdriver_instance(driver_path, url)
        print(driver)

        while len(job_details) < iteration:
            # Test for the "Sign Up" prompt and get rid of it
            try:
                driver.find_element_by_class_name("selected").click()
            except ElementClickInterceptedException:
                pass

            time.sleep(1)

            try:
                driver.find_element_by_css_selector('[alt="Close"]').click()
                print(' Close out worked')
            except NoSuchElementException:
                print(' Close out failed')
                pass

            # Iterating over each job in this page
            # 'jl' for Job Listing button
            job_buttons = driver.find_elements_by_class_name("jl")
            for job_button in job_buttons:
                data_collection_status = False
                print("Progress: {}".format("" + str(len(job_details)) + "/" + str(iteration)))
                if len(job_details) >= iteration:
                    break

                job_button.click()
                time.sleep(1)
            
                while not data_collection_status:
                    try:
                        employer_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text
                        location = driver.find_element_by_xpath('.//div[@class="location"]').text
                        job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
                        job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                        data_collection_status = True
                    except:
                        print('Element not found, waiting')
                        time.sleep(5)

                try:
                    rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
                except NoSuchElementException:
                    rating = -1

                try:
                    salary_estimate = driver.find_element_by_xpath('.//span[@class="gray salary"]').text
                except NoSuchElementException:
                    salary_estimate = -1

                # Printing collected data in case of verbose mode is set
                if verbose:
                    print_verbose(job_title, job_description, employer_name, location, rating, salary_estimate)

                # Checking details on company tab
                try:
                    driver.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()

                    # Company headquarters
                    try:
                        headquarters = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                    except NoSuchElementException:
                        print('Element not found!')
                        headquarters = -1

                    # Company size
                    try:
                        size = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                    except NoSuchElementException:
                        print('Element not found!')
                        size = -1

                    # Company founded year
                    try:
                        founded = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                    except NoSuchElementException:
                        print('Element not found!')
                        founded = -1

                    # Company ownership type
                    try:
                        type_of_ownership = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                    except NoSuchElementException:
                        print('Element not found!')
                        type_of_ownership = -1

                    # Industry type
                    try:
                        industry = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                    except NoSuchElementException:
                        print('Element not found!')
                        industry = -1

                    # Company sector
                    try:
                        sector = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                    except NoSuchElementException:
                        print('Element not found!')
                        sector = -1

                    # Revenue details
                    try:
                        revenue = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                    except NoSuchElementException:
                        print('Element not found!')
                        revenue = -1

                    # Competitor details
                    try:
                        competitors = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                    except NoSuchElementException:
                        print('Element not found!')
                        competitors = -1

                # In case of no Company tab for job postings
                except NoSuchElementException:
                    print('Company details not found!')
                    headquarters = -1
                    size = -1
                    founded = -1
                    type_of_ownership = -1
                    industry = -1
                    sector = -1
                    revenue = -1
                    competitors = -1

                # If verbose set, print the details of company
                if verbose:
                    print_company_details(headquarters, size, founded, type_of_ownership, industry, sctor, revenue, competitors)

                job_details.append({"Job Title" : job_title,
                    "Job Description" : job_description,
                    "Employer Name" : employer_name,
                    "Location" : location,
                    "Rating" : rating,
                    "Salary Estimate" : salary_estimate,
                    "Headquarters" : headquarters,
                    "Size" : size,
                    "Founded" : founded,
                    "Type of ownership" : type_of_ownership,
                    "Industry" : industry,
                    "Sector" : sector,
                    "Revenue" : revenue,
                    "Competitors" : competitors})
            
            
            # Clicking on the "next page" button
            try:
                driver.find_element_by_xpath('.//li[@class="next"]//a').click()
            except NoSuchElementException:
                print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
                break

        return pd.DataFrame(job_details)
