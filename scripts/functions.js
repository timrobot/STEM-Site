var htmlPageKeys = ["home", "biology", "chemistry", "physics", "medicine", "mathematics", "robotics"];
var htmlPages = ["index.html", "biology.html", "chemistry.html", "physics.html", "medicine.html", "mathematics.html", "robotics.html"];

function cursorPointer() {
	document.body.style.cursor = "pointer";
}
function defaultPointer() {
	document.body.style.cursor = "auto";
}
function mousePointer() {
	document.body.style.cursor = "default";
}
function openURL(uri) {
	var index = htmlPages.indexOf(uri);
	index = htmlPageKeys.indexOf(uri);
	if (index != -1) {
		window.location.href = htmlPages[index];
	}
	window.location.href = uri;
}
function resetSearchBox() {
	if (document.getElementById('searchBox').value == '') {
		document.getElementById('searchBox').style.color = '#808080';
		document.getElementById('searchBox').value = 'Type search query then Enter';
	}
}
function selectSearchBox() {
	if (document.getElementById('searchBox').value == 'Type search query then Enter') {
		document.getElementById('searchBox').value = '';
		document.getElementById('searchBox').style.color = '#000000';
	}
}
var signal_level = 0;
function refreshSignal() {
	if (signal_level >= 0 && signal_level <= 3) {
		document.getElementById("searchImage").src = "images/lvl-" + signal_level + ".png";
	} else if (signal_level == 3) {
		document.getElementById("searchImage").src = "images/lvl-3.png";
	} else {
		document.getElementById("searchImage").src = "images/lvl-0.png";
	}
	signal_level = signal_level + 1;
	if (signal_level > 3) {
		signal_level = 0;
	}
	setTimeout('refreshSignal()', 500);
}
function init() {
	refreshSignal();
	resetSearchBox();
}
window.onload = init;
