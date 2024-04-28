// const authClient = PropelAuth.createClient({
// 	authUrl: "https://69808087.propelauthtest.com",
// 	enableBackgroundTokenRefresh: true,
// });

const account = new Vue({
	el: '#index',
	data: {
		campaigns:"",
	},
	computed: {
		
	},
	methods: {
		parseSearchResults(res) {
			let text = ""
			for (let i=0; i<res.length; i++)
				text += '<a href="'+res[i].url+'">'+res[i].name+" ("+res[i].rating+')</a><br>'
			return text
		},
		search() {
			let vue = this
			fetch("http://localhost:5000/api/search/").then(function(res) {
				res.json().then(res=>{
					console.log(res)
					let finalText = ""
					for (let i=0; i<res.length; i++) {
						let cur = ""
						for (let i=0; i<res.length; i++) {
							text += '<a href="'+res[i].url+'">'+res[i].name+" ("+res[i].rating+')</a> '
							// console.log(res[i].url)
						}
					}
					console.log(res)
					if (res != "null") vue.searchResults = vue.parseSearchResults(res)
				})
			})
		},
	},
	mounted: function() {
		this.search()
	}
});
 