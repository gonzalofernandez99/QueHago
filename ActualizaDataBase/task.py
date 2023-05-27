from RPA.Browser.Selenium import Selenium
import mysql.connector
import time
def Database(host,user,password,database,data):
    cnx = mysql.connector.connect(
    host=host,    # El host donde está tu base de datos (en este caso, localhost)
    user=user,    # Tu usuario de MySQL
    password=password, # Tu contraseña de MySQL
    database=database   # El nombre de la base de datos que quieres utilizar
    )

    cursor = cnx.cursor()
 
    query = """INSERT INTO CareerInfo (Name, Duration, Goal) 
           VALUES (%s, %s, %s)"""
           
    for item in data:
        cursor.execute(query, item)

    cnx.commit()
    cursor.close()
    cnx.close()

def open_nytimes(url,browser):
    #Opens the browser and loads the provided URL.
    
    browser.open_available_browser(url)
    browser.maximize_browser_window()  

def get_information(url,title_start,title_end):
    browser = Selenium()
    browser.open_available_browser(url)
    browser.maximize_browser_window()  
    data = []
    element_title = "xpath://td[@align='left']//a"
    browser.wait_until_page_contains_element(element_title)
    titles = browser.find_elements(element_title)
    
    start = False
    for i in range(len(titles)):
        if(titles[i].text == title_start):
            start = True
        if(start):
            print("aca")
            
            browser.wait_until_element_is_visible(titles[i])
            browser.click_element(titles[i])
            time.sleep(10)
        if(titles[i].text == title_end):
            start = False
    return data
def minimal_task():
    url = "https://www.carrerasytrabajos.com.ar/carreras-lista/carreras-en-argentina-donde-estudiar-universidades.html"
    get_information(url,"Abogacía","Yoga")


if __name__ == "__main__":
    minimal_task()
