import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import json
from PIL import Image, ImageDraw
from flask import render_template
import subprocess

UPLOAD_IMG_FOLDER = 'imgs'
ALLOWED_EXTENSIONS = set(['tif'])
MODEL_NAME = 'save.ckpt-130000'
parts_path = 'parts'
all_fields = ['aftertax', 'commission', 'tripdate', 'traveller', 'voucherdate', 'duedate', 'pretax', 'pstreet', 'pzip', 'pcity', 'cname', 'cstreet', 'czip', 'currency', 'vatpercent', 'ccity']

app = Flask(__name__)

app.config['UPLOAD_IMG_FOLDER'] = UPLOAD_IMG_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
           
def run_model(sample_name):
    cmd = 'cd /home/anna/tensorbox/ && python evaluate.py --weights /home/anna/tensorbox/exit/detect_full_2017_05_01_10.03/save.ckpt-220000 --gpu 0 --test_boxes data/%s.json --img_out norm' % (sample_name)
    subprocess.call(cmd, shell=True)
        
           
def make_inp(filename):
    inp = [{'image_path': filename, 'rects':[{'x1':0,'x2':1,'y1':0,'y2':1, 'label':1}]}]
    sample_name = os.path.basename(filename).split('.')[0]
    outfile = open('/home/anna/tensorbox/data/' + sample_name +'.json', 'w')
    json.dump(inp, outfile)
    return sample_name

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    '''
    img_filename = 'imgs/00000005535937_Seite_1_Bild_0001.tif'
    sample_name = make_inp(img_filename)
    run_model(sample_name)
    '''
    if request.method == 'POST':
        file = request.files['img']
        if file and allowed_file(file.filename):
            img_basename = secure_filename(file.filename)
            img_filename = os.path.join(app.config['UPLOAD_IMG_FOLDER'], secure_filename(file.filename))
            file.save('/home/anna/tensorbox/data/' + img_filename)
            img_longname = '/home/anna/tensorbox/data/' + img_filename
            sample_name = make_inp(img_filename)
            run_model(sample_name)
            res_name = os.path.join('model', sample_name + '.json')
            return render_template('simple.html', id_value = sample_name)
            #return process_image(img_filename, res[0]['rects'])
            #return res[0]['image_path']
            #return redirect(url_for('model_result',
                                    #filename=res_name))
            
    return '''
    <!doctype html>
    <title>Detector</title>
    <h1>Select an image</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=img>
         <input type=submit value=Load>
    </form>
    '''
    
from flask import send_from_directory

@app.route('/result/<filename>')
def uploaded_file(filename):
    return send_from_directory('model',
                               filename+'.json')

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response
                               
if __name__ == '__main__':
    app.run(host="localhost", port=8080)
    