# DeCoMi – Decision Source Code Mining  
A prototype by Annemae van de Hoef  

## Overview
This repository contains the final prototype developed for the thesis on extracting DMN models from source code.

## How to Start  
Unfortunately, the original version of the prototype cannot be run, as the LLMs initially used are no longer available due to discontinuation and the expiration of trial access. An 'offline' version of the prototype is provided, which shows 5 DMN models extracted using the prototype. The offline version can be found here: https://decomi-prototype.web.app/

Nevertheless, the following instructions demonstrate how the prototype can be set up and run locally, even though the full functionality with the original LLMs is not available:

```shell
git clone https://github.com/Annemae/DeCoMi
cd back-end/src/
pip install .
```
Once the dependencies are installed, the back-end can be started using:

```shell
flask run
```

After the back-end is running, the front-end can be deployed using a suitable extension, such as Live Server, which serves the HTML, CSS, and JavaScript files locally in a web browser. This local setup allows full interaction with the prototype, even in an offline environment.

## Project Structure  
- **back-end**  
  - `prototype_results`: contains example prototype results generated via the back-end for logic extraction using both Gemini 2.5 Pro and GPT-4.1 across all temperature settings. These results were generated because Gemini 2.5 Pro was discontinued during the conduction of the experiments, and at the time, the optimal settings for decision logic extraction were not yet determined. By generating prototype results for all possible scenarios prior to discontinuation, it was ensured that the data could be used later in the thesis.
  - `src`: contains the back-end source code of the prototype, including a Flask API and the implementation of the core prototype steps.
- **data**: includes ten experimental cases used for experimentation and validation, representing the gold standard, as well as some illustrative examples. Each case contains the following components:
  - The DMN XML file containing the complete DMN model (used for the DMN model conversion experiment).
  - The whole Java source code file in which all decisions are present (used for the decision identification experiment).
  - The Java source code containing only the relevant decisions for the case.
  - The JSON object defining the relevant decisions for the case (used for the decision identification experiment).
  - The decision requirement level JSON object (used for the DRD extraction experiment).
  - The decision logic level JSON objects, one for each individual decision (used for the decision table extraction experiment).
- **experiment**: contains the queries and results from all four experiments, including all iterations conducted with GPT-4.1 and Gemini 2.5 Pro.
- **front-end**: contains the front-end of the prototype, including the CSS, HTML, and JavaScript files, as well as the code for the 'offline' version.

## Software Quality  
During development of the prototype, the following quality aspects were considered:  

- **Functionality**: the software was implemented according to the requirements defined in the thesis.  
- **Usability**: although no formal usability requirements were specified, the front-end was designed with a simple and intuitive UX. For example, users can navigate directly to a decision in the source code by clicking on it in the DMN model.
- **Maintainability**: explanatory comments were added to the front-end and back-end source code, and `flake8` was applied to the back-end to encourage compliance with Python style guidelines [IN PROGRESS].  
