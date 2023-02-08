from bs4 import BeautifulSoup
from Class import Class
from Program import Program
from GenEd import GenEd
import requests

def get_class_data(code: str) -> Class:
    print(code)
    url = f"https://www.rit.edu/programs-api/?type=c&q={code}&college=&degree=&text="
    xml_data = requests.get(url).content
    class_data = BeautifulSoup(xml_data, "xml")
    title = class_data.title.text
    desc = class_data.description.text
    credits = get_credits(class_data.credits.text)
    offered = class_data.typically_offered.text.split(", ")
    requisites = class_data.requisites.text
    return Class(title, code, desc, credits, offered, requisites)


def get_credits(credit_string: str) -> int:
    credit_split = credit_string.split(" ")
    for i in range(0, len(credit_split)-1):
        if credit_split[i] == "Credits":
            return int(credit_split[i+1])
        

def get_program_data(code: str) -> Program:
    url = f"https://www.rit.edu/programs-api/?type=p&q={code}&college=&degree=&text="
    xml_data = requests.get(url).content
    program_data = BeautifulSoup(xml_data, "xml")
    
    all_tr = program_data.program.curriculum_processed.table.tbody.find_all("tr")
    years = 0
    for tr in all_tr:
        if "data-heading" in tr.attrs:
            if int(tr['data-heading']) > years:
                years = int(tr['data-heading'])
                
    courses = []
    exclusive_list = []
    for year in range(years):
        classes = program_data.program.curriculum_processed.table.tbody.find_all("tr", class_=f"hidden-row rows-{year+1}")
        for course in classes:
            tds = course.find_all("td")
            
            if len(tds[0].text) < 2:
                courses.append(GenEd(tds[1].text, int(tds[-1].text)))
                if exclusive_list:
                    courses.append(exclusive_list)
                    exclusive_list = []
            elif tds[0].text == "Choose one of the following:":
                exclusive_list = [1]
            elif tds[0].text == "Choose two of the following:":
                exclusive_list = [2]
            elif ord(tds[0].text[0]) == 160:
                exclusive_list.append(get_class_data(tds[0].text[3:]))
            else:
                if exclusive_list:
                    courses.append(exclusive_list)
                    exclusive_list = []
                courses.append(get_class_data(tds[0].text))
            
    return Program(courses, code, program_data.program.title.text)
    
# print(str(get_class_data(["csec-123"])[0]))
print(repr(get_program_data("PSYC-BS")))