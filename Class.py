class Class:
    def __init__(self, name: str, code: str, desc: str, credit: int, offered: list, requisites: str) -> None:
        self.name = name
        self.code = code
        self.desc = desc
        self.credits = credit
        self.offered = offered
        self.requisites = requisites

    def __str__(self) -> str:
        return f"{self.name} ({self.code}), credits: {self.credits}, times offered: {self.offered}, requisites: {self.requisites}"
    
    def __repr__(self) -> str:
        # return f"{self.name} ({self.code})\n{self.desc}\ncredits: {self.credits}, times offered: {self.offered}, requisites: {self.requisites}"
        return f"{self.name}"
    