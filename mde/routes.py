from mde import app

@app.route('/')
@app.route('/home')
def home_page():
    return 'I am in home_page'