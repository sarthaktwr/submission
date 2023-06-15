import PyPDF2
import json
import re
with open('test.pdf', 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    
    document = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        document += page.extract_text()
heading_pattern = re.compile(r'(?:\n|^)([A-Z][A-Za-z\s]+)\n')

headings = re.findall(heading_pattern, document)

headings_ = []
with open('headings.json', 'w') as f:
    for heading in headings:
        headings_.append(heading)
    json.dump(headings_, f, indent = 4)