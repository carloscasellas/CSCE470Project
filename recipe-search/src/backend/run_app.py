from flask import Flask, request, jsonify
from flask_cors import CORS
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
