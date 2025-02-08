import csv
import urllib.request
from bs4 import BeautifulSoup


url = "https://www.hogapage.de/jobs/suche?q=Koch&where=Frankfurt%2C+Germany&radius=200"

response = urllib.request.urlopen(url).read()
soup = BeautifulSoup(response, 'html.parser')
jobs_data = []

for script in soup(["script", "style"]):
    script.extract()

# title = soup.title
# print(title)

# Save soup data to file
with open('sato_data.txt', 'w') as file:
    file.write(str(soup))

allthelisting = soup.find_all("div", {"class": "hp_search-list-item-body"})

count = 0

for job in allthelisting:
    # if count >= 2:
    # break  # Stop after printing details of 2 jobs

    # Find the job title inside the <a> tag
    title_tag = job.find("a")
    if title_tag:
        job_title = title_tag.text.strip()
        job_link = "https://www.hogapage.de" + title_tag["href"]

        # Now, extract more details from job page
        try:
            job_response = urllib.request.urlopen(job_link).read()
            job_soup = BeautifulSoup(job_response, 'html.parser')

            for script in job_soup(["script", "style"]):
                script.extract()

            # with open('sato_data.txt', 'w') as file:
            #   file.write(str(job_soup))

            # Extract company name
            company_tag = job_soup.find("div", class_="mb-hp_smallest")
            company_name = company_tag.get_text(
                strip=True) if company_tag else "Company name not found"

            # Extract address
            address_tag = job_soup.find("address")
            address = address_tag.get_text(
                strip=True) if address_tag else "Address not found"

            # Extract contact person (Fixed)
            contact_person = ""
            contact_section = job_soup.find(
                "div", class_="position-relative mb-hp_smaller")
            if contact_section:
                bold_tags = contact_section.find_all("b")
                for bold in bold_tags:
                    if "Kontakt" in bold.get_text():
                        next_element = bold.find_next_sibling(string=True)
                        if next_element:
                            contact_person = next_element.strip()
                        break

            # Extracting telephone numbers
            phone_numbers = [a['href'].replace('tel:', '') for a in job_soup.find_all(
                'a', href=True) if 'tel:' in a['href']]

            # Extracting emails
            emails = list({a['href'].replace('mailto:', '').split('?')[0] for a in job_soup.find_all(
                'a', href=True) if 'mailto:' in a['href']})

            jobs_data.append([job_title, job_link, company_name, address,
                              contact_person, ", ".join(phone_numbers), ", ".join(emails)])
            print(f"✅ Successfully fetched job: {job_title}")

        except Exception as e:
            print(f"Error fetching job deatails: {e}")

    else:
        print("Job Name not found")

csv_filename = "job_listings.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Job Title", "Website", "Company Name",
                    "Address", "Contact Person", "Phone Number", "Email"])
    writer.writerows(jobs_data)

print(f"📁 CSV file '{csv_filename}' created successfully.")


# TODO - add filters
# TODO - save data to database
# TODO - load  more pages
