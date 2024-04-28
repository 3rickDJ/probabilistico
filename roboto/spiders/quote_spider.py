#Librerias necesarias para el funcionamiento del programa
import scrapy
from scrapy.loader import ItemLoader
from roboto.items import RobotoItem

#Clase para el spider
class QuotesSpider(scrapy.Spider):
    #Nombre del spider
    name = "quotes"
    #Url inicial
    start_urls = ["http://quotes.toscrape.com/"]
    #Profundidad maxima
    custom_settings = {
            'DEPTH_LIMIT': 1
            }
    #Funcion que se encarga de parsear la pagina, recibe la respuesta y la profundidad
    def parse(self, response, depth=1):
        # Si es una pagina html la guardamos
        if response.headers.get("Content-Type", b"").startswith(b"text/html"):
            l = ItemLoader(item=RobotoItem(), response=response)              #item es una instancia de RobotoItem que se encarga de guardar los datos
            l.add_value("url", response.url)                                  #Obtenemos la url de la pagina
            l.add_value("content", response.text)                             #Obtenemos el contenido de la pagina
            # l.add_value("depth", depth)                                       #Obtenemos la profundidad de la pagina
            item = l.load_item()                                              #Cargamos el item
            self.log(f"Got successful response from {response.url} 📀  {depth}") #Imprimimos en consola que se obtuvo una respuesta exitosa
            yield item                                                      #Retornamos el item
            # depth_limit = self.settings.getint("DEPTH_LIMIT")



        # scrapy.shell.inspect_response(response, self)
        # import pudb; pudb.set_trace()
        #page guarda el numero de pagina en la que estamos
        page = response.url.split("/")[-2]
        #filename guarda el nombre del archivo que se va a guardar
        filename = f"quotes-{page}.html 🍉  {depth}"
        # Path(filename).write_bytes(response.body)H
        self.log(f"Saved file {filename}")
        hrefs = response.xpath("//a/@href").extract()
        for href in hrefs: #Para cada href en hrefs
            url = response.urljoin(href) #Obtenemos la url y la guardamos en url
            if depth >= self.settings.getint("DEPTH_LIMIT"): #Si la profundidad es mayor o igual a la profundidad maxima
                yield scrapy.Request(url=url, callback=self.parse_last) #Retornamos la url y la funcion parse_last
            else:
                #Retornamos la url y la funcion parse con la profundidad aumentada en 1
                yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(depth=depth+1))
#Funcion que se encarga de parsear la ultima pagina, recibe la respuesta
    def parse_last(self, response):
        # Si el contenido de la pagina es html y empiza con text/html entonces guardamos la pagina
        if response.headers.get("Content-Type", b"").startswith(b"text/html"):
            #Obtenemos la profundidad maxima
            max_depth = self.settings.getint("DEPTH_LIMIT")
            l = ItemLoader(item=RobotoItem(), response=response)
            l.add_value("url", response.url)
            l.add_value("content", response.text)
            # l.add_value("depth", max_depth)
            #Retornamos el item
            self.log(f"Got successful response from {response.url} 📀  {max_depth}")
            item = l.load_item()
            yield item
