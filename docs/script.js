document.getElementById("btnSubmit").addEventListener("click", loadFile);

function loadFile() {
    var file = document.getElementById("file-selector");
    var reader = new FileReader();
    reader.onload = function () {
        var text = reader.result;
        populateScreen(text)
    }
    reader.readAsText(file.files[0]);
}

function populateScreen(textJson) {
    var json = JSON.parse(textJson);
    let divContent = document.getElementById("divContent");
    document.getElementById("infoToHide").style.display = "none";
    for (var i = 0; i < json.length; i++) {
        let group = json[i];
        var newCol = document.createElement("DIV");
        newCol.classList.add("col-score");

        newCol.innerHTML += "<h3> <center> Score do Grupo: " + group["scoreGroup"] + "</center></h3>";
        newCol.innerHTML += "<ul>";
        for (var j = 0; j < group["group"].length; j++) {
            let element = group["group"][j];
            newCol.innerHTML += "<li><b>" + element["score"] + "</b> - " + element["code"] + " - " + element["name"];
            newCol.innerHTML += "</li>";
        }
        newCol.innerHTML += "</ul>";

        divContent.appendChild(newCol);
    }
}