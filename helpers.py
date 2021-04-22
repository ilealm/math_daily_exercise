from mde.models import User

def userToCreate(form):
    return User(
                username = form.username.data,
                email_address = form.email_address.data,
                password = form.password1.data,
                parent_email_address = form.parent_email_address.data     )
