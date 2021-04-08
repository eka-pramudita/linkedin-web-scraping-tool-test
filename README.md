# LinkedIn Web-Scraping Tool Test
A web scraping tool to gather job information data designed for LinkedIn

## Data Feature
1. Job Title
2. Company Name
3. Job Posting Time (23 hours ago, 1 minute ago, etc)
4. Number of applicants
5. Seniority level  (Entry level/Associate/Mid-senior level)
6. Size of employee (unable for this version because need to login)
7. Company industry
8. Detail description (job desc, job req, benefit, etc)
9. Employment type
10. Job Function

##Keyword Search Tag
- Senior Data Engineer / Data Engineer
- Senior Data Scientist / Data Scientist
- Senior Data Analyst / Data Analyst
- Senior Business Intelligence / Business Intelligence Analyst


## Flow
1. This tool scrape data from the non-login LinkedIn page. Example:
https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Indonesia&geoId=102478259&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0
2. Data gathered from the right pane of the page, while the right pane is dynamically changing when the job card on left pane is clicked
3. This program uses Selenium o enable auto-click to repeatedly clicking job cards on the left pane
4. After a click on a job card, this program get the data needed from the right pane and store them in array
5. After all data gathering process completed, this program convert array into dataframe and drop row duplicates in the dataset
6. The dataset then become converted to .csv file saved in the same directory with the program

