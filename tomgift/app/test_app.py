from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    print("[DEBUG] Current working directory:", os.getcwd())
    template_path = os.path.join(app.template_folder or 'templates', 'dashboard.html')
    print("[DEBUG] Looking for template at:", template_path)
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
