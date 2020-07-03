# parsebyocr
Parse scanned uniform documents to distinct files, each page as file, named by id detected from each page using OCR.
For example, you have scanned several idcards of employees and now you have to parse them into distinct documents with filenames being the id numbers, so that you will be able to find tham later using Windows Explorer search.
This project aims to do this work.
User indicates where on the first page exists a numeric data that will serve as a name of ech page. The project will try to detect this numeric value with OCR. The user can adjust image properties to get the best OCR result.
Than scanned file is divided into files with each file being one page. Each file is named according to the numeric id detected in that page.
Note that scanned document should be PDF file.
The project uses several third party applications:
1. Tesseract and pytesseract which do the OCR magic. Information can be found here: https://pypi.org/project/pytesseract/
2. pdf2image which does the conversion of pdf pages to images. Information can be found here: https://pypi.org/project/pdf2image/
3. Pillow which does the magic of image manipulation. Information can be found here: https://pypi.org/project/Pillow/

Enjoy.
