from flask import Flask, request, render_template_string
import xml.etree.ElementTree as ET

app = Flask(__name__)

FAKE_FLAG = "FLAG{Not_The_Real_Flag}"
REAL_FLAG = "FLAG{XML_Is_Always_There_But_Hidden}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        xml_data = request.form.get("xml")

        try:
            # Parse the XML data (vulnerable parser)
            root = ET.fromstring(xml_data)
            user_name = root.find("name").text
            user_age = root.find("age").text

            if root.find("admin_secret") is not None and root.find("admin_secret").text == "flag":
                message = f"Congratulations! Here is your real flag: {REAL_FLAG}"
            elif user_name.lower() == "admin":
                message = f"Congratulations! Here is your flag: {FAKE_FLAG}"  # Display decoy flag            
            else:
                message = f"Hello, {user_name}! You are {user_age} years old."
        except Exception as e:
            message = f"Error parsing XML: {str(e)}"

        return render_template_string(f"""
            <div class="container">
                <div class="card">
                    <h2>{message}</h2>
                    <a href='/' class="back-btn">Go Back</a>
                </div>
            </div>
            <style>
                body {{
                    background: linear-gradient(135deg, #20232a, #282c34);
                    color: #f1f1f1;
                    font-family: 'Press Start 2P', sans-serif;
                    text-align: center;
                    padding: 20px;
                }}
                .container {{
                    display: flex;
                    height: 100vh;
                    justify-content: center;
                    align-items: center;
                }}
                .card {{
                    background: rgba(0, 0, 0, 0.8);
                    padding: 30px;
                    border-radius: 10px;
                    border: 2px solid #00ffcc;
                    box-shadow: 0 0 10px #00ffcc;
                }}
                h2 {{
                    color: #00ffcc;
                    margin-bottom: 20px;
                }}
                .back-btn {{
                    padding: 10px 20px;
                    text-decoration: none;
                    color: #282c34;
                    background-color: #00ffcc;
                    border-radius: 5px;
                    font-size: 16px;
                    font-weight: bold;
                    box-shadow: 0 0 10px #00ffcc;
                    border: 2px solid #00ffcc;
                    transition: all 0.3s ease-in-out;
                }}
                .back-btn:hover {{
                    background-color: #282c34;
                    color: #00ffcc;
                }}
            </style>
        """)

    return """
        <div class="container">
            <div class="form-card">
                <h1>Welcome to the XML Challenge!</h1>
                <p>Enter your XML data to see how the server processes it. Hint: Admins have a special flag!</p>
                <form method="POST">
                    <label for="xml">Enter your favorite color:</label><br><br>
                    <textarea name="xml" rows="10" cols="50" placeholder="Enter something fun here!"></textarea><br><br>
                    <button type="submit" class="submit-btn">Submit Data</button>
                </form>
            </div>
        </div>

        <style>
            @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

            body {
                background: radial-gradient(circle, #1f1f1f, #111);
                color: #fff;
                font-family: 'Press Start 2P', sans-serif;
                text-align: center;
            }

            .container {
                display: flex;
                height: 100vh;
                justify-content: center;
                align-items: center;
            }

            .form-card {
                background: rgba(0, 0, 0, 0.8);
                padding: 30px;
                border-radius: 10px;
                border: 2px solid #ff007f;
                box-shadow: 0 0 10px #ff007f;
            }

            h1 {
                font-size: 24px;
                color: #ff007f;
            }

            p {
                font-size: 14px;
                margin-bottom: 20px;
            }

            textarea {
                background-color: #1e1e1e;
                color: #fff;
                border: 2px solid #ff007f;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Press Start 2P', sans-serif;
                width: 100%;
            }

            .submit-btn {
                padding: 10px 20px;
                text-decoration: none;
                color: #1e1e1e;
                background-color: #ff007f;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
                box-shadow: 0 0 10px #ff007f;
                border: 2px solid #ff007f;
                transition: all 0.3s ease-in-out;
            }

            .submit-btn:hover {
                background-color: #1e1e1e;
                color: #ff007f;
            }
        </style>
    """
if __name__ == "__main__":
    app.run(debug=True)
