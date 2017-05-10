import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import json
from PIL import Image, ImageDraw
from flask import render_template
from flask.ext.images import Images
import subprocess

UPLOAD_IMG_FOLDER = 'imgs'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'tif'])
MODEL_NAME = 'save.ckpt-130000'
parts_path = 'parts'
all_fields = ['aftertax', 'commission', 'tripdate', 'traveller', 'voucherdate', 'duedate', 'pretax', 'pstreet', 'pzip', 'pcity', 'cname', 'cstreet', 'czip', 'currency', 'vatpercent', 'ccity']

app = Flask(__name__)

app.secret_key = 'monkey'
images = Images(app)
app.config['UPLOAD_IMG_FOLDER'] = UPLOAD_IMG_FOLDER

def load_dict():
    f = open('reference_dict_new.txt', 'r')
    reference_dict = {x.strip().split(',')[0]:x.strip().split(',')[1] for x in f}
    return reference_dict

def process_image(path, c_info):
    f = open('output.txt', 'w')
    try:
        im = Image.open(path)
    except:
        return 'failed to open your image bro ' + path
    for c in c_info:
        this_crop = (c['x1'] - 7, c['y1'] -7, c['x2']+7, c['y2']+7)
        imm = im.crop([int(x) for x in this_crop])
        imm.save(os.path.join(app.config['PARTS_FOLDER'], str(c['label'])) + '.png')
    return 'success'

def filter_pred(filename):
    fields = dict()
    results = []
    preds = json.load(open(filename, 'r'))[0]['rects']
    for bbx in preds:
        if bbx['label'] not in fields:
            fields[bbx['label']] = [bbx]
        else:
            fields[bbx['label']] += [bbx]
    for label, bbx in fields.items():
        results += [sorted(bbx, key=lambda x: x['score'])[-1]]
    return results

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
    
def fill_parts(path):
    im = Image.open('templates/no_det.png')
    for i in range(len(all_fields) + 1):
       if not os.path.exists(os.path.join(app.config['PARTS_FOLDER'], str(i) + '.png')):
         im.save(os.path.join(app.config['PARTS_FOLDER'], str(i) + '.png'))

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
            if not os.path.exists(os.path.join(parts_path,sample_name)): os.makedirs(os.path.join(parts_path,sample_name))
            app.config['PARTS_FOLDER'] = os.path.join(parts_path,sample_name)
            process_image(img_longname, filter_pred(res_name))
            fill_parts(parts_path)
            reference_dict = load_dict()
            parts_urls = [url_for('get_part', partname=str(load_dict()[x]) + '.png', imname=sample_name) for x in all_fields]
            return render_template('det.html', ims = parts_urls, im_big = url_for('uploaded_file', filename = img_basename[:-3] + "jpg"))
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

@app.route('/parts/<imname>/<partname>')
def get_part(partname, imname):
    return send_from_directory(app.config['PARTS_FOLDER'],partname)

@app.route('/imgs/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_IMG_FOLDER'],
                               filename)

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response
                               
if __name__ == '__main__':
    app.run(host="localhost", port=8080)
    