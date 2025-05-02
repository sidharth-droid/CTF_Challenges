from flask import Flask, request, render_template_string
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GREETING_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Template Tinkerer</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; padding: 20px; }
        .form-container { max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }
        .greeting { margin-top: 20px; text-align: center; color: #343a40; }
    </style>
</head>
<body>
    <div class="form-container">
        <h2 class="text-center mb-4">Admin Greeting Customizer</h2>
        <form method="POST">
            <div class="mb-3">
                <label for="greeting" class="form-label">Enter your greeting:</label>
                <input type="text" class="form-control" id="greeting" name="greeting" placeholder="Hello, {{ name }}!" value="Hello, {{ name }}!">
            </div>
            <button type="submit" class="btn btn-primary w-100">Apply Greeting</button>
        </form>
        <div class="greeting">
            {% if greeting %}
                {{ greeting_output | safe }}
            {% endif %}
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def greeting():
    """Handle greeting customization with SSTI vulnerability."""
    greeting_output = ""
    if request.method == 'POST':
        greeting = request.form.get('greeting', 'Hello, {{ name }}!')
        try:
            greeting_output = render_template_string(greeting, name="User")
        except Exception as e:
            logger.error(f"Rendering error: {e}")
            greeting_output = "Error rendering greeting!"
    return render_template_string(GREETING_PAGE, greeting=True, greeting_output=greeting_output)

