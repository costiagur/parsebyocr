from PIL import Image
from pdf2image import convert_from_bytes
import os

def onepage(scanfile,dpirate=400):

    os.makedirs(name='demo',exist_ok=True)
    os.makedirs(name='drafts',exist_ok=True)
    
    images = convert_from_bytes(scanfile,dpi=dpirate,output_folder=".\\drafts",single_file=True)

    images[0].save('demo\\demopage.png')

    print('saved')

    for entry in os.scandir(r'.\drafts'):
        os.unlink(entry.path)
    #    

    return '1'  
#