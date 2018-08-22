from requests import get
from bs4 import BeautifulSoup
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import requests
import smtplib
from email.mime.text import MIMEText

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close
    device.close
    retstr.close()
    return text

text = convert_pdf_to_txt("Splendor_Card_List_with_Pics.pdf").split("\n")
print(text)
print(len(text))
cards = []
for i in range(5):
    j = 150 * i
    for k in range(18):
        c = [1,1,1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3]
        card = [text[j+2].lower(), str(c[k]), str(c[k]), text[j+k+21], text[j+k+55], text[j+k+93], text[j+k+131], text[j+k+112], text[j+k+74]]
        cards.append(card)

with open("cards.txt", "w") as f:
    for l in cards:
        f.write(' '.join(map(str,l)))
        f.write("\n")
