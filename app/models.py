from app import db
import random
import string

BASIC_CHARS = string.ascii_letters + string.digits

class Aasi(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64), index=True)
    surname = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), index=True, unique=False) #TODO: muuta unique:True
    #phone = db.Columnd(db.String(16))

    verified = db.Column(db.Boolean, index=True)
    printed = db.Column(db.Boolean, index=True)

    verification_string = db.Column(db.String(24), index=True)

    def __init__(self, **kwargs):
        super(Aasi, self).__init__(**kwargs)
        self.verified = False
        self.printed = False
        self.verification_string = self.generate_email_string()


    def generate_email_string(self):
        return ''.join(random.choice(BASIC_CHARS) for i in xrange(24))

    def __repr__(self):
        return '<Aasi {} {} | {} | verified: {} | printed {}>'.format(self.name.encode('utf-8'), self.surname.encode('utf-8'), self.email, self.verified, self.printed)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
