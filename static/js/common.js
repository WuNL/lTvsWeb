	$.ajaxSetup ({     
		// Disable caching of AJAX responses    
		cache: false
	});
	function pushToDjango(){
		active = $("#packetGrepper").switchbutton("options").checked;
		ip = $("#id_ip").val();
		$.post("/sdt-hts/configPacketGrepper/",{'ip':ip,'active':active},
			function(data){
				if(data=="success"){
					$.messager.show({
						title:'通知!',
						msg:'保存成功',
						timeout:5000,
						showType:'slide',
					});
				}
				else if(data=="iperror"){
					$.messager.show({
						title:'警告!',
						msg:'IP无效！',
						timeout:5000,
						showType:'slide',
					});				
				}
				else{
					$.messager.show({
						title:'警告!',
						msg:data,
						timeout:5000,
						showType:'slide',
					});						
				}
			})
	}






 