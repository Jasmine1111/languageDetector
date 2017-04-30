from flask import Flask, render_template, request, jsonify, make_response
from languageDetector import getTextLanguage 
from math import e
from config import HOST
from cors import crossdomain
from datetime import datetime
import json

app = Flask(__name__)
app.debug = False
app.config['MAX_CONTENT_LENGTH'] = (1 << 20) # 1 MB max request size

def get_language_info(text):
    language = getTextLanguage(text)
    return language

@app.route('/')
def home():
	return render_template("index.html")

@app.route('/api/text/', methods=["POST"])
@crossdomain(origin='*')
def read_api():
	text = request.form.get("txt")
	language = get_language_info(text)
	result = {"language": language}
	return jsonify(result=result)

@app.route('/web/text/', methods=["POST"])
@crossdomain(origin='*')
def evaldata():
	text = request.form.get("txt")
	result = get_language_info(text)
	return jsonify(result=result, sentence=text)

@app.route('/api/batch/', methods=["POST"])
@crossdomain(origin='*')
def batch_handler():
	json_data = request.get_json(force=True, silent=True)
	if not json_data:
		return jsonify(error="Bad JSON request")
	result = []
	for req in json_data:
		language = get_language_info(req)
		result.append({"result": language})

	resp = make_response(json.dumps(result))
	resp.mimetype = 'application/json'

	return resp

@app.route('/docs/api/')
def api():
	return render_template('api.html', host=HOST)

@app.route('/about/')
def about():
	return render_template('about.html')

