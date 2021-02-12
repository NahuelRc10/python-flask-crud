import bcrypt

def get_password_crypt(password):
    #salt = os.environ.get("SECRET_PASS")
    salt = "secret"
    password = password.encode()
    salt = bcrypt.gensalt()
    password_crypt = bcrypt.hashpw(password, salt)
    return password_crypt