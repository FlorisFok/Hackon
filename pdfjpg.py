from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import sys
import os


file = r"C:\Users\s147057\Documents\Validaters\one.pdf"
input_file = 'diditwork'
print("Start")
pages = convert_from_path(file, 500)
print("Done")

inp = PdfFileReader(file, "rb")
page = inp.getPage(0)

wrt = PdfFileWriter()
wrt.addPage(page)

r = io.BytesIO()
wrt.write(r)

images = convert_from_bytes(r.getvalue())
images[0].save(input_file+".png")

print("Done, your cover photo has been saved as {}.".format(input_file+".png"))
r.close()


for page in pages:
    area = (400, 400, 800, 800)
    cropped_img = page.crop(area)
    cropped_img.show()
    print(type(page))
    page.save('out.jpg', 'JPEG')

print(len(pages))
