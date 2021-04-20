from flask import render_template


from mde import app

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')