from passlib.context import CryptContext

pw_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_pw(plain_pw:str)->str:
    """hash password for DB

    Args:
        plain_pw (str): user password in plain

    Returns:
        str: the hashed pw for DB
    """

    return pw_context.hash(secret=plain_pw)


def verify_pw(plain_pw:str, db_pw:str)->bool:
    """check if password is valid

    Args:
        plain_pw (str): password plain to test
        db_pw (str): hashed password from db

    Returns:
        bool: True if valid else False
    """

    return pw_context.verify(secret=plain_pw, hash=db_pw)
