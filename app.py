from Recommend import smart_recommend, pub_recommend
import Search
import Random
from flask import Flask, request, jsonify, render_template
import propelauth_flask as propel

app = Flask(__name__)
auth = propel.init_auth("https://69808087.propelauthtest.com", "b7574e339d28d2e617e203f9e417bdbdc8209fea143b558154dc505f40410fc38248e7de23eb0ca7e5bd337365eacba6")

@app.route("/")
def home():
	return render_template("homepage.html")

@app.route("/account/")
def account():
	return render_template("account.html")

@app.route("/search/")
def search():
	return render_template("search.html")

# def recommend(rating: int, tags: set, num: int):
@app.route("/api/recommend/")
def apirecommend():
	print(request.headers)
	rating = int(request.headers['Rating'])
	tags = set(request.headers['Tags'].lower().split(";")) - set([''])
	num = 5
	# print("Tags", tags)

	response = jsonify(pub_recommend(rating, tags, num))
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

# def smart_recommend(handle: str) -> list:
@app.route("/api/smartrecommend/")
@auth.require_user
def apismartrecommend():
	# handle = database.getHandleFromPropelID(propel.current_user.user_id)
	# if handle==None: return None
	handle = "jasonfeng365"
	# print(handle)

	response = jsonify(smart_recommend(handle))
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

@app.route("/api/daily/")
def daily():
	response = jsonify(Random.daily())
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

@app.route("/api/linkaccount/", methods=['POST'])
@auth.require_user
def apilinkaccount():
	username = request.headers['CFUsername']
	# handle = database.setHandleFromPropelID(propel.current_user.user_id, username)
	# if handle==None: return "null"
	# print(handle)
	return "Success"

@app.route("/api/getlinkedaccount/")
@auth.require_user
def apigetlinkedaccount():
	# handle = database.getHandleFromPropelID(propel.current_user.user_id)
	# if handle: return handle
	return "null"

@app.route("/api/search/")
def apisearch():
	name = request.headers['ProblemName']
	if not name: return "null"

	response = jsonify(Search.search(name))
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response