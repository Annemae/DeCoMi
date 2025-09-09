"""extract_decision_requirement_level.py file.

Extract the decision requirement level, i.e., DRD, from source code.
"""
from google import genai
from google.genai import types

# Examples used for few-shot prompting.
# Contains input source code and expected DRD JSON object.
example_1_input = """
public static <T> @Nullable T getNext(Iterator<? extends T> iterator, @Nullable T defaultValue) {
    return iterator.hasNext() ? iterator.next() : defaultValue;
}
"""
example_1_output = """
{
    "Decisions" : {
        "getNext(Iterator<? extends T> iterator, @Nullable T defaultValue)" : {
            "Input" : ["iterator"]
        }
    },
    "InputData" : ["iterator"]
}
"""

example_2_input = """
protected void checkInterval(long start, long end) {
  if (end < start) {
      throw new IllegalArgumentException("The end instant must be greater than the start instant");
  }
}
"""
example_2_output = """
{
    "Decisions" : {
        "checkInterval(long start, long end)" : {
            "Input" : ["start, end"]
        }
    },
    "InputData" : ["start, end"]
}
"""

example_3_input = """
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
"""
example_3_output = """
{
    "Decisions" : {
        "resolve(final HttpHost host)" : {
            "Input" : ["port", "name"]
        }
    },
    "InputData" : ["port", "name"]
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
"""

example_5_input = """
public static String getVersion() {
    return version;
}
"""
example_5_output = """
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
"""

# Question 2 of the prompt.
question_2 = f"""
Consider the following examples (6 examples; some contain decisions (i.e., at a function level) that can be modeled, and some do not):

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

Could you generate a DRD in JSON format for the following Java source code?

Please follow these rules when extracting the DRD:

1) Some of the provided decisions (i.e., functions) may serve as inputs to other decisions. Add these as entries to the `Input` field of the JSON representation for dependent decisions.
2) Use variable names exactly as they appear in the source code. Do not rename, alter, or invent variable names.
3) For the input data of each decision, include only the variables (i.e., function parameters and/or local variables) that are part of a decision expression (e.g., an `if` statement) within that function that directly influence an outcome (i.e., a return value).
4) If multiple variables contribute to the same decision expression, they can be grouped together as a single input in the JSON representation.

If a DRD is present in the code, provide a complete and valid structured JSON object representing the decisions, their inputs (either input data and/or other decisions), and the input data.
If no DRD can be constructed, return an empty JSON object.
Do not interpret the decisions, i.e., extract them exactly as defined in the source code.
Do not write anything else.

Analyze the following source code:
"""


def extract_decision_requirement_level(source_code: str, name: str) -> str:
    """
    Extract DRD.

    Args:
        source_code (str): Source code relevant to one DRD.
        name (str): name to be used for file.

    Returns:
        str: JSON object in string format.
    """
    # Two questions used to prompt the LLM.
    questions = ['We will ask you two questions on Decision Model and Notation. Each question starts with "Q:", and each response should start with "A:" followed by your answer. Only provide an answer to the question which has not been answered yet. Respond using only regular sentences, unless specified otherwise. Do you know Decision Model and Notation and can you create a DRD?',
                 question_2 + source_code]

    query = ""
    answers = []

    # Make sure each LLM response is added for context.
    for question in questions:
        query += f"Q: {question} \n\n"
        # Boolean whether JSON is expected from the LLM.
        if question.startswith("We will ask you two questions on Decision Model and Notation"):
            response = generate(query, False)
            answers.append(response)
        else:
            response = generate(query, True)
            answers.append(response)
        query += f"{response}\n\n"

    # Save results for later evaluation.
    open(f"../prototype_results/gemini_for_logic/case_{name.split('case')[1]}/queries/extract_requirements/{name}_temp_dec_0.6_temp_log_0_temp_req_0_temp_gen_0.txt", "w").write(query)

    # Return the answer that contains the extracted DRD.
    return answers[1]


def generate(question: str, json_output: bool) -> str:
    """
    Generate the LLM response based on a given question.

      Args:
          question (str): Question to be asked.
          json_output (bool): Whether the LLM should output JSON.

      Returns:
          str: LLM response.
    """
    client = genai.Client(
        # Here, the API key should be inserted.
        api_key=""
    )

    model = "gemini-2.5-pro-preview-05-06"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=question),
            ],
        ),
    ]
    # LLM setting configuration.
    if json_output:
        generate_content_config = types.GenerateContentConfig(
            response_mime_type="application/json",
            max_output_tokens=50000,
            temperature=0,
        )
    else:
        generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
            max_output_tokens=50000,
            temperature=0,
        )

    response = ""

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if chunk.text:
            response += chunk.text

    return response.strip()
