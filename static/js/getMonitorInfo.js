//////////////////////////////////////////////////////
// Repository management
///////////////////////////////////////////////////

$(document).ready(function(){
	$.ajaxSetup ({     
		
		cache: false
	});
	
	
	var refreshChannelList = function(){
		
		$.get('/sdt-hts/getMonitorInfo/', function(channelList){
			$("#channelList").html('');
			$('#configChannelBase').html('');
			$('#configPolling').html('');
			var i = 0;
			var j = 0;
			var k = 0;
			var m = 0;
			var textToInsert = [];	
			var textToInsertBase = [];		
			var textToInsertPolling = [];								
			
			for(i; i < channelList.length; i++){
				textToInsert[j++] = '<tr class=' + channelList[i].pk + '>';
				textToInsert[j++] = '<td>' + channelList[i].pk + '</td>\n';
				textToInsert[j++] = '<td>' + channelList[i].fields.GPUSeq + '</td>\n';
				textToInsert[j++] = '<td>' + channelList[i].fields.monitorName + '</td>\n';
				textToInsert[j++] = '<td>' + channelList[i].fields.resolution + '</td>\n';
				textToInsert[j++] = '<td>' + channelList[i].fields.freshRate + '</td>\n';
				textToInsert[j++] = '<td>' + channelList[i].fields.inUse + '</td>\n';

				textToInsert[j++] = '</tr>\n';	
				textToInsertBase[k++] = '<li><a href="/sdt-hts/configChannel/' + channelList[i].pk + '/' + channelList[i].fields.saperateNumber + '/" </a>'
				textToInsertBase[k++] = channelList[i].fields.name + '</a></li>'
				textToInsertPolling[m++] = '<li><a href="/sdt-hts/configPolling/' + channelList[i].pk + '/' + channelList[i].fields.saperateNumber + '/" </a>'
				textToInsertPolling[m++] = channelList[i].fields.name + '</a></li>'
			}


			if ( channelList.length === 0){

				$('#channelList').append("<td>尚未接入显示设备，请接入显示设备后点击获取设备信息或者刷新页面.</td><td></td><td></td>");
			}

			$('#channelList').append(textToInsert.join(''));
			$('#configChannelBase').append(textToInsertBase.join(''));
			$('#configPolling').append(textToInsertPolling.join(''));


		}, "json");
		
	};
	
	refreshChannelList();
	

	
	$("#getMonitorInfo").click(function(event){

		var csrf = $('input[name="csrfmiddlewaretoken"]').val();
		$.post("/sdt-hts/getMonitorInfo/",{'var1':1},
						function(data){
				if(data!="刷新显示器成功"){
					$.messager.show({
						title:'警告!',
						msg:data,
						timeout:5000,
						showType:'slide',
					});
				}
				else{
					refreshChannelList();
					$.messager.show({
						title:'获取成功',
						msg:data,
						timeout:5000,
						showType:'slide',
					});					
				}
			}
			);
		// .success(function() {
		// 	$('#successMessageBox').show();
		// 	$('#successMessage').html('刷新成功').show();
		
		// 	$('#errorMessageBox').hide();
		// 	refreshChannelList();
		// })
		// .error(function(error) {
		// 	$('#successMessageBox').hide();
		// 	$('#errorMessageBox').show();
		// 	$('#errorMessage').html(error.responseText);
		// });
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