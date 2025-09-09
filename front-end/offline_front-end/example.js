// Function that retrieves a DMN model or source code file.
async function getFile(file) {
    try {
        const response = await fetch(file);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        } else {
            const file = await response.text();
            return file;
        }
    } catch (error) {
        console.error("Error retrieving file:", error);
    }
}


// Function that processes the selected example in the front-end, and 
// initiates displaying the selected DMN model.
async function pickExample() {
    const case_id = document.getElementById("cases").value;

    try {
        // Retrieve the DMN model and corresponding source code file.
        const javaFileText = await getFile(`source_code/case${case_id}file.java`);
        const dmnModel = await getFile(`models/case${case_id}.txt`);

        localStorage.setItem('dmnModel', dmnModel);
        localStorage.setItem('javaFileText', javaFileText);

        // Redirect to the visualize.html page to display the DMN model.
        location.replace("http://127.0.0.1:5500/front-end/offline_front-end/visualizeExamples.html");
    } catch (error) {
        console.error("Error retrieving source code or DMN model:", error);
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

    // Put the DMN model saved in localStorage in the dmn-js modeler.
    dmnModel = localStorage.getItem("dmnModel");
    if (dmnModel) {
        model.importXML(dmnModel).then(() => {
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
    const lines_of_code = f;

    code.textContent = lines_of_code;

    code.classList.add("language-java");
    code.id = "line-of-code";

    pre.appendChild(code);
    codeContainer.appendChild(pre);

    // Add the syntax highlighting for the code.
    hljs.highlightElement(code);
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
        const lineOfCode = pre.innerText.split('\n').length;

        // Calculate the height of a single line of code.
        const height = (sourceCode.scrollHeight / lineOfCode) 

        // Scroll to the decision.
        pre.scrollTop = height * lineNumber;
    } 
}