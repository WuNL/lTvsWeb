/////////////////////////////////
// Administrator password change
////////////////////////////////

$(document).ready(function(){
	$.ajaxSetup ({     
		// Disable caching of AJAX responses    
		cache: false
	}); 
	
	$("#setNewAdminPassword").click(function(event){
		// the form info
		var old_password = $("#txtOldPassword").val();
		var new_password1 = $("#txtNewPassword1").val();
		var new_password2 = $("#txtNewPassword2").val();
		
		// Check if both new passwords are the same
		if(new_password1 === new_password2){
			// passwords are the same
			// Call the rest interface to change the admin password
			// proceed to the update
			$.ajax({
				url: '/rest/settings/general/admin/',
				type: 'PUT',
				contentType: 'application/json',
				data: '{"oldPassword": "' + old_password + '","newPassword": "' + new_password1 + '"}',
				success: function(data) {
					showMessage("success", data);
				},
				error: function(error) {
					showMessage("error", error.responseText);
				}
			});
		} else {
			showMessage("error", 'New passwords fields are not the same');
		}

	
	});
	
	//////////////////////////////
	// web based repository browsing
	/////////////////////////////////
	// update the checkbox for the web interface
	var refreshWebinterface = function(){
		var url = '/rest/settings/general/webinterface/';
		$.get(url, function(webinterface){
			// if the web interface is enabled
			if(webinterface['enabled'] == true)
				// check the box
				$('input[name=webinterface]').attr('checked', true);

		}, "json");
	};
	
	// Click on the checkbox, enable or disable the web interface
	$("#webinterface").click(function(event){
		// Get the status of the checkbox
		isChecked = false;
		if($('input[name=webinterface]').attr('checked') === 'checked')
			isChecked = true;
		
		// Setup the data to be send to the server
		data = '{"enabled": ' + isChecked +'}';
		
		var url = '/rest/settings/general/webinterface/';
		// Proceed to the request
		$.ajax({
			url: url,
			type: 'PUT',
			contentType: 'application/json',
			data: data,
			success: function(data) {
				showMessage("success", data);
			},
			error: function(error) {
				showMessage("error", error.responseText);
			}
		});
					
	});
	
	refreshWebinterface();
	
	////////////////////////////////
	// Server port
	//////////////////////////////
	var refreshPort = function(){

		var url = '/rest/settings/general/port/';
		$.get(url, function(ports){

			$('#httpPort').val(ports['httpPort']);
			$('#httpsPort').val(ports['httpsPort']);
			
		}, "json");
		
		
	};
	
	// save the ports numbers
	$("#btnSavePort").click(function(event){
		httpPort = $('#httpPort').val();
		httpsPort = $('#httpsPort').val();
		
		// check is numeric
		if(!isNaN(httpPort) && !isNaN(httpsPort)){
			$.ajax({
				url: '/rest/settings/general/port/',
				type: 'PUT',
				contentType: 'application/json',
				data: '{"httpPort": "' + httpPort + '", "httpsPort": "' + httpsPort + '"}',
				success: function(data) {
					showMessage("success", data);
				},
				error: function(error) {
					showMessage("error", error.responseText);
				}
			})			
		} else {
			showMessage("error", "Please enter a port number");
		}
	

	
	});
	
	
	refreshPort();
	
	////////////////////////////////
	// Repositories location
	//////////////////////////////
	var refreshLocation = function(){

		var url = '/rest/settings/general/repositorylocation/';
		

		$.get(url, function(location){
			$('#repoLocation').val(location['repositories']);
			
		}, "json");
	};
	
	// save the ports numbers
	$("#btnSaveLocation").click(function(event){
		repoLocation = $('#repoLocation').val();
		
		// check is numeric
		$.ajax({
			url: '/rest/settings/general/repositorylocation/',
			type: 'PUT',
			contentType: 'application/json',
			data: '{"repositories": "' + repoLocation + '"}',
			success: function(data) {
				showMessage("success", data);
			},
			error: function(error) {
				showMessage("error", error.responseText);
			}
		})			
		
	

	
	});
	
	refreshLocation();
	
	/////////////////////////////////
	// Handle notifications 
	///////////////////////////////
	var showMessage = function (messageType, messageText) {
		// Success message
		if(messageType == "success"){
			$('#successMessageBox').show();
			$('#successMessage').html(messageText).show();
			$('#errorMessageBox').hide();
		// error message
		} else if (messageType == "error"){
			$('#successMessageBox').hide();
			$('#errorMessageBox').show();
			$('#errorMessage').html(messageText);
		}
			
	}
});