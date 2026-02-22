from flask import Flask, request, redirect, render_template, flash
from email.message import EmailMessage
import smtplib
import os
from pathlib import Path

app = Flask(__name__, static_folder='assets')

GALLERY_CATEGORIES = [
    ('salle-de-bain',         'Salle de bain'),
    ('menuiserie-exterieure', 'Menuiserie extérieure'),
    ('cuisines',              'Cuisines'),
    ('sols',                  'Sols'),
    ('remise-en-etat',        'Remise en état'),
]

VALID_EXTENSIONS = {'.JPG', '.JPEG', '.PNG', '.GIF', '.WEBP', '.MP4', '.WEBM'}

def _file_entry(file, url, category):
    ext = file.suffix.upper()
    return {
        'name': file.name,
        'url':  url,
        'type': 'video' if ext in {'.MP4', '.WEBM'} else 'image',
        'category': category,
    }

def get_gallery_data():
    """Retourne les fichiers de galerie organisés par catégorie."""
    gallery_path = Path(__file__).parent / 'assets' / 'images' / 'gallery'

    if not gallery_path.exists():
        return {'categories': [], 'all_files': [], 'has_categories': False}

    all_files = []
    categories_data = []

    # Fichiers dans les sous-dossiers de catégorie
    for slug, label in GALLERY_CATEGORIES:
        cat_path = gallery_path / slug
        if not cat_path.exists():
            continue
        files = []
        for f in sorted(cat_path.iterdir()):
            if f.is_file() and f.suffix.upper() in VALID_EXTENSIONS:
                entry = _file_entry(f, f'assets/images/gallery/{slug}/{f.name}', slug)
                files.append(entry)
                all_files.append(entry)
        # Toujours inclure la catégorie (même vide) pour l'affichage
        categories_data.append({'slug': slug, 'label': label, 'count': len(files), 'files': files})

    # Fichiers dans le dossier racine (non catégorisés)
    root_files = []
    for f in sorted(gallery_path.iterdir()):
        if f.is_file() and f.suffix.upper() in VALID_EXTENSIONS:
            entry = _file_entry(f, f'assets/images/gallery/{f.name}', 'tous')
            root_files.append(entry)
            all_files.append(entry)

    return {
        'categories':     categories_data,
        'root_files':     root_files,
        'all_files':      all_files,
        'has_categories': len(categories_data) > 0,
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/projets")
def projet():
    gallery_data = get_gallery_data()
    return render_template("projet.html", gallery_data=gallery_data)

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
    
    full_message = f"{description}\n\nEmail: {email}\n\nTéléphone: {phone}"

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

    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
