from hashlib import sha256

def get_salted_password_hash(uname, base_password):
    
    # salting done with the username

    base_password_hash = sha256(base_password.encode()).hexdigest()
    salted_hash = sha256((uname + base_password_hash).encode()).hexdigest()

    return salted_hash