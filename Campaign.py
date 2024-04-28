import requests
import json
import random
import Recommend

def greedy_pset() -> list:
    return [{'contestId': 996, 'index': 'A', 'name': 'Hit the Lottery', 'type': 'PROGRAMMING', 'points': 500.0, 'rating': 800, 'tags': ['dp', 'greedy'], 'url': 'https://codeforces.com/problemset/problem/996/A'},
            {'contestId': 230, 'index': 'A', 'name': 'Dragons', 'type': 'PROGRAMMING', 'points': 500.0, 'rating': 1000, 'tags': ['greedy', 'sortings'], 'url': 'https://codeforces.com/problemset/problem/230/A'},
            {'contestId': 489, 'index': 'B', 'name': 'BerSU Ball', 'type': 'PROGRAMMING', 'points': 1000.0, 'rating': 1200, 'tags': ['dfs and similar', 'dp', 'graph matchings', 'greedy', 'sortings', 'two pointers'], 'url': 'https://codeforces.com/problemset/problem/489/B'},
            {'contestId': 762, 'index': 'B', 'name': 'USB vs. PS/2', 'type': 'PROGRAMMING', 'rating': 1400, 'tags': ['greedy', 'implementation', 'sortings', 'two pointers'], 'url': 'https://codeforces.com/problemset/problem/762/B'},
            {'contestId': 479, 'index': 'C', 'name': 'Exams', 'type': 'PROGRAMMING', 'points': 1500.0, 'rating': 1400, 'tags': ['greedy', 'sortings'], 'url': 'https://codeforces.com/problemset/problem/479/C'},
            {'contestId': 1158, 'index': 'A', 'name': 'The Party and Sweets', 'type': 'PROGRAMMING', 'points': 500.0, 'rating': 1500, 'tags': ['binary search', 'constructive algorithms', 'greedy', 'implementation', 'math', 'sortings', 'two pointers'], 'url': 'https://codeforces.com/problemset/problem/1158/A'},
            {'contestId': 321, 'index': 'B', 'name': 'Ciel and Duel', 'type': 'PROGRAMMING', 'points': 1000.0, 'rating': 1900, 'tags': ['dp', 'flows', 'greedy'], 'url': 'https://codeforces.com/problemset/problem/321/B'}]