// Namespace to handle all blog related javascript

var blog = {

	// Pull all data out of the fields and return it
	// released will let the form know if this should be
	// published to the website right away or not.
	pull: function(released) {
		post = document.getElementById("post").innerHTML;
		tags = document.getElementById("tags").innerHTML;
		content = document.getElementById("content").innerHTML;

		return JSON.stringify({
			"post": post.replace(/(\r\n|\n|\r)/gm,""),
			"tags": tags.replace(/(\r\n|\n|\r)/gm,""),
			"content": content.replace(/(\r\n|\n|\r)/gm,""),
			"released": released.replace(/(\r\n|\n|\r)/gm,"")
		})
	},
	
	// Publish a new blog for view on the front end
	publish: function() {
		var request = new XMLHttpRequest();
		request.open('POST', '/admin/blogPost', true);
		request.setRequestHeader('Content-Type', 'application/json');
		data = blog.pull("published")
		request.send(data);
	},

	// Draft a new blog for view on the front end
	publish: function() {
		var request = new XMLHttpRequest();
		request.open('POST', '/admin/blogPost', true);
		request.setRequestHeader('Content-Type', 'application/json');
		data = blog.pull("draft")
		request.send(data);
	},

	// Update an already published blog
	update: function(id) {
		var request = new XMLHttpRequest();
		request.open('PUT', '/admin/blogPut/' + id, true);
		request.setRequestHeader('Content-Type', 'application/json');
		data = blog.pull("published")
		request.send(data);
	},

	exit: function() {
		// Send user back to the blog page
		window.location.replace("/admin/blog");
	}

}