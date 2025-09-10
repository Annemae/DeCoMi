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
// initiates displaying the extracted DMN model in the front-end.
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
            const dmnModels = data.models;

            localStorage.setItem('dmnModels', JSON.stringify(dmnModels))
            // Sets the default DMN model to the first model in the list.
            localStorage.setItem('selectedModel', 1)
            localStorage.setItem('javaFileText', javaFileText);

            // Redirect to the visualize.html page to display the DMN model.
            location.replace("http://127.0.0.1:5500/front-end/html/visualize.html");
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
        height: 770,
        width: '100%',
        keyboard: {
            bindTo: window
        }
    });

    // Get the DMN model saved in localStorage to put in dmn-js modeler.
    dmnModels = JSON.parse(localStorage.getItem('dmnModels'));
    // Get the selected model number.
    modelNumber = parseInt(localStorage.getItem('selectedModel'), 10) - 1;

    if (dmnModels) {
        model.importXML(dmnModels[modelNumber]).then(() => {
            // Create an event listener that jumps to the section of the source code 
            // that corresponds to the element clicked on in the DMN model.
            const activeEditor = model.getActiveViewer();
            const eventBus = activeEditor.get('eventBus');

            eventBus.on('element.click', function(event) {
                const element = event.element;
                if (element.type === 'dmn:Decision') {
                    jumpToDecision(element.businessObject.name);
                }
            });
        });
        

        // Loads in the DMN model options into the model picker.
        modelPicker = document.getElementById('model-picker');
        modelSelect = document.getElementById('model-select');
        if (dmnModels.length >= 1) {
            modelPicker.hidden = false;
            modelPicker.style.display = "flex";

            // Add for each model number an option in the select element.
            for (let number = 1; number <= dmnModels.length; number++) {
                option = document.createElement('option');
                option.innerText = number;
                option.value = number;
                modelSelect.appendChild(option);
            }
        } 

        // Add event listener to change visualized DMN model, based on selection.
        modelSelect.addEventListener('change', function() {
            const selected_model_number = modelSelect.value;
            localStorage.setItem('selectedModel', selected_model_number);
            
            // Reload page to load in selected DMN model.
            location.replace("http://127.0.0.1:5500/front-end/html/visualize.html");
        })
    } else {
        model.importXML(defaultDMN);
        window.alert("No DMN model was found. Please upload a Java source code file first.");
    }
}

// Function that loads the source code in the UI.
function loadSourceCodeInUI() {
    codeContainer = document.getElementById("source-code-container");
    f = localStorage.getItem('javaFileText');

    const pre = document.createElement("pre");
    pre.id = "source-code"; 
    code = document.createElement("code");

    // Make sure the source code is displayed in the correct format.
    for (let line in f.split('\n')) {
        line = f.split('\n')[line];

        code.innerHTML += line + "\n";
    }

    code.classList.add("language-java");
    code.id = "line-of-code";
    pre.appendChild(code);

    // Add the syntax highlighting for the code.
    hljs.highlightElement(code);

    codeContainer.appendChild(pre);
}

// Function that jumps to a decision in the source code, when clicked on in the DMN model.
function jumpToDecision(decisionName) {
    sourceCode = document.getElementById("source-code");
    const linesOfCode = sourceCode.innerText.split('\n');

    let lineNumber = -1;
    for (let i = 0; i < linesOfCode.length; i++) {
        if (linesOfCode[i].includes(decisionName)) {
            lineNumber = i;
            break;
        } 
    }

    if (lineNumber !== -1) {
        const pre = document.getElementById("source-code");
        const sourceCode = document.getElementById("line-of-code");
        const lineOfCode = pre.innerText.split('\n').length - 1;

        // Calculate the height of a single line of code.
        const height = (sourceCode.scrollHeight / lineOfCode) 

        // Scroll to the decision.
        pre.scrollTop = height * lineNumber;
    } 
}