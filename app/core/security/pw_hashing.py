from passlib.context import CryptContext

"""
⚠️ Installation correcte de bcrypt / passlib (important)

bcrypt et passlib peuvent être incompatibles selon les versions
(Python 3.12 notamment). Si les versions ne sont pas alignées,
l'application peut crasher AVANT même le hashing des mots de passe.

Procédure recommandée :

1) Désinstaller les versions existantes :
   pip uninstall passlib bcrypt -y

2) Installer des versions compatibles et stables :
   pip install passlib==1.7.4 bcrypt==4.1.2

3) Figer les versions dans requirements.txt pour éviter
   les bugs futurs liés aux mises à jour automatiques.

Ces versions sont utilisées couramment en production
avec FastAPI + SQLAlchemy.
"""

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
