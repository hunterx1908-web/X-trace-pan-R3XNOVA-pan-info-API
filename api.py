import os
import requests
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# 🔑 Teri API Key
VALID_KEY = "@R3XNOVA"

# Original API details
ORIGINAL_API_URL = "https://rohit-apis-nine.vercel.app/api/pan-info"
ORIGINAL_KEY = "Bhai"

# 🔥 API Expiry Date (4 din — aaj included)
API_EXPIRY = "2026-11-01"

def is_expired():
    try:
        expiry = datetime.strptime(API_EXPIRY, "%Y-%m-%d")
        return datetime.utcnow() > expiry
    except:
        return False

@app.route('/')
def home():
    return jsonify({
        "status": True,
        "message": "PAN Info API is working! (X-TRACE Edition)",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER",
        "expires_on": API_EXPIRY,
        "status": "Active" if not is_expired() else "Expired",
        "endpoints": {
            "info": "/api/pan-info?key=YOUR_KEY&pan=PAN_NUMBER"
        },
        "example": "/api/pan-info?key=@R3XNOVA&pan=BOKPS7056D"
    })

@app.route('/api/pan-info')
def pan_info():
    # 🔥 Check if API is expired
    if is_expired():
        return jsonify({
            "status": False,
            "error": f"API expired on {API_EXPIRY}! Please contact support.",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER",
            "expires_on": API_EXPIRY
        }), 401
    
    # Get parameters
    key = request.args.get('key')
    pan = request.args.get('pan')
    
    # 🔐 Key verify
    if not key:
        return jsonify({
            "status": False,
            "error": "Missing API Key!",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 400
        
    if key != VALID_KEY:
        return jsonify({
            "status": False,
            "error": "Invalid API Key!",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 401
    
    if not pan:
        return jsonify({
            "status": False,
            "error": "Missing 'pan' parameter!",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 400
    
    # Clean PAN (uppercase, remove spaces)
    pan = pan.strip().upper()
    
    # Basic PAN validation (10 characters)
    if len(pan) != 10:
        return jsonify({
            "status": False,
            "error": "Invalid PAN! Must be 10 characters.",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 400
    
    # Forward to original API
    params = {
        'key': ORIGINAL_KEY,
        'pan': pan
    }
    
    try:
        response = requests.get(ORIGINAL_API_URL, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        
        # 🔥 Clean response
        if isinstance(data, dict):
            # Remove original developer if exists
            data.pop('developer', None)
            data.pop('channel', None)
            data.pop('credits_remaining', None)
            
            # Check if data exists
            if not data.get('data') or data.get('data') == {}:
                return jsonify({
                    "status": False,
                    "message": "No data found",
                    "developer": "@x_TRACEOWNER",
                    "credit": "@x_TRACEOWNER"
                }), 404
            
            # Add our branding
            data['developer'] = '@x_TRACEOWNER'
            data['credit'] = '@x_TRACEOWNER'
            data['api_expires_on'] = API_EXPIRY
            
        return jsonify(data)
        
    except requests.exceptions.Timeout:
        return jsonify({
            "status": False,
            "message": "Request timeout. Please try again later.",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 504
        
    except requests.exceptions.ConnectionError:
        return jsonify({
            "status": False,
            "message": "No data found",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 404
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": False,
            "message": "No data found",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 404
        
    except Exception as e:
        return jsonify({
            "status": False,
            "message": "No data found",
            "developer": "@x_TRACEOWNER",
            "credit": "@x_TRACEOWNER"
        }), 404

@app.route('/api/pan-info/<path:path>')
def catch_all(path):
    return jsonify({
        "status": False,
        "message": "No data found",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER"
    }), 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": False,
        "message": "No data found",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status": False,
        "message": "No data found",
        "developer": "@x_TRACEOWNER",
        "credit": "@x_TRACEOWNER"
    }), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))