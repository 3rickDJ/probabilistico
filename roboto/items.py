#Librerias necesarias para el funcionamiento del programa
import scrapy
from bs4 import BeautifulSoup
from itemloaders.processors import MapCompose, TakeFirst
import re

#Esta funcion recibe el html de la pagina y lo convierte en texto
def extract_text(html):
    #Obtenemos el texto lo convertimos en minusculas y lo limpiamos
    soup = BeautifulSoup(html, "html.parser").get_text().lower().strip()
    words = re.split(r"[^a-z0-9]+", soup)
    return words



#Esta funcion es la que se encarga de crear el item para el pipeline
class RobotoItem(scrapy.Item):
    #url obtiene la url de la pagina
    url = scrapy.Field(
            output_processor = TakeFirst()
            )
    #content obtiene el contenido de la pagina
    content = scrapy.Field(
            output_processor = MapCompose(extract_text)
            )
    #depth obtiene la profundidad de la pagina
    # depth = scrapy.Field(
    #         output_processor = TakeFirst()
    #         )
