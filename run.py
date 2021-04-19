from mde import app

if __name__ == '__main__':
    # (debug=True) so that I don't need to 
    # put it in command, and I can see the changes 
    # WO re-starting the server
    app.run(debug=True)