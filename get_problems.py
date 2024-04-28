import requests
import json





def filter_problems(startRange: int, endRange: int, tags: list[str]):
	tags_param = ';'.join(tags)
	url = f"https://codeforces.com/api/problemset.problems?tags={tags_param}"
	print(url)
	response = requests.get(url=url)
	
	if not response.ok:
		return
	
	rdict = response.json()
	print(rdict.keys())
	problems = rdict['result']['problems']

	filtered = [i for i in problems if 'rating' in i.keys() and startRange <= i['rating'] <= endRange]
	print(len(filtered))

def main():
	filter_problems(800, 1000, ["greedy", "dp"])



if __name__ == '__main__':
	main()