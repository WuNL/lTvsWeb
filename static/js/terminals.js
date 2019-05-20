//////////////////////////////////////////////////////
// Repository management
///////////////////////////////////////////////////

$(document).ready(function(){
	$.ajaxSetup ({     
		// Disable caching of AJAX responses    
		cache: false
	});

	// get the list of all repositories
	var refreshTerminalList = function(){

		$.get('/sdt-hts/addTerminals/', function(terminalList){

			$("#terminalList").html('');
			var i = 0;
			var j = 0;
			var k = 0;
			var textToInsert = [];	
			var textToInsertBase = [];									
			
			for(i; i < terminalList.length; i++){
				textToInsert[j++] = '<tr class=' + terminalList[i].pk + '>';

				textToInsert[j++] = '<td>' + terminalList[i].fields.name + '</td>\n';
				textToInsert[j++] = '<td>' + terminalList[i].fields.terminalIP + '</td>\n';

				textToInsert[j++] = '<td><!-- Icons -->';


				textToInsert[j++] = '<a href="/sdt-hts/editTerminals/'+ terminalList[i].pk+'/" class="editTerminals" title="编辑终端"><img src="/static/images/icons/pencil.png" alt="编辑终端" /></a>';
				textToInsert[j++] = '<a class="deleteRepo" href="#" title="删除"><img src="/static/images/icons/cross.png" alt="Delete" /></a>';

				textToInsert[j++] = '</td>';
				textToInsert[j++] = '</tr>\n';			

			}					
			// if no repository
			if ( terminalList.length === 0){
				// print a nice message
				$('#terminalList').append("<td>尚未添加终端，请先在下方添加.</td><td></td><td></td>");
			}					
			$('#terminalList').append(textToInsert.join(''));
			// register the new elements
			bindRepoBehaviors();
		}, "json");
	};
	
	refreshTerminalList();
	
	
	var bindRepoBehaviors = function() {
		// Delete a specified repo
		$(".deleteRepo").click(function(event){
			var terminalName = $(this).closest("tr").find('td:eq(0)').html();
			var terminalPK = $(this).closest("tr").attr("class");
			// delete the repo
			// configure confirm delete dialog
										$.ajax({
								url: '/sdt-hts/deleteTerminal/' + terminalPK + '/',
								type: 'DELETE',
								success: function(data) {
									// repo successfully delete
					$.messager.show({
						title:'通知!',
						msg:"删除成功",
						timeout:5000,
						showType:'slide',
					});	
									refreshTerminalList();
								},
								error: function(error) {
					$.messager.show({
						title:'通知!',
						msg:"删除失败",
						timeout:5000,
						showType:'slide',
					});	
								}
							});
			// prevent the default action, e.g., following a link
			return false;
			
			
		});
		
		// Delete a specified repo
		$(".importRepo").click(function(event){
			var reponame = $(this).closest("tr").attr("class");
			// delete the repo
			// configure confirm delete dialog
			var $dialog = $('<div></div>')
				.html('<br />Would you like to import ' + reponame + ' to GitStack ?')
				.dialog({
					autoOpen: false,
					title: 'Import ' + reponame,
					modal: true,
					height:140,
					buttons: {
						// delete function
						Import: function() {
							// perform the request to delete the repo
							data = '{"bare": true}';
							
							
							$.ajax({
								url: '/rest/repository/' + reponame + '/',
								type: 'PUT',
								contentType: 'application/json',
								data: data,
								success: function(data) {
									// repo successfully delete
									showMessage("success", data);
									refreshRepoList();
								},
								error: function(error) {
									showMessage("error", error.responseText);
								}
							});
							
							
							$( this ).dialog( "close" );
						},
						// Abord function
						Cancel: function() {
							$( this ).dialog( "close" );
						}
					}
				});
				
			$dialog.dialog('open');
			// prevent the default action, e.g., following a link
			return false;
			
			
		});
	};
	bindRepoBehaviors();
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