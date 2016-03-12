document.getElementById('btnOpen').onclick = function() {
	if ('FileReader' in window) {
		document.getElementById('exampleInputFile').click();
	}
	else 
	{
		alert('Your browser does not support the HTML5 FileReader.');
	}
};


document.getElementById('exampleInputFile').onchange = function(event) {
	var fileToLoad = event.target.files[0];
	
	var values = [];
	if (fileToLoad) {
		var reader = new FileReader();
		reader.onload = function(fileLoadedEvent) {
			var textFromFileLoaded = fileLoadedEvent.target.result;
			//document.getElementById('exampleTextarea').value = textFromFileLoaded.split("\n")[0];
			alllines = textFromFileLoaded.split("\n");
			//var text = "";
			for(i=0;i<alllines.length;i++){
				var polygon = [];
				strvalues = alllines[i].split(",");
				if(strvalues.length<2) continue;
				for(j=0;j<strvalues.length;j++)
				{
					polygon.push(parseFloat(strvalues[j]));
					//document.getElementById('exampleTextarea').value = polygon.length;
				}
				//text+= polygon.length.toString() + "\n"; 
				if(!polygon.length || polygon.length%3)
				{
					alert('Error parsing csv geomatry file!');
					break;
				}
			}
			//document.getElementById('exampleTextarea').value = text;
		};
		reader.readAsText(fileToLoad, 'UTF-8');
	}
};
