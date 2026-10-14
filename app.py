import pickle
import numpy as np
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Load the trained GaussianNB model using your exact filename
MODEL_FILENAME = 'naivebyes.pkl'
with open(MODEL_FILENAME, 'rb') as f:
    model = pickle.load(f)

# Embedded HTML & CSS Template
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee Prediction Portal</title>
    <style>
        :root {
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-color: #1e293b;
            --border-color: #cbd5e1;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
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
            padding: 30px 40px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            width: 100%;
            max-width: 500px;
        }
        h2 {
            margin-top: 0;
            text-align: center;
            color: var(--primary);
            font-size: 24px;
            margin-bottom: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 6px;
            font-weight: 600;
            font-size: 14px;
        }
        input, select {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            box-sizing: border-box;
            font-size: 14px;
            transition: border-color 0.2s;
            background-color: #fff;
        }
        input:focus, select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        }
        button {
            width: 100%;
            background-color: var(--primary);
            color: white;
            padding: 12px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 10px;
            transition: background-color 0.2s;
        }
        button:hover {
            background-color: var(--primary-hover);
        }
        .result-card {
            margin-top: 20px;
            padding: 15px;
            background-color: #e0e7ff;
            border-left: 5px solid var(--primary);
            border-radius: 4px;
            text-align: center;
            font-weight: bold;
            font-size: 16px;
            color: #312e81;
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
            
            <button type="submit">Predict</button>
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
