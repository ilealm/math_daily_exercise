

# Dependencies

Database:
pip install flask-sqlalchemy

To hash passwords:
pip install flask_bcrypt

To log user in session
pip install flask_login

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mde.db'

# Start Server

python run.py

#




# TODO List
# LOGIN branch
TODO: hash password: done
TODO: log the new user to the session: done
TODO: have parent psw optional: done
TODO: align register form components: done
# REGISTER branch
TODO: fix closing flasing windows: done
TODO: add logout route: done
TODO: add logout funcionality: done
TODO: show username when logged: done
TODO: add custom bootstraps: done
TODO: change login ctrol to logut: done
TODO: refactor register_page route: done
TODO: add decorated login_required to routes: DONE

TODO: clear register form