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

def open_web(url,browser):
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

def click_carrer(title,browser):
    browser.wait_until_element_is_visible(title)
    browser.click_element(title)
    
def get_information(browser,title,data):
    element_info = "xpath://td[@align='left']//p"
    browser.wait_until_page_contains_element(element_info)
    informacion = browser.find_elements(element_info)
    texto = "\n".join([info.text for info in informacion])
    duracion,objetivo,salida = regex_info(texto)
    data.append({
        "title":title,
        "duracion":duracion,
        "objetivo":objetivo,
        "salida":salida
    })
    
    return data

def career_list(browser):
    element_title = "xpath://td[@align='left']//a"
    browser.wait_until_page_contains_element(element_title)
    titles = browser.find_elements(element_title)
    
    return titles

def minimal_task():
    url = "https://www.carrerasytrabajos.com.ar/carreras-lista/carreras-en-argentina-donde-estudiar-universidades.html"
    browser = Selenium()
    start = False
    title_start = "Abogacia"
    title_end ="yoga"
    data = []
    try:
        open_web(url,browser)
        titles=career_list
        for i in range(len(titles)):
            if(titles[i].text == title_start):
                start = True
            if(start):
                click_carrer(titles[i],browser)
                get_information(browser,titles[i].text,data)
                time.sleep(10)
            if(titles[i].text == title_end):
                start = False
    except TimeoutError as te:
        print("Error: A TimeoutError occurred: ",te)
    except Exception as e:
        print("Error: An unexpected error occurred: ", e)
    finally:
        browser.close_all_browsers()
    
    
if __name__ == "__main__":
    minimal_task()
