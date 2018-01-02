from werkzeug.utils import secure_filename
from flask import Flask,render_template,jsonify,request,send_from_directory
import time
import os
import base64
import zipfile
from wtforms.fields import SubmitField
import docker

cli = docker.from_env()
app = Flask(__name__)
UPLOAD_FOLDER='upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt','png','jpg','xls','JPG','PNG','xlsx','gif','GIF','zip'])

# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

# 用于测试上传，稍后用到
@app.route('/',methods=['GET'],strict_slashes=False)
def indexpage():
    return render_template('index.html')


# 上传文件
@app.route('/',methods=['POST'],strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['file']  # 从表单的file字段获取文件，file为该表单的name值

    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = secure_filename(f.filename)
        ext = fname.rsplit('.',1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = str(unix_time)+'.'+ext  # 修改了上传的文件名
        #new_filename = '12'+'.'+ext  # 修改了上传的文件名

        f.save(os.path.join(file_dir, new_filename))  #保存文件到upload目录
        if ext == 'zip':
            z = zipfile.ZipFile(file_dir+'/'+new_filename,'r')
            for zz in z.namelist():
               z.extract(zz,'/var/lib/docker/volumes/python_test/_data')
        return render_template('result.html',var1=fname)
    else:
        return jsonify({"errno": 1001, "errmsg": u"failed"})

@app.route("/send_code", methods=['POST'])
def execute_code():
    create_container()
    output = create_container()
    return output


def create_container():
    py_container = cli.containers.run(
         image='python:3',
         command='python main.py',
         volumes={'python_test': {
                 'bind': '/opt',
                 'mode': 'rw',
                 }
             },
         name='hello_word_from_docker',
         working_dir='/opt'
    )

    for py_container in cli.containers.list(filters={'status':'exited'}):
          with open('/opt/py_log.txt', 'a') as f:
                  f.write(str(py_container.logs()))

    output = py_container.logs()
    py_container.remove()

    #return "From docker: {}".format(output.strip())
    return output

if __name__ == '__main__':
    app.run(debug=True, port=9990,host='0.0.0.0')
