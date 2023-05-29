from RPA.Browser.Selenium import Selenium
import mysql.connector
import time
import re

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
    
def regex_info(info):
    duracion_regex = re.search(r'Duración aproximada de la carrera: (.+?)\n', info)
    duracion = duracion_regex.group(1) if duracion_regex else ""
    
    objetivos_regex = re.search(r'Objetivos de la carrera:(.+?)(Campo Ocupacional - Salida Laboral:|Fuente)', info, re.DOTALL)

    if objetivos_regex:
        objetivos = objetivos_regex.group(1)
        objetivos = re.sub(r'\n+', '\n', objetivos)  # Esto limpia los saltos de línea adicionales
    else:
        print("No se encontraron los objetivos.")


    # Para obtener la información después de "Campo Ocupacional - Salida Laboral:"
    salida_laboral_regex = re.search(r'Salida Laboral:(.+?)(Fuente)', info, re.DOTALL)
    salida_laboral = salida_laboral_regex.group(1).strip() if salida_laboral_regex else ""
    
    
    return duracion,objetivos,salida_laboral
def get_information(url,browser):

    element_info = "xpath://td[@align='left']//p"
    browser.wait_until_page_contains_element(element_info)
    titles = browser.find_elements(element_info)
    texto = "\n".join([title.text for title in titles])
    duracion,objetivo,salida = regex_info(texto)
   
def click_career(url,title_start,title_end):
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
            browser.wait_until_element_is_visible(titles[i])
            browser.click_element(titles[i])
            time.sleep(10)
        if(titles[i].text == title_end):
            start = False
    return data
def minimal_task():
    url = "https://www.carrerasytrabajos.com.ar/CARRERAS/abogacia.html"
    #click_career(url,"Abogacía","Yoga")
    get_information(url)

if __name__ == "__main__":
    minimal_task()
