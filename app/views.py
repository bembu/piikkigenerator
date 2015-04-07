from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from app import models, db, app, forms, mail
from flask.ext.mail import Message, Mail
from config import ADMINS, HOST_ROOT
import json
import datetime

@app.route("/", methods=['POST', 'GET'])
def index():
    form = forms.CredentialsForm()

    if form.validate_on_submit():
    #if request.method == 'POST':
        #TODO: validation doesn't currently work!!
        #TODO: if the email is entered again (and already verified), clear the printed variable

        name = form.name.data.strip()
        surname = form.surname.data.strip()
        email = form.email.data.strip()

        u = models.Aasi(name=name, surname=surname, email=email)
        print u
        db.session.add(u)
        db.session.commit()

        _send_verification_mail(u)

        return redirect(url_for('form_success'))

    return render_template('index.html', form=form)

@app.route("/verify/<verification_str>")
def verify_email(verification_str):
    u = models.Aasi.query.filter_by(verification_string=verification_str).first()
    #TODO: ensure that verification str is unique
    #TODO: check the mail address also
    if u:
        u.verified = True
        db.session.commit()
        return "verified!"

    return "not verified!"

@app.route("/success", methods=['GET'])
def form_success():
    # TODO: Create a success template
    return redirect(url_for('debug'))

@app.route("/pdf")
def generate_pdf():
    import StringIO
    # TODO: think of a way to do this nicely

    from flask_weasyprint import HTML, render_pdf

    #users = models.Aasi.query.all()
    users = models.Aasi.query.filter_by(verified=True)

    now = datetime.datetime.now().strftime('%d.%m.%Y');

    html = render_template('piikki.html', users=users, now=now)

    return render_pdf(HTML(string=html))
    return render_template('piikki.html', users=users, now=now)

    # TODO: send the pdf to all the admins
    # TODO: update revision

@app.route("/debug")
def debug():
    users = models.Aasi.query.all()
    return jsonify(json_list = [u.as_dict() for u in users])

def _send_verification_mail(aasi):
    # TODO: modify the layout of the email
    msg = Message('Askipiikki verification', sender=ADMINS[0])
    msg.add_recipient(aasi.email)
    msg.html = "Hello tuusi muusi. <br /> <a href='" + HOST_ROOT + url_for('verify_email', verification_str=aasi.verification_string) + "'>verifioi</a>"
    mail.send(msg)
