import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

t=input("Enter the Year for which you want to export the organization list( Note that this should be less than the current year): ")
url = 'https://summerofcode.withgoogle.com/archive/'+str(t)+'/organizations/'

r = requests.get(url)

if r.status_code == 404:
    print('Archive of this year is not available. Please run the file again with different year')
    exit()

soup = BeautifulSoup(r.content, 'html.parser')

rows = soup.select('section div ul li')

link_list = []

for row in rows:
        abc = 'https://summerofcode.withgoogle.com' + row.select_one('a')['href']
        link_list.append(abc)

OrgName = []
contactlink = []
techlist = []
slots = []
ideas = []

for org_url in link_list:
        lisat = []
        r = requests.get(org_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        org = soup.find('div', class_="banner__text")
        OrgName.append(f"=HYPERLINK(\"{org_url}\",\"{org.h3.text}\")")
        technologies = soup.find_all('li', class_="organization__tag--technology")
        for technology in technologies:
                lisat.append(technology.text)
        mys = ', '.join(lisat)
        techlist.append(mys)
        irc = soup.select_one(".org__meta-button")['href']
        contactlink.append(irc)
        projects = soup.find('ul', class_="project-list-container")
        slot = projects.findChildren('li')
        slots.append(len(slot))
        idea = soup.select_one(".org__button-container md-button")['href']
        ideas.append(idea)



table = {'Org' : OrgName , 'Technologies' : techlist , 'Slots' : slots , 'Ideas Page' : ideas , 'Contact' : contactlink}
df = DataFrame(table)
export_csv = df.to_csv(r'GSoC-Orgs-'+str(t)+'.csv')
print(r'Done!')
