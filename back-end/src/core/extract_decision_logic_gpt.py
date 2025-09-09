from openai import AzureOpenAI

def generate(question, temperature):
    client = AzureOpenAI(
        api_version="2024-12-01-preview",
        azure_endpoint="",
        api_key=""
    )

    response = client.chat.completions.create(
        messages= [{
            "role": "user",
            "content": question,
        }],
        max_completion_tokens=30000,
        temperature=temperature,
        model="gpt-4.1",
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.6
    )

    return response.choices[0].message.content

example_1_input = """
public static <T> @Nullable T getNext(Iterator<? extends T> iterator, @Nullable T defaultValue) {
    return iterator.hasNext() ? iterator.next() : defaultValue;
}
"""
example_1_output = """
{
    "Conditions" : {
        "iterator" : {
            "Type" : "boolean"
        }
    },
    "Conclusions" : {
        "getNext(Iterator<? extends T> iterator, @Nullable T defaultValue)" : {
            "Type" : "string"
        }
    },
    "DecisionRules" : [
        {
            "iterator" : "iterator.hasNext()",
            "getNext(Iterator<? extends T> iterator, @Nullable T defaultValue)" : "iterator.next()"
        },
        {
            "iterator" : "!(iterator.hasNext())",
            "getNext(Iterator<? extends T> iterator, @Nullable T defaultValue)" : "defaultValue"
        }
    ]
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
    "Conditions" : {
        "start, end" : {
            "Type" : "boolean"
        }
    },
    "Conclusions" : {
        "checkInterval(long start, long end)" : {
            "Type" : "string"
        }
    },
    "DecisionRules" : [
        {
            "start, end" : "end < start",
            "checkInterval(long start, long end)" : "throw new IllegalArgumentException(\"The end instant must be greater than the start instant\");"
        },
        {
            "start, end" : "end >= start",
            "checkInterval(long start, long end)" : null
        }
    ]
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
    "Conditions" : {
        "port" : {
            "Type" : "boolean"
        },
        "name" : {
            "Type" : "string"
        }
    },
    "Conclusions" : {
        "resolve(final HttpHost host)" : {
            "Type" : "string"
        }
    },
    "DecisionRules" : [
        {
            "port" : "port > 0",
            "name" : "-",
            "resolve(final HttpHost host)" : "return port;"
        },
        {
            "port" : "port <= 0",
            "name" : "name.equalsIgnoreCase(\"http\")",
            "resolve(final HttpHost host)" : "return 80;"
        },
        {
            "port" : "port <= 0",
            "name" : "name.equalsIgnoreCase(\"https\")",
            "resolve(final HttpHost host)" : "return 443;"
        },
        {
            "port" : "port <= 0",
            "name" : "!(name.equalsIgnoreCase(\"http\")) && !(name.equalsIgnoreCase(\"https\"))",
            "resolve(final HttpHost host)" : "throw new UnsupportedSchemeException(name + \" protocol is not supported\");"
        }
    ]
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

def extract_decision_logic_level_gpt(file, temperature, name, name_normal):
    queries = [f'We will ask you a series of questions on Decision Model and Notation tables. Each question starts with "Q:", and each response should start with "A:" followed by your answer. Only provide an answer to the question which has not been answered yet. Respond using only regular sentences, unless specified otherwise. Below is a part of Java source code, between quotation marks. What does this code decide? \n\n\"\"\"{file}\"\"\"',
        "What does the function return?",
        'What are the variables that influence this decision?',
        'For each input and output, give me an overview of their data type and their possible values.',
        'What are the relevant values of the numerical variables?', 
        query_6,
        'Is this table complete? (I.e., is there an applicable rule for each set of inputs?) If it is incomplete, can you find an example for which no rule would be applicable?',
        f'According to your table, answer the following question. What are the input to the decision?']
    
    query = ""
    answers = []
        
    for question in queries:
        query += f"Q: {question} \n\n"
        if question.startswith('Could you generate a DMN decision table'):
            response = generate(question, temperature)
            answers.append(response)
        else:
            response = generate(query, temperature)
            answers.append(response)
        query += f"{response}\n\n"

    query = query.replace("\u2264", "<=")  
    query = query.replace("\u2265", ">=")
    query = query.replace("\u2192", "->")
    query = query.replace("\u2190", "<-")

    open(f"dmn_models/gpt_for_logic/case_{name_normal.split('case')[1]}/queries/extract_logic/{name}_temp_dec_0.6_temp_log_{temperature}_temp_req_0_temp_gen_0.txt", "w").write(query)

    return answers[5]


query_6 = f"""
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

Could you generate a DMN decision table in JSON format for the part of Java source code provided in the first question that starts with "Q"?

Please follow these rules when extracting the decision table:

1) For the conditions of each decision, include only the variables (i.e., function parameters and/or local variables) that are directly part of a decision expression (e.g., an `if` statement) within that function that directly influences a decision (e.g., an exit statement).
2) Only extract the specific line of code on which the decision is made (e.g., an exit statement). Do not include the entire function body surrounding it.
3) Do not include both a variable and its opposite (e.g., not x && !x, or x > 0 && x <= 0) as separate values within the same decision rule condition. One is sufficient, as the opposite case should be covered by a separate rule. This rule does not apply when the condition involves different variables.
4) If multiple variables together form a single decision expression that directly influences a decision (e.g., an exit statement), they should be grouped as one condition in the JSON representation.
5) Use only the base variable names for conditions, conclusions, and decision rules, exactly as they appear in the source code. Do not rename, alter, invent, or include field/property accesses (e.g., user.name) with variable names. Even if a property is accessed in the code, include only the top-level variable (e.g., use user, not user.name).
6) Extract the conditions, conclusions, and decision rules exactly as they are defined in the source code. Do not interpret, transform, or modify them. For example, if a variable is used as a boolean expression (e.g., number == 2), do not treat it as a numeric value (2).

If a decision table is present in the code, provide a complete and valid structured JSON object with conditions, conclusions, and decision rules for this part of Java source code.  
If no decision table can be constructed, return an empty JSON object.  
Do not write anything else.

Create a decision table for the part of Java source code provided in the first question that starts with "Q".
"""