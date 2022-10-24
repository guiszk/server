import os
import psutil
from flask import Flask, flash, request, redirect, render_template, send_from_directory, send_file
from werkzeug.utils import secure_filename

app=Flask(__name__)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'mp3', 'mp4', 'm4a', 'mkv', 'mov', 'ogg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    with open(os.path.join(path, 'messages.lst'), 'r') as f:
        messages = [i for i in f.read().split('<<MESSAGE>>') if i.strip() != '']
    fan = psutil.disk_usage(path="/")
    diskinfo = str(round(fan.used/1000000000, 2)) + '/' + str(round(fan.total/1000000000, 2)) + ' GB (' + str(fan.percent) + '%)'
    filesvfs = os.stat(UPLOAD_FOLDER)
    filesinfo = str(round(filesvfs.st_size/1024, 2)) + 'KB'
    messvfs = os.stat(os.path.join(path, 'messages.lst'))
    messinfo = str(round(messvfs.st_size/1024, 2)) + 'KB'
    listd = os.listdir(UPLOAD_FOLDER)
    listd.sort(key=lambda s: os.path.getmtime(os.path.join(UPLOAD_FOLDER, s)))
    return render_template('index.html', diskinfo=diskinfo, messinfo=messinfo, filesinfo=filesinfo, result=messages[::-1], files=listd[::-1])


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect('/')
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)

@app.route('/text', methods=['POST'])
def save_text():
    if(request.method == 'POST'):
        if(request.values.get('text')):
            with open(os.path.join(path, 'messages.lst'), 'a') as f:
                f.write('<<MESSAGE>>\n')
                f.write(request.values.get('text'))
                f.write('\n')
            return redirect('/')
        else:
            flash('No text to submit.')
            return redirect('/')

@app.route('/get/<path:filename>',methods = ['GET','POST'])
def get_file(filename):
    try:
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=False)
