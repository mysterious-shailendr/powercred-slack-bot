import requests
from ...core.manager import Manager

class LeaveTracker():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Leave Tracker App"
        self.version = "0.0.1"
        self.description = "For tracking leaves"
        self.manager = Manager()
    
    async def get_leaves(self):
        print(f"Using {self.name} - V.{self.version}")
        message = "Here you go, Leaves Data: \n\n"
        url = self.manager.APP_SCRIPT_URL
        print(f"Fetching data from {url}")
        response = requests.get(url)

        if response.status_code == 200:
            response_data = response.json()  
            tech_data = response_data["tech"]
            bizsales_data = response_data["bizsales"]
            print("Leaves Received data successfully:")
        else:
            return "", 404
        
        message += f"1. Tech Team Leaves:\n"

        markdown_table = f"```\n"
        for row in tech_data:
            markdown_table += f"| {str(row['Member']).ljust(9)} | AM : {str(row['Leaves']['AM']).rjust(3)} | PM : {str(row['Leaves']['PM']).rjust(3)} | AA : {str(row['Leaves']['AA']).rjust(3)} | SL : {str(row['Leaves']['SL']).rjust(3)} |\n"
        markdown_table += "```\n\n"
        message += markdown_table

        message += f"2. Business + Sales (BizSales) Team Leaves:\n"
        markdown_table = f"```\n"
        for row in bizsales_data:
            markdown_table += f"| {row['Member'].ljust(9)} | AM : {str(row['Leaves']['AM']).rjust(3)} | PM : {str(row['Leaves']['PM']).rjust(3)} | AA : {str(row['Leaves']['AA']).rjust(3)} | SL : {str(row['Leaves']['SL']).rjust(3)} |\n"
        markdown_table += "```\n"
        message += markdown_table

        return message, 200