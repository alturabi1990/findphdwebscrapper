# 1st install and import modules:
 #-- pip/pip3 install lxml
 #-- pip/pip3 install requests
 #-- pip/pip3 install beautifulsoup4
import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

phd_title = []
university_name = []
faculty_name = []
funding_status = []
supervisor_name = []
deadline_date = []
links = []

# 2nd step use requests to fetch url
result = requests.get("https://www.findaphd.com/phds/?Keywords=genetic+epidemiology")

# 3rd step save page content /markup

src = result.content
#print(src)


# 4th step create soup object to parse the content
soup = BeautifulSoup(src, "lxml")
#print(soup)

# 5th step find the elements containing info we need
#-- phd title, university, department/faculty, supervisor, funding type, deadline, project description, requirements

phd_titles = soup.find_all("a", {"class" : "h4 text-dark mx-0 mb-3"})
#print(phd_titles)
university = soup.find_all("span", {"class" : "phd-result__dept-inst--title"})
#print(university)
faculty_department = soup.find_all("a", {"class" : "col-24 px-0 col-md-auto deptLink phd-result__dept-inst--dept phd-result__dept-inst--title h6 mb-0 text-secondary font-weight-lighter"})
#print(faculty_department)
funding_type = soup.find_all("a", {"class" : "hoverTitle subButton text-wrap badge badge-light card-badge p-2 m-1 font-weight-light"})
#print(funding_type)
supervisor = soup.find_all("a", {"class" : "phd-result__key-info super text-wrap badge badge-light card-badge p-2 m-1 font-weight-light"})
#print(supervisor)
app_deadline = soup.find_all("a", {"class" : "hoverTitle subButton badge text-wrap badge-light card-badge p-2 m-1 font-weight-light"})
#print(app_deadline)


# 6th step loop over to return lists to extract needed info into other lists (look for error in range as there are some elements are not there
for i in range(len(supervisor)):
    phd_title.append(phd_titles[i].text)
    links.append(phd_titles[i].attrs['href'])
    university_name.append(university[i].text)
    faculty_name.append(faculty_department[i].text)
    funding_status.append(funding_type[i].text)
    supervisor_name.append(supervisor[i].text)
    deadline_date.append(app_deadline[i].text)
#print(phd_title, university_name, faculty_name, funding_status, supervisor_name, deadline_date)


# 7th step create csv file and fill it with values (there are skipping line)
file_list = [phd_title, university_name, faculty_name, funding_status, supervisor_name, deadline_date, links]
exported = zip_longest(*file_list)

with open("/Users/Elhami Alturabi/PycharmProjects/WebScraping/PhDList.csv", "w") as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["PhD title", "University name", "Faculty name", "Funding status", "Supervisor name", "Deadline date", "link"])
    wr.writerows(exported)