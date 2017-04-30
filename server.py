import sys
sys.path.append("code")
from Sentiment_svm import svm_predict
from sentiment_lstm import classify2
from flask import Flask, render_template, request, jsonify, make_response
#from languageDetector import getTextLanguage,getSementLanguage 
from math import e
from config import HOST
from cors import crossdomain
from datetime import datetime
import json


app = Flask(__name__)
app.debug = False
app.config['MAX_CONTENT_LENGTH'] = (1 << 20) # 1 MB max request size

def percentage_confidence(conf):
	return 100.0 * e ** conf / (1 + e**conf)

def get_language_info(text):
    language = getTextLanguage(text)
    return language

def get_sement_language(text):
    language = getSementLanguage(text)
    return language

def get_sentiment_info(text):
	flag, confidence = classify2(text)
	if confidence > 0.5:
		sentiment = "Positive" if flag else "Negative"
	else:
		sentiment = "Neutral"
	conf = "%.4f" % percentage_confidence(confidence)
	return sentiment

@app.route('/')
def home():
	return render_template("index.html")

@app.route('/api/text/', methods=["POST"])
@crossdomain(origin='*')
def read_api():
        text = request.form.get("txt")
        language = get_sement_language(text)
        if language == "Chinese":
            result = svm_predict(text)
        else:
            result = get_sentiment_info(text)
        return jsonify(result=result)

@app.route('/web/text/', methods=["POST"])
@crossdomain(origin='*')
def evaldata():
        text = request.form.get("txt")
        language = get_sement_language(text)
        if language == "Chinese":
            result = svm_predict(text)
        else:
            result = get_sentiment_info(text)
        return jsonify(result=result, sentence=text)

@app.route('/sentiment/text/', methods=["POST"])
@crossdomain(origin='*')
def get_sentiment():
        text = request.form.get("txt")
        language = get_sement_language(text)
        if language == "Chinese":
            result = svm_predict(text)
        else:
            result = get_sentiment_info(text)
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

@app.route('/sentiment/')
def sentiment():
        return render_template('sentiment.html')

