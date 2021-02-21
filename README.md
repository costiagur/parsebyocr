# Parse_by_Ocr
Parse scanned uniform documents to distinct files, each page,or several pages, as files, named by some text detected from each page using OCR.
User can choose several places to pich from the scanned image. the first one will be used an name of the pdf file created.
The default choise is that every page is a file. However, user can set stepping between pages (one number) or an array of values, delimited by comma, which represent pages to cut at.
Note that scanned document should be PDF file.
The project uses several third party applications:
1. Tesseract and pytesseract which do the OCR magic. Information can be found here: https://pypi.org/project/pytesseract/
2. pdf2image which does the conversion of pdf pages to images. Information can be found here: https://pypi.org/project/pdf2image/
3. Pillow which does the magic of image manipulation. Information can be found here: https://pypi.org/project/Pillow/
4. PyPDF2 which splits and merges scanned pdf files. Information can be found here: https://pypi.org/project/PyPDF2/

Enjoy.
