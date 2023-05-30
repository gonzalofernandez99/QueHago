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
    
    objetivos_regex = re.search(r'Objetivos de la carrera(.+?)(Salida Laboral:|¿DÓNDE ESTUDIAR)', info, re.DOTALL)

    # asignamos un valor por defecto a objetivos
    objetivos = ''

    if objetivos_regex:
        objetivos = objetivos_regex.group(1)
        objetivos = re.sub(r'\n+', '\n', objetivos)  # Esto limpia los saltos de línea adicionales
    else:
        print("No se encontraron los objetivos.")


    # Para obtener la información después de "Campo Ocupacional - Salida Laboral:"
    salida_laboral_regex = re.search(r'Salida Laboral:(.+?)(¿DÓNDE ESTUDIAR)', info, re.DOTALL)
    salida_laboral = salida_laboral_regex.group(1).strip() if salida_laboral_regex else ""
    
    return duracion, objetivos, salida_laboral


def click_carrer(title,browser):
    browser.wait_until_element_is_visible(title)
    browser.click_element(title)
    
def get_information(browser,title,data):

    element_info = "xpath://td[@align='left']//p"
    time.sleep(10)
    browser.is_element_enabled(element_info,10)
    informacion = browser.find_elements(element_info)
    texto = "\n".join([info.text for info in informacion])
    duracion,objetivo,salida = regex_info(texto)
    data.append({
        "title":title,
        "duracion":duracion,
        "objetivo":objetivo,
        "salida":salida
    })
    
    browser.go_back()
    return data

def career_list(browser):
    element_title = "xpath://td[@align='left']//a"
    browser.wait_until_page_contains_element(element_title)
    titles = browser.find_elements(element_title)
    
    return titles

def test_get_information():
    browser = Selenium()
    url = "https://www.carrerasytrabajos.com.ar/CARRERAS/abogacia.html"
    title = "Abogacia"
    data = []
    
    open_web(url,browser)
    get_information(browser,title,data)
    print(data)
    

def minimal_task():
    url = "https://www.carrerasytrabajos.com.ar/carreras-lista/carreras-en-argentina-donde-estudiar-universidades.html"
    browser = Selenium()
    start = False
    title_start = "Abogacía"
    title_end = "Yoga"
    data = []
    try:
        open_web(url, browser)
        titles_elements = career_list(browser)
        
        # Guardamos los textos de los títulos en una lista
        titles = [title.text for title in titles_elements]

        for title in titles:
            if title == title_start:
                start = True
            if start:
                # Usamos el texto del título para encontrar y hacer clic en el elemento del título
                title_element = browser.find_element(f"link:{title}")
                click_carrer(title_element, browser)
                print(title)
                time.sleep(15)
                get_information(browser, title, data)
                time.sleep(15)
            if title == title_end:
                start = False

        print[data]

    except TimeoutError as te:
        print("Error: A TimeoutError occurred: ", te)
    except Exception as e:
        print("Error: An unexpected error occurred: ", e)
    finally:
        browser.close_all_browsers()



    
    
if __name__ == "__main__":
    minimal_task()
    #test_get_information()
