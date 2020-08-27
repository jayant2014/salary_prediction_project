from glassdoor_scrapper import GlassdoorScrapper
import pandas as pd 
from datetime import datetime

driver_path = "bin/chromedriver"

gs = GlassdoorScrapper()
#print(dir(gs))

# List of job profiles to search
job_profiles = ['devops', 'data scientist', 'fullstack', 'test analyst', 'solutions architect', 'machine learning']
for profile in job_profiles:
    print('Collecting data for '+profile+' ....')
    df = gs.get_job_details(driver_path, profile, 100, False)
    datafile = datetime.now().strftime('glassdoor_'+profile+'_jobs_%Y%m%d%H%M.csv')
    df.to_csv(datafile, index = False)
