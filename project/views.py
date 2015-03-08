#-*- coding:utf-8 -*-

import MySQLdb
import string

from flask import Flask, g, request, render_template, redirect, url_for, session, jsonify

from uploader import Uploader

app = Flask(__name__)
app.secret_key = 'PS#yio`%_!((f_or(%)))s'
# app.config.from_object('config')

from sae.const import (MYSQL_HOST, MYSQL_HOST_S,
    MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
)

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

@app.before_request
def before_request():
    g.db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS,
                           MYSQL_DB, port=int(MYSQL_PORT), charset='utf8')

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'): g.db.close()



@app.route('/')
@app.route('/index')
def index():
    c = g.db.cursor()
    c.execute("select titleId, titleName, contentSimple, date from blog")
    blogs = list(c.fetchall())
    blogs.reverse()
    return render_template('index.html', blogs=blogs)

@app.route('/blog/<int:titleId>')
def blog(titleId):
    c = g.db.cursor()
    c.execute("select titleName, contentDetail, date from blog where titleId = '%s'" % titleId)
    blogs = list(c.fetchall())
    blog = blogs[0]
    return render_template('blog.html', blog=blog)

@app.route('/save_blog', methods=['GET', 'POST'])
def save_blog():
    if request.method == 'POST':
        contentDetail = request.form.get('content')
        titleName = request.form.get('title')
        if len(contentDetail) < 140:
            contentSimple = contentDetail
        else:
            contentSimple = contentDetail[0:130]
        c = g.db.cursor()
        c.execute("insert into blog (titleName, contentSimple, contentDetail) values(%s, %s, %s)", (titleName, contentSimple, contentDetail ))
        return jsonify(content=contentDetail)
    else:
        return redirect(url_for('index'))

@app.route('/edit', methods=['GET', 'POST'])
@app.route('/edit/<int:titleId>', methods=['GET', 'POST'])
def edit():
    return render_template('edit.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        c = g.db.cursor()
        c.execute("insert into students (stuId, password, email) values(%s, %s, %s)", (request.form['stuId'], request.form['password'], request.form['email'] ))
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        c = g.db.cursor()
        stuId = request.form['stuId']
        password = str(request.form['password'])
        c.execute("select password from students where stuId = '%s'" % stuId)
        msgs = c.fetchall()
        if not msgs :
            return redirect(url_for('login'))
        if not msgs[0][0] == password:
            return redirect(url_for('login'))
        # session['logged_in'] = True
        return redirect(url_for('index'))
    return render_template('login.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'),500

@app.route('/upload/', methods=['GET', 'POST', 'OPTIONS'])
def upload():
    """UEditor文件上传接口
    config 配置文件
    result 返回结果
    """
    mimetype = 'application/json'
    result = {}
    action = request.args.get('action')
    # 解析JSON格式的配置文件
    with open(os.path.join(app.static_folder, 'ueditor', 'php',
                           'config.json')) as fp:
        try:
            # 删除 `/**/` 之间的注释
            CONFIG = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
        except:
            CONFIG = {}
    if action == 'config':
        # 初始化时，返回配置文件给客户端
        result = CONFIG
    elif action in ('uploadimage', 'uploadfile', 'uploadvideo'):
        # 图片、文件、视频上传
        if action == 'uploadimage':
            fieldName = CONFIG.get('imageFieldName')
            config = {
                "pathFormat": CONFIG['imagePathFormat'],
                "maxSize": CONFIG['imageMaxSize'],
                "allowFiles": CONFIG['imageAllowFiles']
            }
        elif action == 'uploadvideo':
            fieldName = CONFIG.get('videoFieldName')
            config = {
                "pathFormat": CONFIG['videoPathFormat'],
                "maxSize": CONFIG['videoMaxSize'],
                "allowFiles": CONFIG['videoAllowFiles']
            }
        else:
            fieldName = CONFIG.get('fileFieldName')
            config = {
                "pathFormat": CONFIG['filePathFormat'],
                "maxSize": CONFIG['fileMaxSize'],
                "allowFiles": CONFIG['fileAllowFiles']
            }
        if fieldName in request.files:
            field = request.files[fieldName]
            uploader = Uploader(field, config, app.static_folder)
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'
    elif action in ('uploadscrawl'):
        # 涂鸦上传
        fieldName = CONFIG.get('scrawlFieldName')
        config = {
            "pathFormat": CONFIG.get('scrawlPathFormat'),
            "maxSize": CONFIG.get('scrawlMaxSize'),
            "allowFiles": CONFIG.get('scrawlAllowFiles'),
            "oriName": "scrawl.png"
        }
        if fieldName in request.form:
            field = request.form[fieldName]
            uploader = Uploader(field, config, app.static_folder, 'base64')
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'
    elif action in ('catchimage'):
        config = {
            "pathFormat": CONFIG['catcherPathFormat'],
            "maxSize": CONFIG['catcherMaxSize'],
            "allowFiles": CONFIG['catcherAllowFiles'],
            "oriName": "remote.png"
        }
        fieldName = CONFIG['catcherFieldName']
        if fieldName in request.form:
            # 这里比较奇怪，远程抓图提交的表单名称不是这个
            source = []
        elif '%s[]' % fieldName in request.form:
            # 而是这个
            source = request.form.getlist('%s[]' % fieldName)
        _list = []
        for imgurl in source:
            uploader = Uploader(imgurl, config, app.static_folder, 'remote')
            info = uploader.getFileInfo()
            _list.append({
                'state': info['state'],
                'url': info['url'],
                'original': info['original'],
                'source': imgurl,
            })
        result['state'] = 'SUCCESS' if len(_list) > 0 else 'ERROR'
        result['list'] = _list
    else:
        result['state'] = '请求地址出错'
    result = json.dumps(result)
    if 'callback' in request.args:
        callback = request.args.get('callback')
        if re.match(r'^[\w_]+$', callback):
            result = '%s(%s)' % (callback, result)
            mimetype = 'application/javascript'
        else:
            result = json.dumps({'state': 'callback参数不合法'})
    res = make_response(result)
    res.mimetype = mimetype
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Headers'] = 'X-Requested-With,X_Requested_With'
    return res
