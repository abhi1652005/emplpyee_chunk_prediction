import pickle
import numpy as np
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Load the trained GaussianNB model using your exact filename
MODEL_FILENAME = 'naivebyes.pkl'
with open(MODEL_FILENAME, 'rb') as f:
    model = pickle.load(f)

# Embedded HTML & CSS Template with New Colors and Animations
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee Prediction Portal</title>
    <style>
        :root {
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --accent: #14b8a6;
            --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --card-bg: rgba(255, 255, 255, 0.95);
            --text-color: #1e293b;
            --border-color: #cbd5e1;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes pulseResult {
            0% { transform: scale(0.98); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--bg-gradient);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .container {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            padding: 35px 40px;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            width: 100%;
            max-width: 500px;
            animation: fadeIn 0.8s ease-out forwards;
        }

        h2 {
            margin-top: 0;
            text-align: center;
            color: var(--primary);
            font-size: 26px;
            margin-bottom: 25px;
            letter-spacing: -0.5px;
        }

        .form-group {
            margin-bottom: 16px;
        }

        label {
            display: block;
            margin-bottom: 6px;
            font-weight: 600;
            font-size: 13px;
            color: #475569;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        input, select {
            width: 100%;
            padding: 11px 14px;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            box-sizing: border-box;
            font-size: 14px;
            transition: all 0.3s ease;
            background-color: #ffffff;
        }

        input:focus, select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15);
            transform: translateY(-1px);
        }

        button {
            width: 100%;
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
            color: white;
            padding: 13px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 15px;
            transition: opacity 0.3s ease, transform 0.2s ease;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }

        button:hover {
            opacity: 0.95;
            transform: translateY(-2px);
        }

        button:active {
            transform: translateY(0);
        }

        .result-card {
            margin-top: 25px;
            padding: 16px;
            background: linear-gradient(135deg, #e0f2fe 0%, #e0e7ff 100%);
            border-left: 6px solid var(--primary);
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
            font-size: 16px;
            color: #1e1b4b;
            animation: pulseResult 0.5s ease-out;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Employee Analysis Portal</h2>
        <form method="POST">
            <div class="form-group">
                <label for="Education">Education Level:</label>
                <select id="Education" name="Education" required>
                    <option value="0">Bachelors</option>
                    <option value="1">Masters</option>
                    <option value="2">PHD</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="JoiningYear">Joining Year:</label>
                <input type="number" id="JoiningYear" name="JoiningYear" required placeholder="e.g., 2018" min="2012" max="2026">
            </div>
            
            <div class="form-group">
                <label for="City">City:</label>
                <select id="City" name="City" required>
                    <option value="0">Bangalore</option>
                    <option value="1">New Delhi</option>
                    <option value="2">Pune</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="PaymentTier">Payment Tier:</label>
                <select id="PaymentTier" name="PaymentTier" required>
                    <option value="1">Tier 1 (Highest)</option>
                    <option value="2">Tier 2</option>
                    <option value="3">Tier 3 (Lowest)</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="Age">Age:</label>
                <input type="number" id="Age" name="Age" required placeholder="e.g., 28" min="18" max="65">
            </div>
            
            <div class="form-group">
                <label for="Gender">Gender:</label>
                <select id="Gender" name="Gender" required>
                    <option value="0">Male</option>
                    <option value="1">Female</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="EverBenched">Ever Benched:</label>
                <select id="EverBenched" name="EverBenched" required>
                    <option value="0">No</option>
                    <option value="1">Yes</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="ExperienceInCurrentDomain">Experience In Current Domain (Years):</label>
                <input type="number" id="ExperienceInCurrentDomain" name="ExperienceInCurrentDomain" required placeholder="e.g., 3" min="0" max="20">
            </div>
            
            <button type="submit">Predict Risk</button>
        </form>

        {% if prediction_text is not none %}
        <div class="result-card">
            Prediction Result: {{ prediction_text }}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction_text = None
    if request.method == 'POST':
        try:
            # Extract features in the exact training order expected by naivebyes.pkl[cite: 1]
            features = [
                float(request.form['Education']),
                float(request.form['JoiningYear']),
                float(request.form['City']),
                float(request.form['PaymentTier']),
                float(request.form['Age']),
                float(request.form['Gender']),
                float(request.form['EverBenched']),
                float(request.form['ExperienceInCurrentDomain'])
            ]
            
            prediction = int(model.predict([features])[0])
            
            # Map numerical output to user-friendly readable descriptions
            if prediction == 1:
                prediction_text = "Likely to Leave (Churn Risk)"
            else:
                prediction_text = "Likely to Stay"
                
        except Exception as e:
            prediction_text = f"Error in processing input: {str(e)}"
            
    return render_template_string(HTML_PAGE, prediction_text=prediction_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
