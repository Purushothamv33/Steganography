from flask import Flask, render_template_string, request, send_file
from stegano import lsb
import os
from datetime import datetime

app = Flask(__name__)

# Folder to store temporary images
OUTPUT_FOLDER = "output_images"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Base image (must be PNG)
BASE_IMAGE_PATH = "C:\\Users\\DELL\\OneDrive\\Desktop\\stegono_app\\static\\ATS.jpg"


# HTML Template
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Steganography Image Download</title>
</head>
<body>
    <h2>Download Image with Hidden Keyword</h2>
    <form method="POST">
        <label>Enter your User ID or Name:</label>
        <input type="text" name="user_id" required>
        <button type="submit">Download Image</button>
    </form>
    {% if image_path %}
        <p>✅ Image generated with your hidden ID!</p>
        <a href="{{ url_for('download_image', filename=image_filename) }}">Click here to download</a>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    image_path = None
    image_filename = None

    if request.method == 'POST':
        user_id = request.form['user_id']
        hidden_message = f"downloaded_by_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Create output image with hidden message
        output_filename = f"{user_id}_hidden.png"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        secret_img = lsb.hide(BASE_IMAGE_PATH, hidden_message)
        secret_img.save(output_path)

        image_path = output_path
        image_filename = output_filename

    return render_template_string(HTML, image_path=image_path, image_filename=image_filename)

@app.route('/download/<filename>')
def download_image(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
