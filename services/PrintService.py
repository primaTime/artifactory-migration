
class PrintService:

    @staticmethod
    def print(content: str):
        print(content)

    @staticmethod
    def h1(content: str):
        stars = "".join((["*"] * len(content)))
        PrintService.print(f"\n\n********{stars}********")
        PrintService.print(f"******* {content} *******")
        PrintService.print(f"********{stars}********\n")

    @staticmethod
    def h2(content: str):
        PrintService.print(f"\n>>>>>>>> {content}")

    @staticmethod
    def line():
        PrintService.print("**************************************************")

    @staticmethod
    def error(content: str):
        PrintService.print(f"ERROR: {content}")