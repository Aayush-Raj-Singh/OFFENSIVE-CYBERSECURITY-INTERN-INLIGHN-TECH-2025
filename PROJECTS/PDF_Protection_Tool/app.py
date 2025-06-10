from flask import Flask, render_template, request, send_file, redirect, flash
import PyPDF2
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from io import BytesIO

# OPTIONAL: Google Drive integration
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'
LOG_FILE = 'log.csv'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def upload_to_drive(file_path):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    file = drive.CreateFile({'title': os.path.basename(file_path)})
    file.SetContentFile(file_path)
    file.Upload()
    return file['alternateLink']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf_file = request.files.get('pdf_file')
        password = request.form.get('password')

        if not pdf_file or not password:
            flash("PDF file and password are required.")
            return redirect('/')

        filename = secure_filename(pdf_file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        output_path = os.path.join(UPLOAD_FOLDER, f"protected_{filename}")
        pdf_file.save(input_path)

        try:
            with open(input_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                writer = PyPDF2.PdfWriter()

                for page in reader.pages:
                    writer.add_page(page)

                writer.encrypt(password)

                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)

            # Logging
            with open(LOG_FILE, 'a') as log:
                log.write(f"{filename},{datetime.now().isoformat()},{request.remote_addr}\n")

            # OPTIONAL: Upload to Google Drive
            drive_link = upload_to_drive(output_path)
            flash(f"✅ PDF uploaded to Google Drive: <a href='{drive_link}' target='_blank'>{drive_link}</a>")

            return send_file(
                output_path,
                as_attachment=True,
                download_name=f"protected_{filename}",
                mimetype='application/pdf'
            )

        except Exception as e:
            flash(f"Error: {str(e)}")
            return redirect('/')

    return render_template('index.html')

@app.route('/logs')
def view_logs():
    if not os.path.exists(LOG_FILE):
        return "<p>No logs available.</p>"

    with open(LOG_FILE, 'r') as f:
        lines = f.readlines()

    return render_template('logs.html', logs=lines)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Here you would save user data to DB or file
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        flash(f"Account created for {name} ({email})! ✅")
        return redirect('/')
    return render_template('signup.html')
