# Parse_by_Ocr
Parse scanned documents to distinct files, each page, or several pages, as files, named according to the text detected from each page using OCR.
User can choose several spots to pick from the scanned image. User can choose which spots will serve as parsing conditins and which will serve as names.
spots are viewd relative to anchors, which are texts or images that are expected to return in each document. For example and invoice might have an invoice number and a title "Invoice number". The title would serve as an anchor and the number is the data being searched.
Note that scanned document should be a PDF file.

Activation file is servhttp.py

The project uses several third party applications and python packages: Tesseract and pytesseract which do the OCR magic, pdf2image, Pillow, PyPDF2 and Opencv-python.

Enjoy.
