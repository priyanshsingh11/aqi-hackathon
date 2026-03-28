import docx
import os

path = 'c:/Users/Priyansh Singh/Desktop/aqi_hackathon/aqi_hackathon_data/AQI_Hackathon_Problem_Statement.docx'

if os.path.exists(path):
    doc = docx.Document(path)
    for para in doc.paragraphs:
        print(para.text)
else:
    print("File not found.")
