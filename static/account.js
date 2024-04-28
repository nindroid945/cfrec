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
			authClient.getAuthenticationInfoOrNull().then((authInfo)=>{
				if (!authInfo) return
				let vue = this
				fetch("http://localhost:5000/api/linkaccount/", {
					method: "POST",
					headers: {
						"Content-type": "application/json; charset=UTF-8",
						"Authorization": `Bearer ${authInfo.accessToken}`,
						"CFUsername":vue.cfusername,
					}
				})
				.then((response) => response.text())
				.then((res) => console.log(res))
			})
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
 