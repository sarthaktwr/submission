from autoscraper import AutoScraper
from bs4 import BeautifulSoup
from spacy import displacy
from lxml import etree
import requests
import PyPDF2
import spacy
import json

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

response = requests.get('https://www.sec.gov/Archives/edgar/data/27904/000002790421000003/dal-20201231.htm')

if response.status_code == 200:
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    document = soup.get_text()
    doc = nlp(document)

    entities = []

    for ent in doc.ents:
        if ent.label_ in ['TIME', 'DATE', 'YEAR', 'PERCENT']:
            entities.append({'text':ent.text,
                            'label': ent.label_,
                            'start_char': ent.start_char,
                            'end_char': ent.end_char})

    colors = {'TIME': 'linear-gradient(90deg, #aa9cfc, #fc9ce7)', 
            'DATE': 'linear-gradient(90deg, #a6e3ff, #fc9ce7)', 
            'YEAR': 'linear-gradient(90deg, #ffadad, #fc9ce7)',
            'PERCENT': 'linear-gradient(90deg, #caffbf, #fc9ce7)'}
    options = {'ents': ['TIME', 'DATE', 'YEAR', 'PERCENT'], 'colors': colors}
    html = displacy.render(doc, style='ent', options=options, page=True)

    # Creates a html page with bouunding boxes on the entites
    with open('visualized_entities.html', 'w', encoding='utf-8') as outfile:
        outfile.write(html)
    # Creates a json file with the entities
    with open('entities.json', 'w') as f:
        json.dump(entities, f, indent = 4)    
    header = soup.select('body > div:nth-child(116) > span')
    header_text = header.get_text(strip=True) if header else None

    # Creates a json file with the header
    with open('headings.json', 'w') as g:
        json.dump(header_text, g, indent = 4) 
    
else:
    print('Failed to retrieve the webpage. Error:', response.status_code)
