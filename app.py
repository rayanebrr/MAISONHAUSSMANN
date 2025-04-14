from flask import Flask, request, redirect, render_template, flash
from email.message import EmailMessage
import smtplib

app = Flask(__name__, static_folder='assets')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/projets")
def projet():
    return render_template("projet.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/a-propos")
def a_propos():
    return render_template("a_propos.html")

@app.route('/contact', methods=["POST"])
def mailDevis():
    email = request.form.get("email")
    phone = request.form.get("phone")
    description = request.form.get("textarea")
    
    full_message = f"{description}\n\nEmail: {email}\nTéléphone: {phone}"

    msg = EmailMessage()
    msg.set_content(full_message)
    msg["Subject"] = "Demande de devis"
    msg["From"] = "demandedevis.maisonhaussmann@gmail.com"
    msg["To"] = "contact@maisonhaussmann.fr"

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login("demandedevis.maisonhaussmann@gmail.com", "qgfwpleeotukozcz")
    s.send_message(msg)
    s.quit()

    return redirect("/?success=1")

if __name__ == '__main__':
    app.run(debug=True)
