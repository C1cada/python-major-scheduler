import re

class Class:
    def __init__(self, name: str, code: str, desc: str, credit: int, offered: list, requisites: str) -> None:
        self.name = name
        self.code = code
        self.desc = desc
        self.credits = credit
        self.offered = offered
        self.requisites = self.parse_requisites(requisites)
        
    def parse_requisites(self, requisites: str) -> dict:
        if re.search("Prerequisites", requisites):
            requisites = requisites[15:]
            requisites = re.sub(' +|\(|\)', '', requisites)
            and_list = requisites.split("and")
            or_list = []
            for i in and_list:
                or_list.append(i.split("or"))
            
            reqs = {"Prerequisites" : []}
            for i in or_list:
                and_list = []
                if type(i) == list:
                    for course in i:
                        if re.match("\w{4}-\d*", course):
                            and_list.append(course)
                else:
                    if re.match("\w{4}-\d*", course):
                        and_list.append(course)
                
                reqs["Prerequisites"].append(and_list)
            
            print(reqs)
            return reqs
                       
        elif re.search("Co-requisites", requisites):
            requisites = requisites[15:]
            requisites = re.sub(' +|\(|\)', '', requisites)
            and_list = requisites.split("and")
            or_list = []
            for i in and_list:
                or_list.append(i.split("or"))
            
            reqs = {"Co-requisites" : []}
            for i in or_list:
                and_list = []
                if type(i) == list:
                    for course in i:
                        if re.match("\w{4}-\d*", course):
                            and_list.append(course)
                else:
                    if re.match("\w{4}-\d*", course):
                        and_list.append(course)
                
                reqs["Co-requisites"].append(and_list)
            
            print(reqs)
            return reqs     
        # elif re.search("Co-requisites", requisites):

    def __str__(self) -> str:
        return f"{self.name} ({self.code}), credits: {self.credits}, times offered: {self.offered}, {self.requisites}"
    
    def __repr__(self) -> str:
        # return f"{self.name} ({self.code})\n{self.desc}\ncredits: {self.credits}, times offered: {self.offered}, requisites: {self.requisites}"
        return f"{self.name}"