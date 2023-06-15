from bs4 import BeautifulSoup
from spacy import displacy
import requests
import PyPDF2
import spacy
import json

nlp = spacy.load('en_core_web_sm')

with open('test.pdf', 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    
    document = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        document += page.extract_text()

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

with open('visualized_entities.html', 'w', encoding='utf-8') as outfile:
    outfile.write(html)

with open('entities.json', 'w') as f:
    json.dump(entities, f, indent = 4)