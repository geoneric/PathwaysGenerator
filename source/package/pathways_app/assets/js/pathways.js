setTimeout(function () {
    var oldMessageHandler = pythonWorker.onmessage;
    pythonWorker.onmessage = function (message) {
        try {
            msgObj = JSON.parse(message.data);
            switch (msgObj.action) {
                case "open_project":
                    openFile();
                    break;
                case "save_project":
                    saveFile(msgObj.content, msgObj.filename);
                    break;
                default:
                    oldMessageHandler(message);
                    break;
            }
        } catch (e) {
            console.error(e);
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
        if (e.target.files.length == 0) return;

        var file = e.target.files[0];

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

var file_download_link = document.createElement("a");

function saveFile(data, filename) {
    var blob = new Blob([data], {
        type: "text/plain;charset=utf-8",
    });
    file_download_link.href = URL.createObjectURL(blob);
    file_download_link.download = filename;
    file_download_link.click();
}
