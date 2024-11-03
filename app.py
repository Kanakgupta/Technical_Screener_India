from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Define your valid CSV categories and patterns
CSV_FILES = [
    'NIFTY-500_TOP_STOCKS', 'NIFTY-COMMODITIES', 'NIFTY-CONSUMPTION',
    'NIFTY-DIGITAL', 'NIFTY-DIVIDEND-OPPORTUNITIES', 'NIFTY-INFRASTRUCTURE',
    'NIFTY-MANUFACTURING', 'NIFTY-MICROCAP-250', 'NIFTY-MIDSMALLCAP',
    'NIFTY-OIL-GAS', 'NIFTY-TATA-GROUP'
]

PATTERNS = [
    'rounding_bottom', 'head_and_shoulders', 'multiple_top_bottom',
    'bullish_engulfing', 'bearish_engulfing', 'morning_star',
    'evening_star', 'rising_wedge', 'falling_wedge', 'inverted_head_and_shoulders'
]

@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML form from a template

@app.route('/process', methods=['POST'])
def process():
    category = request.form['category']
    patterns = request.form.getlist('patterns')

    # Debugging output
    print(f"Category: {category}, Patterns: {patterns}")

    if not patterns:
        return "No patterns selected.", 400

    if category not in CSV_FILES or not any(pattern in PATTERNS for pattern in patterns):
        return "Invalid category or patterns selected.", 400

    # Simulating processing results
    results = {pattern: f"Results for {pattern} in {category}" for pattern in patterns}

    return render_template('results.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)