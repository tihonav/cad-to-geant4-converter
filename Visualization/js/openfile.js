document.getElementById('btnOpen').onclick = function() {
  if ('FileReader' in window) {
    document.getElementById('exampleInputFile').click();
  } else {
    alert('Your browser does not support the HTML5 FileReader.');
  }
};

document.getElementById('exampleInputFile').onchange = function(event) {
  var fileToLoad = event.target.files[0];

  if (fileToLoad) {
    var reader = new FileReader();
    reader.onload = function(fileLoadedEvent) {
      var textFromFileLoaded = fileLoadedEvent.target.result;
      document.getElementById('exampleTextarea').value = textFromFileLoaded;
    };
    reader.readAsText(fileToLoad, 'UTF-8');
  }
};
