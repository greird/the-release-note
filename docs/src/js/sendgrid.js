(function () {
	const sg = window.sg = new SendGrid("<apiKey>");

	function SendGrid(apiKey) {
		if (!(this instanceof SendGrid)) {
			throw new TypeError("Class constructors cannot be invoked without 'new'");
		}
		this.apiKey = "Bearer " + apiKey;
		this.settings = {
			"async": true,
			"crossDomain": true,
			"headers": {
				"authorization": this.apiKey,
				"content-type": "application/json"
			}
		};
	}

	SendGrid.prototype.getRecipentsCount = function() {
		this.settings['url'] = "https://api.sendgrid.com/v3/contactdb/recipients/count";
		this.settings['data'] = {};
		this.settings['method'] = "GET";

		$.ajax(this.settings).done(function (response) {
			console.log(response);
		});
	};

	SendGrid.prototype.getRecipentsList = function() {
		this.settings['url'] = "https://api.sendgrid.com/v3/contactdb/recipients";
		this.settings['data'] = {};
		this.settings['method'] = "GET";

		$.ajax(this.settings).done(function (response) {
			console.log(response);
		});
	};

	SendGrid.prototype.addRecipient = function(email, deezer_user_id) {
		let data = JSON.stringify([
		{ 
			"email": email, 
			"deezer_user_id": Number(deezer_user_id)
		}
		]);
		this.settings['url'] = "https://api.sendgrid.com/v3/contactdb/recipients";
		this.settings['data'] = data;
		this.settings['method'] = "POST";
		this.settings['processData'] = false;

		$.ajax(this.settings).done(function (response) {
			console.log(response);
			console.log(response);
		});
	};

	SendGrid.prototype.addRecipientToList = function(recipientID, contactList) {
		var recipientID = String(recipientID);
		var contactList = String(contactList);
		this.settings['url'] = "https://api.sendgrid.com/v3/contactdb/lists/" + contactList + "/recipients/" + recipientID;
		this.settings['method'] = "POST";
		this.settings['data'] = "null";

		$.ajax(this.settings).done(function (response) {
			console.log(response);
		});	
	};

	SendGrid.prototype.getRecipent = function(recipientID) {
		var recipientID = String(recipientID);
		this.settings['url'] = "https://api.sendgrid.com/v3/contactdb/recipients/" + recipientID
		this.settings['data'] = {}
		this.settings['method'] = "GET";

		$.ajax(this.settings).done(function (response) {
			console.log(response);
		});
	}
}())