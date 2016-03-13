//var allgeometry = []




//* minimal three.js code
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight , 0.1, 10000 );

var renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth , window.innerHeight   );
document.body.appendChild( renderer.domElement );
var group = new THREE.Group();
var geom = new THREE.Geometry(); 

/*
//* cube example
var geometry = new THREE.BoxGeometry( 1, 1, 1 );
var material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
var cube = new THREE.Mesh( geometry, material );
scene.add( cube );
camera.position.z = 5;
*/












document.getElementById('btnOpen').onclick = function() {
	if ('FileReader' in window) {
		document.getElementById('exampleInputFile').click();
	}
	else 
	{
		alert('Your browser does not support the HTML5 FileReader.');
	}
};


function createGeometry(polygons)
{
	var NVERTPOLYGON = 3;
	for(ipolygon=0; ipolygon<polygons.length; ipolygon++){
		var polygon = polygons[ipolygon];
		var nvert = polygon.length /NVERTPOLYGON;
		//var geom = new THREE.Geometry(); 
		for(ivert = 0; ivert< nvert; ivert++){
			geom.vertices.push(new THREE.Vector3(polygon[ivert*3],polygon[ivert*3+1],polygon[ivert*3+2]));
		}
		if(nvert==NVERTPOLYGON){
			geom.faces.push( new THREE.Face3( ipolygon*NVERTPOLYGON, ipolygon*NVERTPOLYGON+ 1,ipolygon*NVERTPOLYGON+ 2 ) );
			//geom.faces.push( new THREE.Face3( 0, 2, 1 ) );
			geom.computeFaceNormals();
		}
		else{
			var message = 'Unrecognized geometry type ==> so far only allow triangulated solids, while nvert='+nvert.toString();
			alert(message);
		}


		//object.position.z = -100;//move a bit back - size of 500 is a bit big
		//object.rotation.y = -Math.PI * .5;//triangle is pointing in depth, rotate it -90 degrees on Y

		//scene.add(object);
		//group.add(object);



		//console.log(allgeometry[igeom].length);
	}
	//scene.add( group );
	var object = new THREE.Mesh( geom, new THREE.MeshNormalMaterial({ color: 0x00ff00 }) );
	group.add(object)
	scene.add(group);
	//console.log("aaaa="+polygons.length.toString());
	camera.position.z = 1000;
	

	/*
	var geometry = new THREE.BoxGeometry( 1, 1, 1 );
	var material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
	var cube = new THREE.Mesh( geometry, material );
	scene.add( cube );
	camera.position.z = 5;
	*/

	/*
	var geom = new THREE.Geometry(); 
	geom.vertices.push(new THREE.Vector3(0,0,0));
	geom.vertices.push(new THREE.Vector3(1,0,0));
	geom.vertices.push(new THREE.Vector3(0,1,0));
	geom.faces.push( new THREE.Face3( 0, 1, 2 ) );
	geom.computeFaceNormals();
	var object = new THREE.Mesh( geom, new THREE.MeshNormalMaterial({ color: 0x00ff00 }) );
	scene.add(object);


	var geom = new THREE.Geometry(); 
	geom.vertices.push(new THREE.Vector3(1,1,0));
	geom.vertices.push(new THREE.Vector3(0,1,0));
	geom.vertices.push(new THREE.Vector3(1,0,0));
	geom.faces.push( new THREE.Face3( 0, 1, 2 ) );
	geom.computeFaceNormals();
	var object = new THREE.Mesh( geom, new THREE.MeshNormalMaterial({ color: 0x00ff00 }) );
	scene.add(object);
	

	camera.position.z = 5.;
	*/

	
}

document.getElementById('exampleInputFile').onchange = function(event) {
	for(ifile=0; ifile<event.target.files.length; ifile++){
		var fileToLoad = event.target.files[ifile];

		if (fileToLoad) {

			var values = [];
			var reader = new FileReader();
			reader.onload = function(fileLoadedEvent) {
				// *
				// * read csv file
				// *
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
						alert('Error parsing csv geomatry file! ==> number of vertices = '+polygon.length.toString());
						break;
					}
					values.push(polygon);
				}
				//document.getElementById('exampleTextarea').value = text;
				//allgeometry.push(values);
				//alert("test "+allgeometry.length.toString());

				// *
				// * process geometry
				// *
				createGeometry(values);
			};
			reader.readAsText(fileToLoad, 'UTF-8');
		}
	}
};



// * render the scene
function render() {
	//console.log(allgeometry.length);
	requestAnimationFrame( render );

	//window.alert(document.getElementById('inputButton').value);

	group.rotation.x += 0.1;
	group.rotation.y += 0.1;

	renderer.render( scene, camera );
}
render();
