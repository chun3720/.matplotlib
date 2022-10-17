
from batterydataextractor import Document


address = "https://pubs.rsc.org/en/content/articlehtml/2022/sc/d2sc03980j?page=search.html"

f = open(address, 'rb')

doc = Document.from_file(f)