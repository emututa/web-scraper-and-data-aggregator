import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def scrape_jobs():
    logging.info("Scraping jobs...")
    print("Scraping jobs...")
    url = "https://vacancymail.co.zw/jobs/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        logging.info(f"Successfully fetched data from {url}")
        print(f"Successfully fetched data from {url}")

        soup = BeautifulSoup(response.text, 'html.parser')
        job_listings = soup.find_all('a', class_='job-listing')  # Adjusted selector

        if not job_listings:
            logging.warning("No job listings found.")
            print("No job listings found.")
            return

        # Prepare a list to collect job data
        jobs_data = []
        for job in job_listings:
            title = job.find('h3', class_='job-listing-title').text.strip() if job.find('h3', class_='job-listing-title') else "N/A"
            company = job.find('h4', class_='job-listing-company').text.strip() if job.find('h4', class_='job-listing-company') else "N/A"
            
            # Extract location and expiry date from the job listing footer
            footer = job.find('div', class_='job-listing-footer')
            if footer:
                # Location is typically the first <li> after the location icon
                location_icon = footer.find('i', class_='icon-material-outline-location-on')
                location = location_icon.find_parent('li').text.strip() if location_icon else "N/A"
                
                # Expiry date is typically the <li> with the expiry icon
                expiry_icon = footer.find('i', class_='icon-material-outline-access-time')
                expiry_date = expiry_icon.find_parent('li').text.strip() if expiry_icon else "N/A"
            else:
                location = "N/A"
                expiry_date = "N/A"

            description = job.find('p', class_='job-listing-text').text.strip() if job.find('p', class_='job-listing-text') else "N/A"
            
            jobs_data.append({
                "Job Title": title,
                "Company": company,
                "Location": location,
                "Expiry Date": expiry_date,
                "Description": description
            })

        # Store data in a DataFrame
        df = pd.DataFrame(jobs_data)

        # Save to CSV
        df.to_csv('scraped_data.csv', index=False)
        logging.info(f"Data saved to scraped_data.csv at {pd.Timestamp.now()}")
        print(f"Data saved to scraped_data.csv at {pd.Timestamp.now()}")

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        print(f"Error occurred: {e}")  # Print error to console

if __name__ == "__main__":
    logging.info("Starting the web scraper...")
    print("Starting the web scraper...")
    scrape_jobs()  # Call the function to execute scraping