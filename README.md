# parsebyocr
Parse scanned uniform documents to distinct files, each page as file, named by id detected from each page using ocr
The project aims to parse scanned documents gathered in one pdf file. The file is parsed by page, therefore all the pages should be uniform documents. User indicates where the number that can serve as id for each page is written. OCR will attempt to detect that number and set is as a name for each page that will be parsed. The result should be several pdf documents, each one with its own name that is the id detected in that page.
