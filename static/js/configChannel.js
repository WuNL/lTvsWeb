//////////////////////////////////////////////////////
// Repository management
///////////////////////////////////////////////////

$(document).ready(function(){
	$.ajaxSetup ({     
		// Disable caching of AJAX responses    
		cache: false
	});
	

	// var getTerminalList = function(){
				
	// 			$.get('/sdt-hts/addTerminals/', function(terminalList){
					
	// 				$("#terminalList").html('');
	// 				var i = 0;
	// 				var j = 0;
	// 				var k = 0;
	// 				var textToInsert = [];							
	// 				for(i; i < terminalList.length; i++){
	// 					textToInsert[j++] = '<tr>';
	// 					textToInsert[j++] = '<td>';
	// 					textToInsert[j++] = '<div class="item">' + terminalList[i].fields.name + '</div>';


	// 					textToInsert[j++] = '</td>\n';
	// 					textToInsert[j++] = '</tr>\n';			
						
	// 				}					
	// 				// if no repository
	// 				if ( terminalList.length === 0){
	// 					// print a nice message
	// 					// $('#terminalList').append("<td>尚未添加终端，请先在下方添加.</td><td></td><td></td>");
	// 				}					
	// 				$('#terminalList').append(textToInsert.join(''));
	// 				// register the new elements
	// 			}, "json");
	// };
	
	// getTerminalList();


	
	// register the actions

	
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