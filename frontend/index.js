const maze = new Vue({
	el: '#puzzle',
	data: {
		mazes:[],
		explanations:[],
		index:0,
		secondArray:[0,1,2,3,4,9,12,14],

		currentMaze:"",
		currentExplanation:"",
		
		input:"",
		response:"Enter your answer above.",
	},
	computed: {
		lowest(){
			return this.index==0
		},
		highest(){
			return this.index==this.mazes.length-1
		},
	},
	methods: {
		setOutputs(){
			this.currentMaze = this.mazes[this.index];
			this.currentExplanation = this.explanations[this.index];
		},
		submit(){
			this.response = (hashCode(this.input.trim())==mazeAnswer) ? "That's the correct answer!" : "Not quite. Try again."
		},
		next(){
			if (this.index<this.mazes.length-1) ++this.index;
			this.setOutputs()
		},
		prev(){
			if (this.index>0) --this.index;
			this.setOutputs()
		},
	},
	mounted: function() {
		this.mazes.push("# # # # # # #\n# A . . . P #\n# P # # # # #\n# . . P . B #\n# # # # # # #")
		this.explanations.push("Here's the maze at the beginning. The mouse, marked M, starts on tile A.\nThe mouse needs to eat all the cheese, marked P- there are many paths it can take.")
		this.mazes.push("# # # # # # #\n# A M . . P #\n# P # # # # #\n# . . P . B #\n# # # # # # #")
		this.explanations.push("Although the cheese right below A is closer, it is more optimal to first collect the cheese at the top left.")
		this.mazes.push("# # # # # # #\n# A . M . P #\n# P # # # # #\n# . . P . B #\n# # # # # # #")
		this.explanations.push("The mouse moves to the right.")
		this.mazes.push("# # # # # # #\n# A . . M P #\n# P # # # # #\n# . . P . B #\n# # # # # # #")
		this.explanations.push("The mouse moves to the right.")
		this.mazes.push("# # # # # # #\n# A . . . M #\n# P # # # # #\n# . . P . B #\n# # # # # # #")
		this.explanations.push("The mouse collects the first cheese, and turns back to get all the others.")
		this.mazes.push("# # # # # # #\n# A . . . . #\n# M # # # # #\n# . . P . B #\n# # # # # # #")
		this.explanations.push("The mouse then moves leftward, to collect the cheese in the middle row. Some seconds are skipped for conciseness.")
		this.mazes.push("# # # # # # #\n# A . . . . #\n# . # # # # #\n# . . M . B #\n# # # # # # #")
		this.explanations.push("The mouse collects the third piece of cheese. It is then ready to reach the goal.")
		this.mazes.push("# # # # # # #\n# A . . . . #\n# . # # # # #\n# . . . . M #\n# # # # # # #")
		this.explanations.push("The goal is reached after 14 seconds. Therefore, 14 would be the answer to this maze.")

		//maybe looks better? idk
		for (var i = 0; i < this.mazes.length; ++i) this.mazes[i] = this.mazes[i].replaceAll(" ", "")
		this.index = 0
		this.setOutputs()

	}
});
 