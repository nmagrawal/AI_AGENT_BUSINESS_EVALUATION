from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from startup import run_analysis  # We'll create this function

app = Flask(__name__)
CORS(app)

@app.route('/api/analyze', methods=['POST'])
def analyze_business():
    data = request.json
    business_idea = data.get('business_idea')
    if not business_idea:
        return jsonify({'error': 'No business idea provided'}), 400
    
    try:
        result = run_analysis(business_idea)
        # Convert CrewAI output to string
        result_str = str(result)
        return jsonify({'result': result_str})
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error details: {error_details}")
        return jsonify({'error': str(e), 'details': error_details}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)
