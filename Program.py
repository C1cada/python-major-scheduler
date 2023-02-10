class Program:
    def __init__(self, class_list: list, code: str, name: str, tables: list=[]) -> None:
        self.class_list = class_list
        self.code = code
        self.name = name
        self.tables = tables
        
    def __str__(self) -> str:
        return f"{self.name} ({self.code})"
    
    def __repr__(self) -> str:
        return f"{self.name} ({self.code})\n {self.class_list}\n {self.tables}"