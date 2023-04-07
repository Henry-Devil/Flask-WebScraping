from .entities.User import User
from werkzeug.security import check_password_hash

class ModelUser():
    def __init__(self, db):
        self.db = db

    @classmethod
    def login(cls, db, user):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, username, password, fullname FROM user WHERE username = %s"
            cursor.execute(sql, (user.username,))
            row = cursor.fetchone()
            if row is not None and check_password_hash(row[2], user.password):
                found_user = User(row[0], row[1], row[2], row[3])
                return found_user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, username, fullname FROM user WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        