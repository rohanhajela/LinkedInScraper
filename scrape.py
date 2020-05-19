from excelOutput import excelOutput
from scraperUtils import *

username = None
password = None

def getLogin():
	global username
	global password
	#Asking for Linkedin Authentication
	username = input("Enter Linkedin email: ")
	print()
	password = input("Enter Linkedin password: ")
	print()

def main():
	
	if (username == None or password == None):
		getLogin()


	#Get Company Input
	cur_company = input("Enter Company Name: ")
	print()

	#Asking for titles list input for LinkedIn Filter (comma-seperated)
	print("Enter titles as comma-seperated list (ie. Director, Growth, Vice President, SVP).")
	print("RECOMMENDED: DON'T INPUT THAT MANY TITLES OTHERWISE YOU WILL BURN THROUGH YOUR LINKEDIN SEARCHES.")
	title_input = input("Enter Titles (Recommended - 3): ")
	print()
	titles = title_input.split(", ")

	#Number of Pages
	page_total = input("Enter number of pages you want scraped (3 is recommended): ")
	print()

	#File Name
	file_name = input("Enter desired file name as excel file (ie. kahoot.xlsx): ")
	print()

	#Confirmation
	print("Please confirm if all this information is correct:")
	print("Company: " + cur_company)
	print("Titles: " + ', '.join(titles))
	print("Pages: " + page_total)
	print("File Name: " + file_name)
	confirm = input("Enter y if information is correct: ")
	print()

	if confirm.lower() == "y":
		excel_file = excelOutput(file_name)
		execute(username, password, titles, cur_company, page_total, excel_file)
	else:
		main()

main()

