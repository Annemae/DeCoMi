"""extract_decisions.py file.

Extract all functions from source code that contain DMN elements.
"""
from openai import AzureOpenAI
import json
from typing import List


# Examples used for few-shot prompting.
# Contains input JSON objects and expected identified decisions based on these objects.
example_1_input = """
/**
 * Returns the next element in {@code iterator} or {@code defaultValue} if the iterator is empty.
 * The {@link Iterables} analog to this method is {@link Iterables#getFirst}.
 *
 * @param defaultValue the default value to return if the iterator is empty
 * @return the next element of {@code iterator} or the default value
 * @since 7.0
 */
public static <T> @Nullable T getNext(Iterator<? extends T> iterator, @Nullable T defaultValue) {
    return iterator.hasNext() ? iterator.next() : defaultValue;
}
"""
example_1_output = """
{
    "Decisions": [
        {"Model": "model_1",
        "FunctionName": "getNext(Iterator<? extends T> iterator, @Nullable T defaultValue)"}]
}
"""

example_2_input = """
//-----------------------------------------------------------------------
/**
 * Validates an interval.
 *
 * @param start  the start instant in milliseconds
 * @param end  the end instant in milliseconds
 * @throws IllegalArgumentException if the interval is invalid
 */
protected void checkInterval(long start, long end) {
    if (end < start) {
        throw new IllegalArgumentException("The end instant must be greater than the start instant");
    }
}
"""
example_2_output = """
{
    "Decisions": [
        {"Model": "model_1",
        "FunctionName": "checkInterval(long start, long end)"}]
}
"""

example_3_input = """
/**
 * Default {@link SchemePortResolver}.
 *
 * @since 4.3
 */
@Contract(threading = ThreadingBehavior.IMMUTABLE)
public class DefaultSchemePortResolver implements SchemePortResolver {

    public static final DefaultSchemePortResolver INSTANCE = new DefaultSchemePortResolver();

    @Override
    public int resolve(final HttpHost host) throws UnsupportedSchemeException {
        Args.notNull(host, "HTTP host");
        final int port = host.getPort();
        if (port > 0) {
            return port;
        }
        final String name = host.getSchemeName();
        if (name.equalsIgnoreCase("http")) {
            return 80;
        } else if (name.equalsIgnoreCase("https")) {
            return 443;
        } else {
            throw new UnsupportedSchemeException(name + " protocol is not supported");
        }
    }

}
"""
example_3_output = """
{
    "Decisions": [
        {"Model": "model_1",
        "FunctionName": "resolve(final HttpHost host)"}]
}
"""

example_4_input = """
public static final BuildInfo BUILD_INFO = new BuildInfo();

// Remote listener
public static final RemoteListenerServerLifecycle REMOTE_LISTENER = new RemoteListenerServerLifecycle();

public static final ImportFormatReader IMPORT_FORMAT_READER = new ImportFormatReader();
public static final TaskExecutor TASK_EXECUTOR = new DefaultTaskExecutor();
"""
example_4_output = """
{ }
"""

example_5_input = """
public static String getVersion() {
    return version;
}
"""
example_5_output = """
{ }
"""

example_6_input = """
public static void openWinConfigFileDialog() {
  JFileChooser chooser = new JFileChooser();
  chooser.setFileFilter(new FileNameExtensionFilter("WIN Config (.config)", "config"));
  chooser.addChoosableFileFilter(new FileNameExtensionFilter("Text File (.txt)", "txt"));
  chooser.setCurrentDirectory(new File(swarmConfig.lastPath));
  chooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
  chooser.setMultiSelectionEnabled(false);
  chooser.setDialogTitle("Select WIN configuration file...");
  if (WinDataFile.configFile != null) {
    chooser.setSelectedFile(WinDataFile.configFile);
  }
  int result = chooser.showOpenDialog(applicationFrame);
  if (result == JFileChooser.APPROVE_OPTION) {
    File f = chooser.getSelectedFile();
    SwarmConfig.getInstance().lastPath = f.getParent();
    WinDataFile.configFile = f;
  }
}
"""
example_6_output = """
{ }
"""


def extract_grouped_decisions_source_code(response: str, source_code: str) -> List[List[str]]:
    """
    Extract LLM identified decisions from source code file.

    Args:
        response (str): LLM response.
        source_code (str): User-provided source code file.

    Returns:
        List[str]: List of individual functions and their code.
    """
    grouped_decisions = []
    passed_model_ids = []
    extracted_decisions = json.loads(response)

    for decision in extracted_decisions:
        model_id = decision['Model']

        if model_id not in passed_model_ids:
            decisions = []
            # Get all names of other decisions that share the same DMN model
            # number as this decision.
            decision_names = [entry['FunctionName'] for entry in extracted_decisions
                              if entry['Model'] == model_id]

            if len(decision_names) > 0:
                # Extract each decision from the source code file, i.e.,
                # extract each function and its body.
                for decision_name in decision_names:
                    start = source_code.find(decision_name)
                    if start == -1:
                        break

                    function_opening = source_code.find('{', start)
                    if function_opening == -1:
                        break

                    bracket_tracker = []
                    current_character = function_opening

                    # Identify what the closing bracket is to the opening bracket.
                    while current_character < len(source_code):
                        if source_code[current_character] == '{':
                            bracket_tracker.append('x')
                        elif source_code[current_character] == '}':
                            bracket_tracker.pop()
                            if len(bracket_tracker) == 0:
                                function_code = source_code[start:current_character + 1].strip()
                                decisions.append(function_code)
                                break
                        current_character += 1
            else:
                return []

            grouped_decisions.append(decisions)
            passed_model_ids.append(model_id)

    return grouped_decisions


def extract_decisions(source_code: str, name: str) -> List[List[str]]:
    """
    Identify relevant decisions in a source code file.

      Args:
        source_code (str): Source code relevant to one DRD.
        name (str): name to be used for file.

      Returns:
        list[list[str]]: List of grouped decisions.
    """
    # Four questions used to prompt the LLM.
    questions = ['We will ask you two questions on Decision Model and Notation. Each question starts with "Q:", and each response should start with "A:" followed by your answer. Only provide an answer to the question which has not been answered yet. Respond using only regular sentences, unless specified otherwise. Are you able to recognize which functions contain Decision Model and Notation elements in source code?',
                 f"""Consider the following examples (6 examples; each contains one or no decision (at a function level), but real examples may contain more):

Input: {example_1_input}
Expected JSON output: {example_1_output}

Input: {example_4_input}
Expected JSON output: {example_4_output}

Input: {example_2_input}
Expected JSON output: {example_2_output}

Input: {example_5_input}
Expected JSON output: {example_5_output}

Input: {example_3_input}
Expected JSON output: {example_3_output}

Input: {example_6_input}
Expected JSON output: {example_6_output}

Given a Java source code file, your task is to identify all functions that include decision logic and group those that belong to the same DMN model. We will do this in two steps.

Analyze the following source code: {source_code}

First, identify which functions contain decisions. If the file contains any such functions, provide a JSON object listing these functions with the `Model` entry containing an empty string ("") for each. We will assign the model number in the next step.
            """,
            """Second, using the same Java source code and the list of functions identified in Step 1, analyze the source code to extract all function call relationships between these functions only.

Consider only those function calls where the called function influences the return value of the calling function (i.e., calls that affect the return statement directly or indirectly).

Output only a JSON array where each element represents a call relationship with the following fields (do not repeat elements, only at them once):
- "caller": the name of the calling function.
- "callee": the name of the called function.
            """,
            """Third, using the list of functions identified in Step 1 and the call relationships extracted in Step 2, group the functions into DMN models.

Assign the same model number to all functions that are connected by any call chain, meaning if one function calls another, directly or indirectly, they belong to the same model.

Functions that do not call or are not called by any other function (i.e., isolated functions) should be assigned their own unique DMN model.

Start model numbering from "model_1", then "model_2", and so on.

Output only the JSON array with updated `Model` fields. Do not write anything else.
            """]

    query = ""
    answers = []

    # Make sure each LLM response is added for context.
    for question in questions:
        query += f"Q: {question} \n\n"
        response = generate(query)
        query += f"{response}\n\n"
        answers.append(response)

    # Save results for later evaluation.
    open(f"dmn_models/gemini_for_logic/case_{name.split('case')[1]}/queries/extract_decisions/{name}_temp_dec_0.6_temp_log_0_temp_req_0_temp_gen_0.txt", "w").write(query)

    # Return the grouped decisions by exracting the corresponding source code.
    return extract_grouped_decisions_source_code(answers[3], source_code)


def generate(question: str) -> str:
    """
    Generate the LLM response based on a given question.

      Args:
          question (str): Question to be asked.

      Returns:
          str: LLM response.
    """
    client = AzureOpenAI(
        api_version="2024-12-01-preview",
        # Here, the Azure Endpoint and API key should be inserted.
        azure_endpoint="",
        api_key=""
    )

    response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": question,
        }],
        # LLM setting configuration.
        max_completion_tokens=30000,
        temperature=0.6,
        model="gpt-4.1"
    )

    return response.choices[0].message.content
