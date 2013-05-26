var expand = true;
function focusSearchBox() {
	generateSearchBox();
}
function blurSearchBox() {
	document.getElementById("searchBox").innerHTML = "";
	contractSearchBox();
}
function contractSearchBox() {
	var marginTop = document.getElementById("topcontainer").style.marginTop;
	var end = marginTop.indexOf("px");
	var pixels = 0;
	document.getElementById("searchText").innerHTML = "";
	if (end != -1) {
		pixels = parseInt(marginTop.slice(0, end));
		if (pixels <= 0) {
			document.getElementById("topcontainer").innerHTML = "";
			document.getElementById("topcontainer").style.height = "0px";
			document.getElementById("topcontainer").style.marginTop = "0px";
			document.getElementById("topcontainer").style.marginBottom = "0px";
			document.getElementById("topcontainer").style.width = "0%";
			return;
		}
		pixels -= 5;
		document.getElementById("topcontainer").style.marginTop = pixels + "px";
		document.getElementById("topcontainer").style.marginBottom = pixels * 2 + "px";
	}
	var height = document.getElementById("topcontainer").style.height;
	end = height.indexOf("px");
	if (end != -1) {
		pixels = parseInt(height.slice(0, end));
		pixels -= 6;
		document.getElementById("topcontainer").style.height = pixels + "px";
	}
	setTimeout("contractSearchBox()", 25);
}
function generateSearchBox() {
	var marginTop = document.getElementById("topcontainer").style.marginTop;
	var end = marginTop.indexOf("px");
	var pixels = 0;
	if (document.getElementById("topcontainer").innerHTML != "") {
	    return;
	}
	if (end != -1) {
		pixels = parseInt(marginTop.slice(0, end));
		if (pixels >= 30) {
			var code = "<form action='search.html' method='post'>";
			code += "		<input type='text' name='query' id='searchBox' onblur='blurSearchBox()' style='opacity:0'></input>";
			code += "	</form>";
			code += "<div id='searchText' style='text-align:center;margin:18px;font-size:18px;color:rgb(108, 108, 108);opacity:0'>Press Enter to Search</div>";
			document.getElementById("topcontainer").innerHTML = code;
			expandSearchBox();
			return;
		}
		pixels += 5;
		document.getElementById("topcontainer").style.marginTop = pixels + "px";
		document.getElementById("topcontainer").style.marginBottom = pixels * 2 + "px";
	}
	var height = document.getElementById("topcontainer").style.height;
	end = height.indexOf("px");
	if (end != -1) {
		pixels = parseInt(height.slice(0, end));
		pixels += 6;
		document.getElementById("topcontainer").style.height = pixels + "px";
	}
	setTimeout("generateSearchBox()", 25);
}
function expandSearchBox() {
	var width = document.getElementById("topcontainer").style.width;
	var end = width.indexOf("%");
	if (end != -1) {
	    var percent = parseInt(width.slice(0, end));
		if (percent >= 100) {
		    document.getElementById("searchBox").focus();
			return;
		}
		percent += 10;
		document.getElementById("topcontainer").style.width = percent + "%";
	    if (percent > 0) {
	        document.getElementById("searchText").style.opacity = percent / 100.0;
	        document.getElementById("searchBox").style.opacity = percent / 100.0;
	    }
		setTimeout("expandSearchBox()", 25);
	}
}
function pointerCursor() {
	document.body.style.cursor = "pointer";
}
function autoCursor() {
	document.body.style.cursor = "auto";
}
