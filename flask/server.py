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
import re
app = Flask(__name__)

def convert_pdf(filename, output_path, pagenumber):
    input_file = 'diditwork'
    print("Start")
    print("Done")

    inp = PdfFileReader(filename, "rb")
    page = inp.getPage(pagenumber)

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

def pos_neg_calc(list):
    display_dict = {
        'succes': True,
        'total': 0,
        'totalparsed': 0,
        'records': []
    }
    for e in list[:-1]:
        if e:
            f = e.replace(',', '').replace(' ', '').replace('.', '')
            if ("(" in f and ")" in f) or "-" in f:
                f = f.replace('(', '').replace(')', '').replace('-', '')
                display_dict['total'] -= int(f)
                display_dict['records'].append(-int(f))
            else:
                display_dict['total'] += int(f)
                display_dict['records'].append(int(f))
    last = list[-1]
    if last:
        l = last.replace(',', '').replace(' ', '').replace('.', '')
        if ("(" in f and ")" in f) or "-" in f:
            l = l.replace('(', '').replace(')', '').replace('-', '')
            display_dict['totalparsed'] = -int(l)
        else:
            display_dict['totalparsed'] = int(l)
    return display_dict

def read_image(filename, point=False):
    im = PImage.open(filename)
    text = pytesseract.image_to_string(im, lang = 'eng')

    # digits = []
    # if len(numbers) > 0:
    #     if point:
    #         for num in numbers[:-1]:
    #             try:
    #                 total += float(num[0])+float(num[1])*0.1
    #             except:
    #                 total += float(num[0])
    #     else:
    #         for num in numbers[:-1]:
    #             number = ''
    #             for s in num:
    #                 number += s
    #             total += int(number)
    #             digits.append(int(number))
            # for s in numbers[-1]:
            #     totalpic += s
    display_dict = pos_neg_calc(text.split('\n'))
    print(text)
    print("---------- PARSED DATA ----------")
    for d in display_dict['records']:
        print(d)
    print("-------------- +")
    print("Parsed total:		", display_dict['totalparsed'])
    print("Calculated total:	", display_dict['total'])
    print("-----------------------------------")
    print("Posneg:")
    print()
    # data = text.split("\n")
    # total = 0
    # print(text)
    # print("---------- PARSED DATA ----------")

    # for d in data[:-2]:
    #     euro = float(d.replace(',', '').replace(' ', ''))
    #     total += euro
    #     print(euro)
    # print("-------------- +")
    # totalpic = float(data[-1].replace(',', '').replace(' ', ''))
    # print("Parsed total:		", totalpic)
    # print("Calculated total:	", total)

    # if (total == totalpic):
    #     print("Correct!")
    # elif ((total - 1) == totalpic or (total + 1) == totalpic):
	#     print("Rounding error!")
    # else:
    #     print("Incorrect!")
    return display_dict

@app.route('/')
def hello():
    return render_template('layout.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        pagenumber = request.form['pagenum']
        if not pagenumber:
            pagenumber = 1
        else:
            pagenumber = int(pagenumber)
        pagenumber -= 1
        filename = secure_filename(f.filename)
        path = os.path.join('/home/canelaguila/Downloads/', filename)
        f.save(path)
        filen = convert_pdf(path, "./static", pagenumber)
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
        area = (int(x1) * 2, int(y1) * 2, int(x2) * 2, int(y2) * 2)
        image = crop_image(filename, area)
        path = os.path.join('/home/canelaguila/Downloads/', "out.png")
        image.save(path, "PNG")
        display_dict = read_image(path)
        return jsonify(display_dict)
    else:
        return jsonify({"success": False})