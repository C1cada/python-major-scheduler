from bs4 import BeautifulSoup
from Class import Class
from Program import Program
from GenEd import GenEd
import requests
import re

def get_class_data(code: str) -> Class:
    try:
        url = f"https://www.rit.edu/programs-api/?type=c&q={code}&college=&degree=&text="
        xml_data = requests.get(url).content
        class_data = BeautifulSoup(xml_data, "xml")
        title = class_data.title.text
        desc = class_data.description.text
        credits = get_credits(class_data.credits.text)
        offered = class_data.typically_offered.text.split(", ")
        requisites = class_data.requisites.text
        c = Class(title, code, desc, credits, offered, requisites)
    except Exception as e:
        print(e)
        c = Class(code=code)
    return c


def get_credits(credit_string: str) -> int:
    credit_split = credit_string.split(" ")
    for i in range(0, len(credit_split)-1):
        if credit_split[i] == "Credits":
            return int(credit_split[i+1])
        
def get_classes(classes, list):
    exclusive_list = []
    for course in classes:
        tds = course.find_all("td")
        # try:
        if tds:
            print(tds[0].text)
            if len(tds[0].text) < 2:
                if "elective" in tds[-1].text.lower():
                    list.append(GenEd(tds[-1].text, 0))
                else:
                    list.append(GenEd(tds[1].text, int(tds[-1].text)))
                if exclusive_list:
                    list.append(exclusive_list)
                    exclusive_list = []
            elif tds[0].text == "Choose one of the following:":
                exclusive_list = [1]
            elif tds[0].text == "Choose two of the following:":
                exclusive_list = [2]
            elif tds[0].text == "Choose three of the following:":
                exclusive_list = [3]
            elif tds[0].text == "Choose any combination of four of the following:":
                exclusive_list = [4]
            elif ord(tds[0].text[0]) == 160:
                exclusive_list.append(get_class_data(tds[0].text[3:]))
            else:
                if exclusive_list:
                    list.append(exclusive_list)
                    exclusive_list = []
                list.append(get_class_data(tds[0].text))
            # except Exception as e:
            #     print(e)
            #     print(tds)
            #     print(course)
            #     list.append(Class(code = course.td.text))

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
    for year in range(years):
        classes = program_data.program.curriculum_processed.table.tbody.find_all("tr", class_=f"hidden-row rows-{year+1}")
        get_classes(classes, courses)
                
    tables = []
    tracks = {}
    other = {}
    for h3 in program_data.program.curriculum_processed.find_all("h3"):
        if h3.text != "Tracks" and not "degree" in h3.text.lower():
            other[h3.text] = []
            table = h3.find_next_sibling('table')
            classes = table.tbody.find_all("tr")
            get_classes(classes, other[h3.text])
    
    for h4 in program_data.program.curriculum_processed.find_all("h4"):
        tracks[h4.text] = []
        table = h4.find_next_sibling('table')
        classes = table.tbody.find_all("tr")
        get_classes(classes, tracks[h4.text])
        
    tables.append(tracks)
    tables.append(other)
            
    return Program(courses, code, program_data.program.title.text, tables)
    
# print(str(get_class_data("SWEN-262")))
print(repr(get_program_data("ECON-BS")))