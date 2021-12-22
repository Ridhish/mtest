from settings import db


class Mailer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    subject = db.Column(db.String)
    message = db.Column(db.String)

class Maildb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mdb_name = db.Column(db.String)
    mdb_email = db.Column(db.String)
    