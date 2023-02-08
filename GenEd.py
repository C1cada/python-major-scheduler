from Class import Class

class GenEd(Class):
    def __init__(self,desc: str, credit: int) -> None:
        super().__init__("General Education", "", desc, credit, "Annual", "")