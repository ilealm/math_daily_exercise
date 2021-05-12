

# Dependencies

Database:
pip install flask-sqlalchemy

To hash passwords:
pip install flask_bcrypt

To log user in session
pip install flask_login

Bootstrap icons
npm i bootstrap-icons

.env File
pip install python-dotenv

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

# LOGIN_V2 branch
TODO: create template/login.html : done
TODO: create loginForm : done
TODO: create mgnt on route login_page : done


# play branch

TODO: create play.html: select tables to practice, number of games
TODO: redisign register and login layout: done


# play_backend branch
TODO: Fix range to to 10: done
TODO: Add message "needs to be an integer" to amount

TODO: in select to, select 10 as default: done
TODO: validation on from less than to: done
TODO: set cursor on 1st input: done
TODO: play logic
TODO: show results
TODO: save game
TODO: reestart game
TODO: 

TODO: auto-fase flash windows