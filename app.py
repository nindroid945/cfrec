from Recommend import smart_recommend, pub_recommend
from flask import Flask, request, jsonify, render_template
import propelauth_flask as propel
import time
app = Flask(__name__)
auth = propel.init_auth("https://69808087.propelauthtest.com", "b7574e339d28d2e617e203f9e417bdbdc8209fea143b558154dc505f40410fc38248e7de23eb0ca7e5bd337365eacba6")

@app.route("/")
def home():
	return render_template("homepage.html")

# def recommend(rating: int, tags: set, num: int):
@app.route("/api/recommend")
def recommend():
	print(request.headers)
	rating = request.headers['rating']
	tags = request.headers['tags']
	num = request.headers['num']

	response = jsonify(pub_recommend(rating, tags, num))
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

# def smart_recommend(handle: str) -> list:
@app.route("/api/smartrecommend/<handle>")
@auth.require_user
def smartrecommend(handle):
	# print(handle)
	response = jsonify(smart_recommend(handle))
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response