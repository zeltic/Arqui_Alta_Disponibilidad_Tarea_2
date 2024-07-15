import requests
from datetime import datetime
from xml.etree import ElementTree
# from .schemas import LeyCreate
from schemas import LeyCreate, LeyDetailCreate
import logging

def fetch_latest_laws():
    url = "https://www.leychile.cl/Consulta/obtxml?opt=3&cantidad=5"
    response = requests.get(url)
    response.raise_for_status()  # Asegurarse de que la solicitud fue exitosa

    # Parsear el XML
    root = ElementTree.fromstring(response.content)
    
    leyes = []
    for norma in root.findall('NORMA'):
        id_norma = norma.get('idNorma')
        titulo = norma.find('TITULO').text
        fecha_publicacion = norma.find('FECHA_PUBLICACION').text
        url = f"https://www.leychile.cl/Navegar?idNorma={norma.get('idNorma')}"
        
        ley = LeyCreate(
            id_norma=id_norma,
            titulo=titulo,
            fecha_publicacion=datetime.strptime(fecha_publicacion, "%Y-%m-%d").date(),
            url=url
        )
        leyes.append(ley)
    return leyes

def fetch_law_details(id_norma: str):
    url = f"https://www.leychile.cl/Consulta/obtxml?opt=7&idNorma={id_norma}"
    response = requests.get(url)
    response.raise_for_status()  # Asegurarse de que la solicitud fue exitosa
    
    root = ElementTree.fromstring(response.content)

    string_list = ""

    # logger = logging.getLogger('uvicorn.error')
    # logger.setLevel(logging.DEBUG)
    # logger.debug("".join([str_val.text.strip() for str_val in root.findall(".//{http://www.leychile.cl/esquemas}Texto")]))

    titulo = root.find(".//{http://www.leychile.cl/esquemas}TituloNorma").text
    fecha_promulgacion = root.find(".//{http://www.leychile.cl/esquemas}Identificador").get("fechaPromulgacion")
    fecha_publicacion = root.find(".//{http://www.leychile.cl/esquemas}Identificador").get("fechaPublicacion")
    texto = "".join([str_val.text.strip() for str_val in root.findall(".//{http://www.leychile.cl/esquemas}Texto")])

    ley_detail = LeyDetailCreate(
        id_norma=id_norma,
        titulo=titulo,
        fecha_promulgacion=datetime.strptime(fecha_promulgacion, "%Y-%m-%d").date(),
        fecha_publicacion=datetime.strptime(fecha_publicacion, "%Y-%m-%d").date(),
        texto=texto,
        url=url
    )
    
    return ley_detail