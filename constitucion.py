from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json
import os
import errno

def scrape_constitution(start_url, end_url):
    current_url = start_url
    data = []

    while True:
        print(f"Obteniendo datos de: {current_url}")
        response = requests.get(current_url)
        if response.status_code != 200:
            print(f"Error al obtener la página: {current_url}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        p_tags = soup.find_all('p')  # Find all <p> tags

        for i, p in enumerate(p_tags):
            a_tag = p.find('a')  # Find <a> tag inside <p> tag
            
            articulo = None
            if a_tag:
                articulo = a_tag.text 
            contenido = p.text  # Get the text inside <p> tag
            data.append({'url': current_url,  'index': i, 'articulo': articulo, 'contenido': contenido, 'date_taken': datetime.now().isoformat()})

        # Find the "next" link
        next_link = soup.find('a', text='Siguiente')

        if current_url == end_url:
            break
        
        if next_link:
            next_url = next_link.get('href')
            if not next_url.startswith('http://www.secretariasenado.gov.co/senado/basedoc/'):
                next_url = 'http://www.secretariasenado.gov.co/senado/basedoc/' + next_url
            current_url = next_url
        else:
            break
    return data

# URL inicial y final
start_url = "http://www.secretariasenado.gov.co/senado/basedoc/codigo_civil.html"
end_url = "http://www.secretariasenado.gov.co/senado/basedoc/constitucion_politica_1991_pr015.html"

# Ejecutar el scraper
constitution_data = scrape_constitution(start_url, end_url)

try:
    # Use an absolute file path
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/constitution_data.json')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(constitution_data, f, ensure_ascii=False, indent=4)
except IOError as e:
    # print error and exit 1
    print("I/O error({0}): {1}".format(e.errno, e.strerror))
    exit(1)
