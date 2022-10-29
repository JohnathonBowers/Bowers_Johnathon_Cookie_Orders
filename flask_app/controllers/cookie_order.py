from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.cookie import Cookie
from flask_app.config.mysqlconnection import connectToMySQL

@app.route('/')
def home():
    return redirect('/cookies')

@app.route('/cookies')
def r_get_cookie_orders():
    return render_template('all_orders.html', cookies = Cookie.get_all_cookies())

@app.route('/cookies/new')
def r_new_cookie_order():
    return render_template('new_order.html')

@app.route('/cookies/new_order', methods=['POST'])
def f_new_cookie_order():
    if not Cookie.validate_order(request.form):
        session['name'] = request.form['name']
        session['cookie_type'] = request.form['cookie_type']
        session['box_nums'] = request.form['box_nums']
        return redirect('/cookies/new')
    Cookie.add_cookie(request.form)
    if session:
        session.pop('name')
        session.pop('cookie_type')
        session.pop('box_nums')
    return redirect ('/cookies')

@app.route('/cookies/edit/<int:id>')
def r_cookie_edit(id):
    dictionary = {'id': id}
    return render_template("edit_order.html", order = Cookie.get_one(dictionary))

@app.route('/cookies/update', methods=['POST'])
def f_update_cookie_order():
    print(request.form)
    id = request.form['id']
    if not Cookie.validate_order(request.form):
        return redirect(f'/cookies/edit/{id}')
    Cookie.udpate_order(request.form)
    return redirect ('/cookies')

@app.route('/cookies/delete/<int:id>')
def r_cookie_destroy(id):
    dictionary = {'id': id}
    Cookie.destroy_order(dictionary)
    return redirect ('/cookies')