// Default DMN model used to trigger the dmn-js model functionality.
const defaultDMN = `<?xml version="1.0" encoding="UTF-8"?>
                    <definitions xmlns="https://www.omg.org/spec/DMN/20191111/MODEL/"
                        id="DMN Diagram"
                        name="DMN Diagram">
                    </definitions>`;

// Function that reads a file and returns its content as a string.
function readFile(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = () => resolve(reader.result);
        reader.onerror = () => reject(reader.error);

        reader.readAsText(file);
    });
}

// Function that sends the selected user file to the back-end for DMN model extraction, and 
// displays the extracted DMN model in the front-end.
async function sendFile() {
    const url = "http://127.0.0.1:5000/extract";
    const user_file = document.getElementById("file").files[0];

    // If no file is selected, alert the user.
    if (!user_file) {
        alert("Please select a file.");
        return;
    }

    // Show in the UI that a DMN model is being extracted.
    div = document.getElementById("input-file");
    div.innerHTML = '';

    h3 = document.createElement('h3');
    h3.innerText = "DMN Model is being created..."

    p = document.createElement('p');
    p.innerText = "This may take some time."

    div.appendChild(h3);
    div.appendChild(p);

    // Read the file and send it to the back-end.
    try {
        javaFileText = await readFile(user_file);

        const formData = new FormData();
        formData.append("file", new Blob([javaFileText], { type: "text/plain" }));

        const response = await fetch(url, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Something went wrong while sending the file.");
        } else {
            const data = await response.json();
            const dmnModel = data.model;

            localStorage.setItem('dmnModel', dmnModel);
            localStorage.setItem('javaFileText', javaFileText);

            // Redirect to the visualize.html page to display the DMN model.
            location.replace("http://127.0.0.1:5500/frontend/html/visualize.html");
        }
    } catch (error) {
        console.error("Error reading or sending file:", error);
    }
}

// Function that loads the DMN model in the UI using dmn-js.
function loadDMNModelInUI() {
    loadSourceCodeInUI();

    const model = new DmnJS({
        container: '#dmn-model',
        height: 675,
        width: '100%',
        keyboard: {
            bindTo: window
        }
    });

    // Put the DMN model saved in localStorage in the dmn-js modeler.
    dmnModel = localStorage.getItem('dmnModel');
    if (dmnModel) {
        model.importXML(dmnModel);
    } else {
        model.importXML(defaultDMN);
        window.alert("No DMN model was found. Please upload a Java source code file first.");
    }
}

// Function that loads the source code in the UI.
function loadSourceCodeInUI() {
    // TODO hightlight the source code.
    codeContainer = document.getElementById("source-code-container");
    f = localStorage.getItem('javaFileText');

    const pre = document.createElement("pre");
    pre.id = "source-code";
    pre.textContent = f; 

    codeContainer.appendChild(pre);
}
