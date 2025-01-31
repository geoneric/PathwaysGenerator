setTimeout(function () {
    var oldMessageHandler = pythonWorker.onmessage;
    pythonWorker.onmessage = function (message) {
        if (message.data == "open_project") {
            openFile();
        } else {
            oldMessageHandler(message);
        }
    };
});

var file_open_input = document.createElement("input");
file_open_input.type = "file";
file_open_input.accept = ".pwproj";
file_open_input.multiple = false;

function openFile() {
    file_open_input.onchange = (e) => {
        // getting a hold of the file reference
        var file = e.target.files[0];
        console.log(file);

        // setting up the reader
        var reader = new FileReader();
        reader.readAsText(file, "UTF-8");

        reader.onload = (readerEvent) => {
            var content = readerEvent.target.result;
            pythonWorker.postMessage(
                JSON.stringify({
                    action: "open_project_result",
                    payload: content,
                })
            );
        };
    };

    file_open_input.click();
}
