import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
import socket

app = Flask(__name__)
mysql = MySQL(app)

app.config['MYSQL_DATABASE_USER'] = 'flask'
app.config['MYSQL_DATABASE_PASSWORD'] = 'flask'
app.config['MYSQL_DATABASE_DB'] = 'smartfreezer'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

app.config['UPLOAD_FOLDER'] = 'static/img'
app.config['ALLOWED_EXTENSIONS'] = ('png', 'jpg', 'jpeg')

os.system('sudo chmod 604 /dev/hidraw1')

def get_data(sql, params=None):
    conn = mysql.connect()
    cursor = conn.cursor()
    print("getting data")
    try:
        print(sql)
        cursor.execute(sql, params)
    except Exception as e:
        print(e)
        return False

    result = cursor.fetchall()
    data = []
    for row in result:
        data.append(list(row))
    cursor.close()
    conn.close()

    return data


def set_data(sql, params=None):
    conn = mysql.connect()
    cursor = conn.cursor()
    print("Setting Data")
    try:
        cursor.execute(sql, params)
        conn.commit()
    except Exception as e:
        print(e)
        return False

    cursor.close()
    conn.close()

    return True


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def barcode_reader():
    hid = {4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm',
           17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y',
           29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ',
           45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';', 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'}

    hid2 = {4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M',
            17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y',
            29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ',
            45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':', 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'}
    fp = open('/dev/hidraw1', 'rb')
    ss = ""
    shift = False
    done = False
    while not done:
        buffer = fp.read(8)
        for c in buffer:
            if c > 0:
                if c == 40:
                    done = True
                    break
                if shift:
                    if c == 2:
                        shift = True
                    else:
                        ss += hid2[c]
                        shift = False
                else:
                    if c == 2:
                        shift = True
                    else:
                        ss += hid[c]
    return ss


@app.route('/')
def index():
    print('index')
    sql = 'select idproduct, name, amount, datediff(expirationdate, now()), comments, istemplate, i.* ' \
          'from product as p ' \
          'join icon as i on i.idicon = p.iconid ' \
          'where amount > 0'
    data = get_data(sql)
    print('got data')
    return render_template('content.html', title='Content', search_icon=True, fab=True, data=data)


@app.route('/search', methods=['POST', 'GET'])
def content_search():
    if request.method == 'POST':
        search = request.form['search']
        search = '%' + search + '%'
        sql = 'select idproduct, name, amount, datediff(expirationdate, now()), comments, istemplate, i.* ' \
              'from product as p ' \
              'join icon as i on i.idicon = p.iconid ' \
              'where amount > 0 and name like (%s)'
        data = get_data(sql, search)
        return render_template('content_search.html', no_title=True, back_icon=True, data=data)
    sql = 'select idproduct, name, amount, datediff(expirationdate, now()), comments, istemplate, i.* ' \
          'from product as p ' \
          'join icon as i on i.idicon = p.iconid ' \
          'where amount > 0'
    data = get_data(sql)
    return render_template('content_search.html', title='Search', no_title=True, back_icon=True, back_url=url_for('index'), data=data)


@app.route('/templates')
def templates():
    sql = 'select idproduct, name, amount, datediff(expirationdate, creationdate), comments, istemplate, i.* ' \
          'from product as p ' \
          'join icon as i on i.idicon = p.iconid ' \
          'where istemplate = 1'
    data = get_data(sql)
    return render_template('templates.html', title='Templates', search_icon=True, fab=True, data=data)


@app.route('/temperature')
def temperature():
    sql = 'select temp ' \
          'from settings ' \
          'limit 1'
    sql2 = 'select temp ' \
           'from temperature ' \
           'order by idtemperature desc ' \
           'limit 1'
    temp = get_data(sql)[0][0]
    current_temp = get_data(sql2)[0][0]
    current_temp = round(current_temp, 1)
    print(temp, current_temp)
    return render_template('temperature.html', title='Temperature', temp=temp, current_temp=current_temp)


@app.route('/temperature/minus')
def minus_temp():
    sql = 'update settings ' \
          'set temp = temp - 1'
    set_data(sql)
    return redirect(url_for('temperature'))


@app.route('/temperature/plus')
def plus_temp():
    sql = 'update settings ' \
          'set temp = temp + 1'
    set_data(sql)
    return redirect(url_for('temperature'))


@app.route('/settings', methods=['POST', 'GET'])
def settings():
    if request.method == 'POST':
        min_temp = request.form['min_temp']
        max_temp = request.form['max_temp']
        if 'pae' in request.form:
            pae = 1
        else:
            pae = 0
        if 'pe' in request.form:
            pe = 1
        else:
            pe = 0
        if 'shoppinglist' in request.form:
            shoppinglist = 1
        else:
            shoppinglist = 0
        sql = 'update settings ' \
              'set mintemp = (%s), maxtemp = (%s), pae = (%s), pe = (%s), shoppinglist = (%s)'
        set_data(sql, (min_temp, max_temp, pae, pe, shoppinglist))
        return redirect(url_for('index'))
    sql = 'select * ' \
          'from settings ' \
          'limit 1'
    data = get_data(sql)[0]
    return render_template('settings.html', title='Settings', check_icon=True, info_icon=True, data=data)


@app.route('/info')
def info():
    ip = get_ip_address()
    return render_template('info.html', title='Info', back_icon=True, back_url=url_for('settings'), ip=ip)


@app.route('/product/<id>')
def product(id):
    sql = 'select idproduct, name, amount, datediff(expirationdate, now()), comments, istemplate, i.* ' \
          'from product as p ' \
          'join icon as i on i.idicon = p.iconid ' \
          'where idproduct = (%s)'
    params = id
    data = get_data(sql, params)[0]
    print(data)
    return render_template('product.html', title=data[1], delete_icon=True, edit_icon=True, back_icon=True, back_url=url_for('index'), plus_minus_buttons=True, data=data)


@app.route('/add_amount/<id>')
def add_amount(id):
    sql = 'update product ' \
          'set amount = amount + 1 ' \
          'where idproduct = (%s)'
    set_data(sql, id)
    return redirect(url_for('product', id=id))


@app.route('/minus_amount/<id>')
def minus_amount(id):
    sql = 'update product set amount = amount - 1 where idproduct = (%s)'
    set_data(sql, id)
    return redirect(url_for('product', id=id))


@app.route('/delete_product/<id>')
def delete_product(id):
    sql = 'select istemplate from product where idproduct = (%s)'
    is_template = get_data(sql, id)[0][0]
    print(is_template)
    if is_template == 1:
        print('updating')
        sql = 'update product set amount = 0 where idproduct = (%s)'
        set_data(sql, id)
    else:
        print('deleting')
        sql = 'delete from product where idproduct = (%s)'
        set_data(sql, id)
    return redirect(url_for('index'))


@app.route('/edit_product/<id>', defaults={'imgid': None}, methods=['POST', 'GET'])
@app.route('/edit_product/<id>/<imgid>', methods=['POST', 'GET'])
def edit_product(id, imgid):
    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']
        date_added = request.form['date_added']
        expiration_date = request.form['expiration_date']
        comments = request.form['comments']
        if imgid:
            sql = 'update product ' \
                  'set name = (%s), amount = (%s), creationdate = (%s), expirationdate = date_add(now(), interval %s day), iconid = (%s), comments = (%s) ' \
                  'where idproduct = (%s)'
            set_data(sql, (name, amount, date_added, expiration_date, imgid, comments, id))
        else:
            sql = 'update product ' \
                  'set name = (%s), amount = (%s), creationdate = (%s), expirationdate = date_add(now(), interval %s day), comments = (%s) ' \
                  'where idproduct = (%s)'
            set_data(sql, (name, amount, date_added, expiration_date, comments, id))
        return redirect(url_for('product', id=id))
    img=None
    if imgid:
        sql_img = 'select * ' \
                  'from icon ' \
                  'where idicon = (%s)'
        img = get_data(sql_img, imgid)[0]
    sql = 'select idproduct, name, amount, creationdate, datediff(expirationdate, now()), iconid, comments, istemplate, i.* ' \
          'from product as p ' \
          'join icon as i on i.idicon = p.iconid ' \
          'where idproduct = (%s)'
    params = id
    data = get_data(sql, params)[0]
    print(data)
    return render_template('edit_product.html', title='Edit product', check_icon=True, back_icon=True, back_url=url_for('product', id=id), icon_back_url='edit_product', data=data, img=img)


@app.route('/add_product')
def add_product():
    return render_template('select_method.html', title='Add product', back_icon=True, back_url=url_for('index'))


@app.route('/add_product_manually', defaults={'imgid': '1'}, methods=['POST', 'GET'])
@app.route('/add_product_manually/<imgid>', methods=['POST', 'GET'])
def add_product_manually(imgid):
    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']
        date_added = request.form['date_added']
        expiration_date = request.form['expiration_date']
        comments = request.form['comments']
        sql = 'insert into product (name, amount, creationdate, expirationdate, iconid, comments) ' \
              'values ((%s), (%s), (%s), date_add(now(), interval %s day), (%s), (%s))'
        set_data(sql, (name, amount, date_added, expiration_date, imgid, comments))
        return redirect(url_for('index'))
    img = None
    if imgid:
        sql_img = 'select * ' \
                  'from icon ' \
                  'where idicon = (%s)'
        img = get_data(sql_img, imgid)[0]
    return render_template('edit_product.html', title='Add product', check_icon=True, back_icon=True, img=img, back_url=url_for('add_product'), icon_back_url=('add_product_manually'))


@app.route('/add_product_template')
def add_product_template():
    sql = 'select idproduct, name, amount, datediff(expirationdate, now()), comments, istemplate, i.* ' \
          'from product as p join icon as i on i.idicon = p.iconid ' \
          'where isTemplate = 1 and amount = 0'
    data = get_data(sql)
    return render_template('add_product_template.html', title='Choose template', back_icon=True, back_url=url_for('add_product'), data=data)


@app.route('/add_product_template/<id>', defaults={'imgid': None}, methods=['POST', 'GET'])
@app.route('/add_product_template/<id>/<imgid>', methods=['POST', 'GET'])
def add_product_template_id(id, imgid):
    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']
        date_added = request.form['date_added']
        expiration_date = request.form['expiration_date']
        comments = request.form['comments']
        if imgid:
            sql = 'update product ' \
                  'set name = (%s), amount = (%s), creationdate = (%s), expirationdate = date_add(now(), interval %s day), iconid = (%s), comments = (%s) ' \
                  'where idproduct = (%s)'
            set_data(sql, (name, amount, date_added, expiration_date, imgid, comments, id))
        else:
            sql = 'update product ' \
                  'set name = (%s), amount = (%s), creationdate = (%s), expirationdate = date_add(now(), interval %s day), comments = (%s) ' \
                  'where idproduct = (%s)'
            set_data(sql, (name, amount, date_added, expiration_date, comments, id))
        return redirect(url_for('product', id=id))
    img = None
    if imgid:
        sql_img = 'select * ' \
                  'from icon ' \
                  'where idicon = (%s)'
        img = get_data(sql_img, imgid)[0]
    sql = 'select idproduct, name, amount, creationdate, datediff(expirationdate, now()), iconid, comments, istemplate, i.* ' \
          'from product as p ' \
          'join icon as i on i.idicon = p.iconid ' \
          'where idproduct = (%s)'
    params = id
    data = get_data(sql, params)[0]
    data[2] = 1
    return render_template('edit_product.html', title='Add product', check_icon=True, back_icon=True, back_url=url_for('add_product_template'), icon_back_url='add_product_template_id', data=data, img=img)


@app.route('/add_product_barcode')
def add_product_barcode():
    return render_template('add_product_barcode.html', title='Add product', back_icon=True, back_url=url_for('add_product'), barcode_scanner=True)

@app.route('/scan_product')
def scan_product():
    barcode = barcode_reader()
    return redirect(url_for('add_product_barcode_id', id=barcode))


@app.route('/add_product_barcode/<id>', defaults={'imgid': None}, methods=['POST', 'GET'])
@app.route('/add_product_barcode/<id>/<imgid>', methods=['POST', 'GET'])
def add_product_barcode_id(id, imgid):
    barcode = id
    img = None
    if imgid:
        sql_img = 'select * ' \
                  'from icon ' \
                  'where idicon = (%s)'
        img = get_data(sql_img, imgid)[0]
    sql = 'select idproduct, name, amount, creationdate, datediff(expirationdate, now()), iconid, comments, istemplate, i.* ' \
          'from product as p ' \
          'join icon as i on i.idicon = p.iconid where barcode = (%s)'
    data = get_data(sql, barcode)
    if not data:
        print('Geen data')
        if request.method == 'POST':
            name = request.form['name']
            amount = request.form['amount']
            date_added = request.form['date_added']
            expiration_date = request.form['expiration_date']
            comments = request.form['comments']
            sql = 'insert into product (name, amount, creationdate, expirationdate, iconid, comments, barcode) ' \
                  'values ((%s), (%s), (%s), date_add(now(), interval %s day), (%s), (%s), (%s))'
            set_data(sql, (name, amount, date_added, expiration_date, imgid, comments, barcode))
            return redirect(url_for('index'))
        return render_template('edit_product.html', title='Add product', check_icon=True, back_icon=True,
                               back_url=url_for('add_product'), back_url_id=barcode,
                               icon_back_url='add_product_barcode_id', img=img)
    else:
        print('Barcode in database')
        data = data[0]
        if request.method == 'POST':
            name = request.form['name']
            amount = request.form['amount']
            date_added = request.form['date_added']
            expiration_date = request.form['expiration_date']
            comments = request.form['comments']
            sql = 'select idproduct from product where barcode = (%s)'
            id = get_data(sql, barcode)[0][0]
            if imgid:
                sql = 'update product ' \
                      'set name = (%s), amount = (%s), creationdate = (%s), expirationdate = date_add(now(), interval %s day), iconid = (%s), comments = (%s) ' \
                      'where barcode = (%s)'
                set_data(sql, (name, amount, date_added, expiration_date, imgid, comments, barcode))
            else:
                sql = 'update product ' \
                      'set name = (%s), amount = (%s), creationdate = (%s), expirationdate = date_add(now(), interval %s day), comments = (%s) ' \
                      'where barcode = (%s)'
                set_data(sql, (name, amount, date_added, expiration_date, comments, barcode))
            return redirect(url_for('product', id=id))
        return render_template('edit_product.html', title='Add product', check_icon=True, back_icon=True,
                               back_url=url_for('add_product'), back_url_id=barcode, icon_back_url='add_product_barcode_id',
                               data=data, img=img)


@app.route('/edit_template/<id>', defaults={'imgid': None}, methods=['POST', 'GET'])
@app.route('/edit_template/<id>/<imgid>', methods=['POST', 'GET'])
def edit_template(id, imgid):
    if request.method == 'POST':
        name = request.form['name']
        expiration_time = request.form['expiration_time']
        comments = request.form['comments']
        if imgid:
            sql = 'update product ' \
                  'set name = (%s), expirationdate = date_add(creationdate, interval %s day), iconid = (%s), comments = (%s) ' \
                  'where idproduct = (%s)'
            set_data(sql, (name, expiration_time, imgid, comments, id))
        else:
            sql = 'update product ' \
                  'set name = (%s), expirationdate = date_add(creationdate, interval %s day), comments = (%s) ' \
                  'where idproduct = (%s)'
            set_data(sql, (name, expiration_time, comments, id))
        return redirect(url_for('templates', id=id))
    img = None
    if imgid:
        sql_img = 'select * ' \
                  'from icon ' \
                  'where idicon = (%s)'
        img = get_data(sql_img, imgid)[0]
        print(img)
    sql = 'select idproduct, name, datediff(expirationdate, creationdate), comments, i.* ' \
          'from product as p ' \
          'join icon as i on i.idicon = p.iconid ' \
          'where idproduct = (%s) and isTemplate = 1'
    params = id
    data = get_data(sql, params)[0]
    return render_template('edit_template.html', title='Edit template', delete_icon_template=True, check_icon=True, back_icon=True, back_url=url_for('templates'), data=data, img=img)


@app.route('/add_template')
def add_template():
    sql = 'select idproduct, name, amount, datediff(expirationdate, now()), comments, istemplate, i.* ' \
          'from product as p ' \
          'join icon as i on i.idicon = p.iconid ' \
          'where isTemplate = 0'
    data = get_data(sql)
    return render_template('add_template.html', title='Choose product', back_icon=True, back_url=url_for('templates'), data=data)


@app.route('/add_template/<id>')
def add_template_id(id):
    sql = 'update product ' \
          'set isTemplate = (%s) ' \
          'where idproduct = (%s)'
    params = (1, id)
    set_data(sql, params)
    return redirect(url_for('templates'))


@app.route('/delete_template/<id>')
def delete_template(id):
    sql = 'update product ' \
          'set isTemplate = (%s) ' \
          'where idproduct = (%s)'
    params = (0, id)
    set_data(sql, params)
    return redirect(url_for('templates'))


@app.route('/edit_icon/<back_url>/<back_url_id>', methods=['POST', 'GET'])
@app.route('/edit_icon/<back_url>', defaults={'back_url_id': None}, methods=['POST', 'GET'])
def edit_icon(back_url, back_url_id):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No files part')
            print('No file part')
            return render_template(request.url)
        file = request.files['file']
        print('icon')
        if file.filename == '':
            flash('No file specified')
            print('No file file')
            return render_template(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(path)
            file.save(path)
            sql = 'insert into icon (iconpath) values (%s)'
            set_data(sql, os.path.join(app.config['UPLOAD_FOLDER'].rsplit('/', 1)[1], filename))
            return redirect(request.url)
    sql = 'select * ' \
          'from icon'
    data = get_data(sql)
    print(data)
    return render_template('edit_icon.html', title='Choose icon', back_icon=True, data=data, back_url=url_for(back_url, id=back_url_id), icon_back_url=back_url, back_url_id=back_url_id, upload_form=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
