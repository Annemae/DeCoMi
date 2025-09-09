"""create_dmn_xml.py file.

Create complete DMN model based on extracted DMN elements.
"""
from google import genai
from google.genai import types


# Examples used for few-shot prompting.
# Contains input JSON objects and expected DMN XML based on these objects.
example_1_input = """
Decision Logic Level:
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

Decision Requirement Level:
{
    "Decisions" : {
        "getNext(Iterator<? extends T> iterator, @Nullable T defaultValue)" : {
            "Input" : ["iterator"]
        }
    },
    "InputData" : ["iterator"]
}
"""
example_1_output = """
<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="https://www.omg.org/spec/DMN/20191111/MODEL/" xmlns:dmndi="https://www.omg.org/spec/DMN/20191111/DMNDI/" xmlns:dc="http://www.omg.org/spec/DMN/20180521/DC/" xmlns:di="http://www.omg.org/spec/DMN/20180521/DI/" id="definitions_08em653" name="definitions" namespace="http://camunda.org/schema/1.0/dmn" exporter="dmn-js (https://demo.bpmn.io/dmn)" exporterVersion="17.2.0">
  <inputData id="InputData_05mgc6n" name="iterator" />
  <decision id="Decision_1pocaxa" name="getNext(Iterator&#60;? extends T&#62; iterator, @Nullable T defaultValue)">
    <informationRequirement id="InformationRequirement_1g2xc78">
      <requiredInput href="#InputData_05mgc6n" />
    </informationRequirement>
    <decisionTable id="DecisionTable_0izbi3j">
      <input id="InputClause_1s1rlxb" label="iterator">
        <inputExpression id="LiteralExpression_0mwc8gu" typeRef="boolean" />
      </input>
      <output id="OutputClause_0h2gn4j" label="getNext(Iterator&#60;? extends T&#62; iterator, @Nullable T defaultValue)" typeRef="string" />
      <rule id="DecisionRule_1b22qw5">
        <inputEntry id="UnaryTests_1128jj0">
          <text>iterator.hasNext()</text>
        </inputEntry>
        <outputEntry id="LiteralExpression_14bqw98">
          <text>iterator.next()</text>
        </outputEntry>
      </rule>
      <rule id="DecisionRule_0rzdr3u">
        <inputEntry id="UnaryTests_1qgxg8r">
          <text>!(iterator.hasNext())</text>
        </inputEntry>
        <outputEntry id="LiteralExpression_1c0zqqe">
          <text>defaultValue</text>
        </outputEntry>
      </rule>
    </decisionTable>
  </decision>
  <dmndi:DMNDI>
    <dmndi:DMNDiagram id="DMNDiagram_088hwua">
      <dmndi:DMNShape id="DMNShape_0vq1aiw" dmnElementRef="InputData_05mgc6n">
        <dc:Bounds height="45" width="125" x="177" y="258" />
      </dmndi:DMNShape>
      <dmndi:DMNEdge id="DMNEdge_06c9zcq" dmnElementRef="InformationRequirement_1g2xc78">
        <di:waypoint x="240" y="258" />
        <di:waypoint x="240" y="220" />
        <di:waypoint x="240" y="200" />
      </dmndi:DMNEdge>
      <dmndi:DMNShape id="DMNShape_11s6k8p" dmnElementRef="Decision_1pocaxa">
        <dc:Bounds height="80" width="180" x="150" y="120" />
      </dmndi:DMNShape>
    </dmndi:DMNDiagram>
  </dmndi:DMNDI>
</definitions>
"""

example_2_input = """
Decision Logic Level:
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

Decision Requirement Level:
{
    "Decisions" : {
        "checkInterval(long start, long end)" : {
            "Input" : ["start, end"]
        }
    },
    "InputData" : ["start, end"]
}
"""
example_2_output = """
<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="https://www.omg.org/spec/DMN/20191111/MODEL/" xmlns:dmndi="https://www.omg.org/spec/DMN/20191111/DMNDI/" xmlns:dc="http://www.omg.org/spec/DMN/20180521/DC/" xmlns:di="http://www.omg.org/spec/DMN/20180521/DI/" id="definitions_00gpcft" name="definitions" namespace="http://camunda.org/schema/1.0/dmn" exporter="dmn-js (https://demo.bpmn.io/dmn)" exporterVersion="17.2.0">
  <decision id="decision_0iygfo0" name="checkInterval(long start, long end)">
    <informationRequirement id="InformationRequirement_0hhzr6i">
      <requiredInput href="#InputData_0enwjwx" />
    </informationRequirement>
    <decisionTable id="decisionTable_0n05uj7">
      <input id="input1" label="start, end">
        <inputExpression id="inputExpression1" typeRef="boolean">
          <text></text>
        </inputExpression>
      </input>
      <output id="output1" label="checkInterval(long start, long end)" name="" typeRef="string" />
      <rule id="DecisionRule_00anz39">
        <inputEntry id="UnaryTests_1iqx1ms">
          <text>end &lt; start</text>
        </inputEntry>
        <outputEntry id="LiteralExpression_0ji4wn3">
          <text>throw new IllegalArgumentException("The end instant must be greater than the start instant");</text>
        </outputEntry>
      </rule>
      <rule id="DecisionRule_0zq27lu">
        <inputEntry id="UnaryTests_09is226">
          <text>end &gt;= start</text>
        </inputEntry>
        <outputEntry id="LiteralExpression_0559wuy">
          <text>null</text>
        </outputEntry>
      </rule>
    </decisionTable>
  </decision>
  <inputData id="InputData_0enwjwx" name="start, end" />
  <dmndi:DMNDI>
    <dmndi:DMNDiagram id="DMNDiagram_0e8pnjw">
      <dmndi:DMNShape id="DMNShape_0ytr1p2" dmnElementRef="decision_0iygfo0">
        <dc:Bounds height="80" width="180" x="160" y="110" />
      </dmndi:DMNShape>
      <dmndi:DMNShape id="DMNShape_0nqt3kg" dmnElementRef="InputData_0enwjwx">
        <dc:Bounds height="45" width="125" x="187" y="237" />
      </dmndi:DMNShape>
      <dmndi:DMNEdge id="DMNEdge_1srdu7x" dmnElementRef="InformationRequirement_0hhzr6i">
        <di:waypoint x="250" y="237" />
        <di:waypoint x="250" y="210" />
        <di:waypoint x="250" y="190" />
      </dmndi:DMNEdge>
    </dmndi:DMNDiagram>
  </dmndi:DMNDI>
</definitions>
"""

example_3_input = """
Decision Logic Level:
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

Decision Requirement Level:
{
    "Decisions" : {
        "resolve(final HttpHost host)" : {
            "Input" : ["port", "name"]
        }
    },
    "InputData" : ["port", "name"]
}
"""
example_3_output = """
<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="https://www.omg.org/spec/DMN/20191111/MODEL/" xmlns:dmndi="https://www.omg.org/spec/DMN/20191111/DMNDI/" xmlns:dc="http://www.omg.org/spec/DMN/20180521/DC/" xmlns:di="http://www.omg.org/spec/DMN/20180521/DI/" id="definitions_1khyx15" name="definitions" namespace="http://camunda.org/schema/1.0/dmn" exporter="dmn-js (https://demo.bpmn.io/dmn)" exporterVersion="17.2.0">
  <decision id="decision_08mi2kh" name="resolve(final HttpHost host)">
    <informationRequirement id="InformationRequirement_11zq33g">
      <requiredInput href="#InputData_1yd1o35" />
    </informationRequirement>
    <informationRequirement id="InformationRequirement_10edaps">
      <requiredInput href="#InputData_1gapmsp" />
    </informationRequirement>
    <decisionTable id="decisionTable_0fn2rr7">
      <input id="InputClause_1m3q0rl" label="port">
        <inputExpression id="LiteralExpression_1mibefk" typeRef="boolean">
          <text></text>
        </inputExpression>
      </input>
      <input id="input1" label="name">
        <inputExpression id="inputExpression1" typeRef="string">
          <text></text>
        </inputExpression>
      </input>
      <output id="output1" label="resolve(final HttpHost host)" name="" typeRef="string" />
      <rule id="DecisionRule_152edol">
        <inputEntry id="UnaryTests_1n1yrsc">
          <text>port &gt; 0</text>
        </inputEntry>
        <inputEntry id="UnaryTests_0k0wvh4">
          <text>-</text>
        </inputEntry>
        <outputEntry id="LiteralExpression_1rssu1i">
          <text>return port;</text>
        </outputEntry>
      </rule>
      <rule id="DecisionRule_1kluoj5">
        <inputEntry id="UnaryTests_11n73o7">
          <text>port &lt;= 0</text>
        </inputEntry>
        <inputEntry id="UnaryTests_0mtb96b">
          <text>name.equalsIgnoreCase("http")</text>
        </inputEntry>
        <outputEntry id="LiteralExpression_10proya">
          <text>return 80;</text>
        </outputEntry>
      </rule>
      <rule id="DecisionRule_01m4cqv">
        <inputEntry id="UnaryTests_0yqqqf1">
          <text>port &lt;= 0</text>
        </inputEntry>
        <inputEntry id="UnaryTests_0dleyfy">
          <text>name.equalsIgnoreCase("https")</text>
        </inputEntry>
        <outputEntry id="LiteralExpression_09hc5el">
          <text>return 443;</text>
        </outputEntry>
      </rule>
      <rule id="DecisionRule_0zxf3ra">
        <inputEntry id="UnaryTests_0n5agrw">
          <text>port &lt;= 0</text>
        </inputEntry>
        <inputEntry id="UnaryTests_1j6q8qw">
          <text>!(name.equalsIgnoreCase("http")) &amp;&amp; !(name.equalsIgnoreCase("https"))</text>
        </inputEntry>
        <outputEntry id="LiteralExpression_0nhkia1">
          <text>throw new UnsupportedSchemeException(name + " protocol is not supported");</text>
        </outputEntry>
      </rule>
    </decisionTable>
  </decision>
  <inputData id="InputData_1yd1o35" name="port" />
  <inputData id="InputData_1gapmsp" name="name" />
  <dmndi:DMNDI>
    <dmndi:DMNDiagram id="DMNDiagram_0l8iwsm">
      <dmndi:DMNShape id="DMNShape_1djzll4" dmnElementRef="decision_08mi2kh">
        <dc:Bounds height="80" width="180" x="220" y="80" />
      </dmndi:DMNShape>
      <dmndi:DMNShape id="DMNShape_1mjduok" dmnElementRef="InputData_1yd1o35">
        <dc:Bounds height="45" width="125" x="157" y="218" />
      </dmndi:DMNShape>
      <dmndi:DMNEdge id="DMNEdge_0pi63kv" dmnElementRef="InformationRequirement_11zq33g">
        <di:waypoint x="220" y="218" />
        <di:waypoint x="280" y="180" />
        <di:waypoint x="280" y="160" />
      </dmndi:DMNEdge>
      <dmndi:DMNShape id="DMNShape_0q08g0q" dmnElementRef="InputData_1gapmsp">
        <dc:Bounds height="45" width="125" x="338" y="219" />
      </dmndi:DMNShape>
      <dmndi:DMNEdge id="DMNEdge_1yb2q7y" dmnElementRef="InformationRequirement_10edaps">
        <di:waypoint x="401" y="219" />
        <di:waypoint x="340" y="180" />
        <di:waypoint x="340" y="160" />
      </dmndi:DMNEdge>
    </dmndi:DMNDiagram>
  </dmndi:DMNDI>
</definitions>
"""


def create_dmn_xml(json_objects: str, name: str) -> str:
    """
    Create DMN XML file.

      Args:
          json_objects (str): Extracted DMN elements.
          name (str): name to be used for file.

      Returns:
          str: DMN XML that contains a complete DMN XML.
    """
    # Two questions used to prompt the LLM.
    questions = ['We will ask you two questions on Decision Model and Notation. Each question starts with "Q:", and each response should start with "A:" followed by your answer. Only provide an answer to the question which has not been answered yet. Respond using only regular sentences, unless specified otherwise. Do you know Decision Model and Notation and can you create a DMN XML?',
                 f'Consider the following examples (3 examples): \n\n  \n\n Input: {example_1_input} \n Expected JSON output: {example_1_output} \n Input: {example_2_input} \n Expected JSON output: {example_2_output} \n Input: {example_3_input} \n Expected JSON output: {example_3_output} \nGiven multiple structured JSON objects, you are expected to generate a corresponding DMN XML file based on these JSON objects. Only provide the DMN XML. Do not write anything else. Analyze the following JSON objects: {json_objects}',]

    query = ""
    answers = []

    # Make sure each LLM response is added for context.
    for question in questions:
        query += f"Q: {question} \n\n"
        response = generate(query)
        query += f"{response}\n\n"
        answers.append(response)

    # Save results for later evaluation.
    open(f"../prototype_results/gemini_for_logic/case_{name.split('case')[1]}/queries/create_dmn/{name}_temp_dec_0.6_temp_log_0_temp_req_0_temp_gen_0.txt", "w").write(query)

    # Return the answer that contains DMN XML.
    return answers[1]


def generate(question: str) -> str:
    """
    Generate the LLM response based on a given question.

      Args:
          question (str): Question to be asked.

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
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        max_output_tokens=50000,
        temperature=0
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
