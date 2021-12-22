
from re import sub
from werkzeug.utils import redirect, secure_filename
import settings
from settings import app, db
import models

# ------------------------- Home Page Settings Starts here -------------------- ]]
@app.route('/', methods=["GET", "POST"])
def index():
    if settings.request.method == "POST":
        name = settings.request.form['name']
        email = settings.request.form['email']
        subject = settings.request.form['subject']
        message = settings.request.form['message']
        info = models.Mailer(name=name, email=email, subject=subject, message=message)
        db.session.add(info)
        db.session.commit()
        email = email.split(",")

        msg = settings.Message(
                    subject,
                    sender =app.config['MAIL_USERNAME'],
                    recipients = email
                            )
        msg.body = message
        msg.html= msg.body
        settings.mail.send(msg)
        
    fetch=models.Maildb.query.all()

    return settings.render_template('index.html', getinfo1=fetch)


@app.route('/downdb', methods=['GET', 'POST'])
def exportexcel():
    data = models.Maildb.query.all()
    datalist = []
    # datalist.append(['Name','Email'])
    for d in data:
        datalist.append([d.mdb_name,d.mdb_email])

    df = settings.pd.DataFrame(datalist)
    df = df.rename({0: 'Name', 1: 'Email'}, axis=1)
    filename = "static/excel/maildb.xlsx"
    writer = settings.pd.ExcelWriter(filename)
    df.to_excel(writer, sheet_name='maildb',index=False)
    writer.save()

    return settings.send_file(filename)



@app.route('/uploaddb', methods=["GET", "POST"])
def uploaddb():
    if settings.request.method == "POST":
        file = settings.request.files['mail_db']
        fname= 'static/excel/'+secure_filename(file.filename)
        file.save(fname)
        df = settings.pd.read_excel(fname)
        ################## APPEND STARTS CODE ######################
        fetchemail = models.Maildb.query.all()
        flag=0
        for index in df.index:
            flag=0
            for mails in fetchemail:
                if mails.mdb_email == df['Email'][index]:
                    flag=1
                    break
            if flag == 0:
                ################## APPEND ENDS CODE ######################
                info = models.Maildb(mdb_name=df['Name'][index], mdb_email=df['Email'][index])
                db.session.add(info)
                db.session.commit()
    return redirect('/maildb')


@app.route('/maildb', methods=["GET", "POST"])
def maildata():
    if settings.request.method == "POST":
        mdb_name = settings.request.form['mdb_name']
        mdb_email = settings.request.form['mdb_email']
        information = models.Maildb(mdb_name=mdb_name, mdb_email=mdb_email)
        db.session.add(information)
        db.session.commit()
    fetch = models.Maildb.query.all()

    return settings.render_template('maildb.html', getinfo=fetch)

@app.route('/delmdb/<int:id>', methods=["GET", "POST"])
def delmdb(id):
    fetch = models.Maildb.query.filter_by(id=id).first()
    db.session.delete(fetch)
    db.session.commit()

    return settings.redirect("/maildb")

if __name__ == '__main__':
   app.run(debug=True)

