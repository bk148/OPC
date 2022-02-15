# Scraper
## Goal:
An application to retrieve the following data at the time of execution:
 - product page url 
 - universal product code (upc) 
 - title 
 - price including tax 
 - price excluding tax 
 - number available
 - product description 
 - category 
 - review rating 
 - image url
 - book image

## Getting started:
**Note**: Make sure python3 is installed in your machine : `python -V; if not please check https://www.python.org/downloads/:
 1. Clone the repository <URL_REPO> on the terminal or command prompt
 2. Create a virtual environment with "venv"  
	 - cd scaper :  to access the folder 
	 - python -m venv ***environment name*** : to create the virtual environment - exemple: `py -m venv env` 
3. Activate the virtual environment:
	for windows:
	- ***environment name***\Scripts\activate - ex: `envbooks\Scripts\activate`
4. Install the packages with pip: `pip install -r requirements.txt`	
6. Run the program with : `python .\src\main.py`

NB: on windows hosts sometimes `python` is aliased by `py`

***Without any connection problem at the end of the program you should have:***

 - an **"csv"** folder under scraped_data/csv folder*** which contains all_books infos scraped
 - an **"images"** folder under scraped_date/images folder which contains 1000 images since there are 1000 books books on the gallery/site
