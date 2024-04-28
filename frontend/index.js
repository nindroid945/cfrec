const maze = new Vue({
	el: '#index',
	data: {
		tags:['2-sat', 'Binary search', 'Bitmasks', 'Brute force', 'Chinese remainder theorem', 'Combinatorics', 'Constructive algorithms', 'Data structures', 'DFS and similar', 'Divide and conquer', 'DP', 'DSU', 'Expression parsing', 'FFT', 'Flows', 'Games', 'Geometry', 'Graph matchings', 'Graphs', 'Greedy', 'Hashing', 'Implementation', 'Interactive', 'Math', 'Matrices', 'Meet-in-the-middle', 'Number theory', 'Probabilities', 'Schedules', 'Shortest paths', 'Sortings', 'String suffix structures', 'Strings', 'Ternary search', 'Trees', 'Two pointers'],
		tagsHTML:"",
		low:"",
		high:"",
		recommendResponse:"",
		recommendProblemLink:"",
	},
	computed: {
		lowest(){
			return this.index==0
		},
	},
	methods: {
		toTagFormat(string) {
			return string.toLowerCase().replace(" ", "-")
		},
		generateSingleTagRow(startIdx) {
			let res = ''
			res += '<div class="row"><div class="col"></div>'
			for (let i=startIdx; i<startIdx+6; i++)
				res += '<div class="col"><div class="form-check"><input class="form-check-input" type="checkbox" value="" id="'+this.toTagFormat(this.tags[i])+'"><label class="form-check-label" for="'+this.toTagFormat(this.tags[i])+'">'+this.tags[i]+'</label></div></div>'
			res += '<div class="col"></div></div>\n'
			return res
		},
		generateTags() {
			res = ""
			for (let i=0; i<36; i+=6) res += this.generateSingleTagRow(i)
			return res
		},
		getQuery() {
			for (let i=0; i<36; i++) {
				let checkedValue = document.getElementById(this.toTagFormat(this.tags[i])).checked;
				console.log(this.tags[i]+": "+checkedValue)
			}
		},
		validateQuery() {
			if (this.low == "" || this.high == "") {
				this.recommendResponse = "Enter a range of problem ratings"
				return false
			}
			this.low = Math.round(Number(this.low))
			this.high = Math.round(Number(this.high))

			if (this.low > this.high) this.recommendResponse = "Highest must be greater than lowest"
			else if (this.low < 800 || this.high > 3500) this.recommendResponse = "Ratings must be between 800 and 3500"
			else this.recommendResponse = ""

			return this.recommendResponse == ""
		},
		getLink() {
			return "69420"
		},
		autoRecommend() {
			let problemLink = ""
			this.recommendProblemLink = this.setRecommendedProblem(problemLink)
		},
		manualRecommend() {
			if (!this.validateQuery()) return;

			let problemLink = this.getQueryLink()
		},
	},
	mounted: function() {
		console.log(window.location.href.split("?"))
		this.tagsHTML = this.generateTags()
	}
});
 