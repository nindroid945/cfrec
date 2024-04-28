from Recommend import smart_recommend, pub_recommend
import Search
import Random
from flask import Flask, request, jsonify, render_template
import propelauth_flask as propel
import sqlite3
import requests


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
	# handle = "jasonfeng365"
	handle = apigetlinkedaccount()
	print(handle)

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
	handle = request.headers['CFUsername']
	user_id = propel.current_user.user_id

	response = requests.get(f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=1")

	if not response.ok:
		return f"Unable to link: Response errored, Code {response.status_code}"
	
	rdict = response.json()['result']
	if len(rdict) != 1 or 'verdict' not in rdict[0]:
		return "Unable to link: It looks like you haven't solved any problems yet. Maybe Codeforces is still processing your submission?"
	
	if rdict[0]['problem']['contestId'] != 4 or rdict[0]['problem']['index'] != "A" or rdict[0]['verdict'] != "COMPILATION_ERROR":
		verdict = rdict[0].get('verdict')
	
		print(f"Verdict Error, {verdict = }")
		return "Unable to link: Please run `/link` again and ensure you submit a Compile Error to https://codeforces.com/problemset/problem/4/A and then click the checkmark."

	con = sqlite3.connect("users.db")
	cursor = con.cursor()
	cursor.row_factory = sqlite3.Row

	c = f"""
SELECT * FROM cf_users
WHERE handle='{handle}'
"""
	cursor.execute(c)
	if cursor.fetchone() != None:
		# user with Handle exists, just update discord_id
		
		update = f"""
UPDATE cf_users
SET pauth_id='{user_id}'
WHERE handle='{handle}'
"""
		cursor.execute(update)
		con.commit()
	else:
		# handle not found, insert discord_id
		s = f"""
INSERT INTO cf_users (handle, pauth_id)
VALUES ('{handle}', '{user_id}')
"""
		cursor.execute(s)
		con.commit()
	return "Successfully linked!"

@app.route("/api/getlinkedaccount/")
@auth.require_user
def apigetlinkedaccount():
	con = sqlite3.connect("users.db")
	cursor = con.cursor()
	cursor.row_factory = sqlite3.Row


	user_id = propel.current_user.user_id
	check_exists = f"""
SELECT * FROM cf_users
WHERE pauth_id='{user_id}'
"""
	cursor.execute(check_exists)
	user_before_update = cursor.fetchone()
	con.commit()

	if user_before_update == None: return "null"
	else: return user_before_update["handle"]

@app.route("/api/search/")
def apisearch():
	name = request.headers['ProblemName']
	if not name: return "null"

	response = jsonify(Search.search(name))
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response