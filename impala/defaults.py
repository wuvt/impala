DEBUG = False
SECRET_KEY = "changeme"
SQLALCHEMY_DATABASE_URI = "postgresql://impala:changeme@localhost/impala"
SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
# smuggler:hunter2
M2M_USERS = {'smuggler': { 'access': ['librarian'], 'password_hash': '$pbkdf2-sha256$29000$g3Du3Zuz1hoDYKx1Tsm5tw$3hZ/b6WaNWaP4Q4zgIpL8nKjaTumekv5l97TkJx4ZBo'}}
ENABLE_OIDC = False
OIDC_CLOCK_SKEW = 60
#OIDC_CLIENT_ID = "impala"
#OIDC_ISSUER = "https://id.apps.wuvt.vt.edu"
#OIDC_LIBRARIAN_GROUPS = ['librarians']
