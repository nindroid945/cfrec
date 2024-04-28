const authClient = PropelAuth.createClient({
	authUrl: "https://69808087.propelauthtest.com",
	enableBackgroundTokenRefresh: true,
});

const account = new Vue({
	el: '#index',
	data: {
		loginButtonText:"Login/Signup",
		cfusername:"",
	},
	computed: {
		
	},
	methods: {
		linkaccount() {
			
		},
	},
	mounted: function() {
		let vue = this
		authClient.getAuthenticationInfoOrNull().then((authInfo)=>{
			if (!authInfo) return

			this.loggedIn = true
			this.loginButtonText = authInfo.user.email
			console.log(authInfo)

			fetch("http://localhost:5000/api/getlinkedaccount/", {
				headers: {
					"Content-Type": "application/json",
					"Authorization": `Bearer ${authInfo.accessToken}`
				}
			}).then(function(res) {
				res.text().then(res=>{
					console.log(res)
					if (res != "null") vue.cfusername = res
				})
			})
		})
	}
});
 