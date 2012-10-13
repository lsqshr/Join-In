// JavaScript Document

function createGroup() {
	alert("You want to Create a group!");
}

function settings() {
		alert("You want to modify Settings!");
}

function mostraEscondeMsg(idCampo, mostra){	

	if (mostra == true) {
		document.getElementById(idCampo).style.display = "block";
	} else {
		document.getElementById(idCampo).style.display = "none"; 
	}		
}
	
function fechaTempo(idCampo, tempo){
	tempo = Math.ceil(tempo);
	setTimeout("document.getElementById('"+idCampo+"').style.visibility='hidden'", tempo);
}

function addGroups(idField, value) {
	
	oldValue = document.getElementById(idField).value;
	newValue = oldValue + ";" + value;
	document.getElementById(idField).value = newValue;
	
}





