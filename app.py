from Recommend import smart_recommend, pub_recommend

from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

@app.route("/")
def home():
	return render_template('index.html')

# def recommend(rating: int, tags: set, num: int):
@app.route("/api/recommend")
def recommend():
	print(request.headers)
	rating = request.headers['rating']
	tags = request.headers['tags']
	num = request.headers['num']
	return pub_recommend(rating, tags, num)

# def smart_recommend(handle: str) -> list:
@app.route("/api/smartrecommend/<handle>")
def smartrecommend(handle):
	# print(handle)
	response = jsonify(smart_recommend(handle))
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response