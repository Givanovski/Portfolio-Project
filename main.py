from flask import Flask, render_template, request
import smtplib
import os
import gunicorn

OWN_EMAIL = os.environ.get("OWN_EMAIL")
OWN_PASSWORD = os.environ.get("OWN_PASSWORD")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        data = request.form
        send_mail(data["name"], data["email"], data["subject"], data["message"])
        return render_template("index.html", msg_sent=True)
    return render_template("index.html", msg_sent=False)


def send_mail(name, email, subject, message):
    email_message = f"Subject: {subject}\n\nName: {name}\nEmail: {email}\nMessage: {message}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(email, OWN_EMAIL, email_message)


if __name__ == "__main__":
    app.run(debug=False)
