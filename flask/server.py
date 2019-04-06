import os
from flask import request
from flask import render_template
from flask import Flask
from werkzeug.utils import secure_filename
from PIL import Image as PImage
import pytesseract
from pdf2image import convert_from_path, convert_from_bytes
from PyPDF2 import PdfFileWriter, PdfFileReader
from flask import jsonify
import io
import sys
app = Flask(__name__)

def convert_pdf(filename, output_path):
    input_file = 'diditwork'
    print("Start")
    print("Done")

    inp = PdfFileReader(filename, "rb")
    page = inp.getPage(7)

    wrt = PdfFileWriter()
    wrt.addPage(page)

    r = io.BytesIO()
    wrt.write(r)

    image_filename = os.path.splitext(os.path.basename(filename))[0]
    image_filename = '{}.png'.format(image_filename)
    image_filename = os.path.join(output_path, image_filename)

    images = convert_from_bytes(r.getvalue())
    images[0].save(image_filename)


    print("Done, your cover photo has been saved as {}.".format(input_file+".png"))
    r.close()
    return (image_filename)

def crop_image(filename, area = (400, 400, 800, 800)):
    png_img = PImage.open(filename)
    cropped_img = png_img.crop(area)
    return cropped_img

# def convert_pdf(filename, output_path, resolution=300):
#     """ Convert a PDF into images.

#         All the pages will give a single png file with format:
#         {pdf_filename}-{page_number}.png

#         The function removes the alpha channel from the image and
#         replace it with a white background.
#     """
#     all_pages = Image(filename=filename, resolution=resolution)
#     for i, page in enumerate(all_pages.sequence):
#         with Image(page) as img:
#             img.format = 'png'
#             img.background_color = Color('white')
#             img.alpha_channel = 'remove'

            # image_filename = os.path.splitext(os.path.basename(filename))[0]
            # image_filename = '{}-{}.png'.format(image_filename, i)
            # image_filename = os.path.join(output_path, image_filename)

#             img.save(filename=image_filename)
#             return (image_filename)



def read_image(filename):
    im = PImage.open(filename)
    text = pytesseract.image_to_string(im, lang = 'eng')
    data = text.split("\n")
    total = 0
    print(text)
    print("---------- PARSED DATA ----------")

    for d in data[:-2]:
        euro = float(d.replace(',', '').replace(' ', ''))
        total += euro
        print(euro)
    print("-------------- +")
    totalpic = float(data[-1].replace(',', '').replace(' ', ''))
    print("Parsed total:		", totalpic)
    print("Calculated total:	", total)

    if (total == totalpic):
        print("Correct!")
    else:
        print("Incorrect!")

@app.route('/')
def hello():
    return render_template('layout.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        filename = secure_filename(f.filename)
        path = os.path.join('/Users/oscar/Development/EY-hackathon/Hackon/flask/uploads', filename)
        f.save(path)
        filen = convert_pdf(path, "./static")
        return render_template('next.html', img=filen)

@app.route("/image", methods=["POST"])
def check():
    x1 = request.form.get("x1")
    y1 = request.form.get("y1")
    x2 = request.form.get("x2")
    y2 = request.form.get("y2")
    filename = request.form.get("imgsrc")
    if x1 and y1 and x2 and y2 and filename:
        print(x1, " ", y1, " ", x2, " ", y2, " ", filename)
        area = (int(x1), int(y1), int(x2), int(y2))
        image = crop_image(filename, area)
        path = os.path.join('/Users/oscar/Development/EY-hackathon/Hackon/flask/uploads', "out.png")
        image.save(path, "PNG")
        read_image(path)
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})