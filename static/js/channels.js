//////////////////////////////////////////////////////
// Repository management
///////////////////////////////////////////////////

$(document).ready(function(){
	$.ajaxSetup ({     
		
		cache: false
	});
	
	
	var refreshChannelList = function(){
		
		$.get('/sdt-hts/configChannels/', function(channelList){
			$("#channelList").html('');
			var i = 0;
			var j = 0;
			var k = 0;
			var m = 0;
			var textToInsert = [];	
			var textToInsertBase = [];		
			var textToInsertPolling = [];								
			
			for(i; i < channelList.length; i++){
				textToInsert[j++] = '<tr class=' + channelList[i].name + '>';
				textToInsert[j++] = '<td>' + channelList[i].pk + '</td>\n';
				textToInsert[j++] = '<td>' + channelList[i].fields.name + '</td>\n';
				textToInsert[j++] = '<td>' + channelList[i].fields.saperateNumber + '</td>\n';
				textToInsert[j++] = '<td>' + channelList[i].fields.content + '</td>\n';
				textToInsert[j++] = '<td><!-- Icons -->';

				textToInsert[j++] = '<a href="/web/index.php?p=' + channelList[i].fields.name + '.git&a=summary" title="Browse"><img src="/static/images/icons/magnifier.png" alt="Browse" /></a>';
				textToInsert[j++] = '<a href="/gitstack/repository/' + channelList[i].fields.name + '/permission/" class="editUsers" title="Permissions"><img src="/static/images/icons/users.png" alt="Permissions" /></a>';
				textToInsert[j++] = '<a class="deleteRepo" href="#" title="Delete"><img src="/static/images/icons/cross.png" alt="Delete" /></a>';

				textToInsert[j++] = '</td>';
				textToInsert[j++] = '</tr>\n';	
				textToInsertBase[k++] = '<li><a href="/sdt-hts/configChannel/' + channelList[i].pk + '/' + channelList[i].fields.saperateNumber + '/" </a>'
				textToInsertBase[k++] = channelList[i].fields.name + '</a></li>'
				textToInsertPolling[m++] = '<li><a href="/sdt-hts/configPolling/' + channelList[i].pk + '/' + channelList[i].fields.saperateNumber + '/" </a>'
				textToInsertPolling[m++] = channelList[i].fields.name + '</a></li>'
			}


			if ( channelList.length === 0){

				$('#channelList').append("<td>尚未添加通道，请先在下方添加.</td><td></td><td></td>");
			}

			$('#channelList').append(textToInsert.join(''));
			$('#configChannelBase').append(textToInsertBase.join(''));
			$('#configPolling').append(textToInsertPolling.join(''));


		}, "json");
		
	};
	
	refreshChannelList();
	

	
	$("#btnCreateChannel").click(function(event){

		var csrf = $('input[name="csrfmiddlewaretoken"]').val();
		var form = $('#formCreateChannel').serialize();
		console.log(form)

		$.post("/sdt-hts/configChannels/", $('#formCreateChannel').serialize() )
		.success(function() {
			$('#successMessageBox').show();
			$('#successMessage').html('添加通道成功').show();
			
			$('#errorMessageBox').hide();
			refreshChannelList();
		})
		.error(function(error) {
			$('#successMessageBox').hide();
			$('#errorMessageBox').show();
			$('#errorMessage').html(error.responseText);
		});
	});
	


	

	var showMessage = function (messageType, messageText) {

		if(messageType == "success"){
			$('#successMessageBox').show();
			$('#successMessage').html(messageText).show();
			$('#errorMessageBox').hide();

		} else if (messageType == "error"){
			$('#successMessageBox').hide();
			$('#errorMessageBox').show();
			$('#errorMessage').html(messageText);
		}
		
	}
});