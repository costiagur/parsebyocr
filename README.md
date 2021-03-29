# Parse_by_Ocr
Parse scanned uniform documents to distinct files, each page,or several pages, as files, named by some text detected from each page using OCR.
User can choose several places to pick from the scanned image. The first one will be used an name of the pdf file created.
For more precise matching user can pick additional places in the document will serve as anchors relative to which the equired data is placed. For example and invoice might have an invoice number and a title "Invoice number". The title would serve as an anchor and the number is the data being searched.
The default choise is that every page is a file. However, user can set stepping between pages (one number) or an array of values, delimited by comma, which represent pages to cut at.
Note that scanned document should be a PDF file.
The project uses several third party applications and python packages: Tesseract and pytesseract which do the OCR magic, pdf2image, Pillow, PyPDF2 and Opencv-python.

Enjoy.
