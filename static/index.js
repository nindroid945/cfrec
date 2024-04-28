const authClient = PropelAuth.createClient({
	authUrl: "https://69808087.propelauthtest.com",
	enableBackgroundTokenRefresh: true,
});

const homepage = new Vue({
	el: '#index',
	data: {
		tags:['2-sat', 'Binary search', 'Bitmasks', 'Brute force', 'Chinese remainder theorem', 'Combinatorics', 'Constructive algorithms', 'Data structures', 'DFS and similar', 'Divide and conquer', 'DP', 'DSU', 'Expression parsing', 'FFT', 'Flows', 'Games', 'Geometry', 'Graph matchings', 'Graphs', 'Greedy', 'Hashing', 'Implementation', 'Interactive', 'Math', 'Matrices', 'Meet-in-the-middle', 'Number theory', 'Probabilities', 'Schedules', 'Shortest paths', 'Sortings', 'String suffix structures', 'Strings', 'Ternary search', 'Trees', 'Two pointers'],
		tagsHTML:"",
		low:"",
		high:"",
		recommendResponse:"",
		recommendedProblemLink:"",
		opponent:"",
		loginButtonText:"Login/Signup",
		loggedIn:false,
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
			let res = '<br>'
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
		getQueryTags() {
			let tags = []

			for (let i=0; i<36; i++)
				if (document.getElementById(this.toTagFormat(this.tags[i])).checked)
					tags.push(this.tags[i].toLowerCase())
			return tags
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
		getSmartRecommendation(username) {
			let text = ""
			text += "Recommended problems: "
			let url = "http://localhost:5000/api/smartrecommend/"+username

			let vue = this

			authClient.getAuthenticationInfoOrNull().then((authInfo)=>{
				if (!authInfo) return
				fetch(url, {
					headers: {
						"Content-Type": "application/json",
						"Authorization": `Bearer ${authInfo.accessToken}`
					}
				}).then(function(res) {
					res.json().then(res=>{
						console.log(res)
						for (let i=0; i<res.length; i++) {
							text += '<a href="'+res[i].url+'">'+res[i].name+" ("+res[i].rating+')</a> '
							// console.log(res[i].url)
						}
	
						vue.recommendedProblemLink = text
						console.log(text)
						return text
					})
				})
			})


			
		},
		autoRecommend() {
			// let problemLink = ""
			// let rec = this.getSmartRecommendation("jasonfeng365")
			// console.log(rec)
			// this.recommendedProblemLink = rec
			// this.$forceUpdate()
			// this.recommendedProblemLink = "69420"
			this.getSmartRecommendation("jasonfeng365")
		},
		manualRecommend() {
			// console.log("Manual rec")
			if (!this.validateQuery()) return;

			// this.recommendedProblemLink = "69420"
			
		},
	},
	mounted: function() {
		// console.log(window.location.href.split("?"))
		this.tagsHTML = this.generateTags()

		authClient.getAuthenticationInfoOrNull().then((authInfo)=>{
			if (!authInfo) return
			this.loggedIn = true
			this.loginButtonText = "Welcome!"
		})
	}
});
 