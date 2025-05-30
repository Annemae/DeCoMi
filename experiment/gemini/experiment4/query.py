from google import genai
from google.genai import types

case_1 = ("case1",
"""
{
    "Conditions" : {
        "expression" : {
            "Type" : "boolean"
        }
    },
    "Conclusions" : {
        "checkArgument(boolean expression)" : {
            "Type" : "string"
        }
    },
    "DecisionRules" : [
        {
            "expression" : "!expression",
            "checkArgument(boolean expression)" : "throw new IllegalArgumentException();"
        },
        {
            "expression" : "expression",
            "checkArgument(boolean expression)" : null
        }
    ]
}

{
    "Decisions" : {
        "checkArgument(boolean expression)" : {
            "Input" : ["expression"]
        }
    },
    "InputData" : ["expression"]
}
""")

case_2 = ("case2",
"""
{
    "Conditions" : {
        "s" : {
            "Type" : "boolean"
        },
        "pageParts" : {
            "Type" : "boolean"
        }
    },
    "Conclusions" : {
        "format(String s)" : {
            "Type" : "string"
        }
    },
    "DecisionRules" : [
        {
            "s" : "s == null",
            "pageParts" : "-",
            "format(String s)" : "return \"\";"	
        },
        {
            "s" : "s != null",
            "pageParts" : "pageParts.length == 2",
            "format(String s)" : "return pageParts[1];"	
        },
        {
            "s" : "s != null",
            "pageParts" : "pageParts.length >= 1",
            "format(String s)" : "return pageParts[0];"	
        },
        {
            "s" : "s != null",
            "pageParts" : "-",
            "format(String s)" : "return \"\";"	
        }
    ]
}

{
    "Decisions" : {
        "format(String s)" : {
            "Input" : ["s", "pageParts"]
        }
    },
    "InputData" : ["s", "pageParts"]
}
""")

case_3 = ("case3",
"""
{
    "Conditions" : {
        "neTargets" : {
            "Type" : "boolean"
        },
        "neSources" : {
            "Type" : "boolean"
        }
    },
    "Conclusions" : {
        "uptodate(ResourceCollection src, ResourceCollection target)" : {
            "Type" : "boolean"
        }
    },
    "DecisionRules" : [
        {
            "neTargets" : "neTargets > 0",
            "neSources" : "-",
            "uptodate(ResourceCollection src, ResourceCollection target)" : "return false;"
        },
        {
            "neTargets" : "neTargets <= 0",
            "neSources" : "neSources > 0",
            "uptodate(ResourceCollection src, ResourceCollection target)" : "return false;"
        },
        {
            "neTargets" : "neTargets <= 0",
            "neSources" : "neSources <= 0",
            "uptodate(ResourceCollection src, ResourceCollection target)" : "return oldestTarget.getLastModified() >= newestSource.getLastModified();"
        }
    ]
}

{
    "Decisions" : {
        "uptodate(ResourceCollection src, ResourceCollection target)" : {
            "Input" : ["neTargets", "neSources"]
        }
    },
    "InputData" : ["neTargets", "neSources"]
}
""")

case_4 = ("case4",
"""
{
    "Conditions" : {
        "val" : {
            "Type" : "number"
        }
    },
    "Conclusions" : {
        "toString(Object val)" : {
            "Type" : "string"
        }
    },
    "DecisionRules" : [
        {
            "val" : "val == null",
            "toString(Object val)" : "return "null";"
        },
        {
            "val" : "val == Undefined.instance",
            "toString(Object val)" : "return \"undefined\";"
        },
        {
            "val" : "val instanceof String",
            "toString(Object val)" : "return (String)val;"
        },
        {
            "val" : "val instanceof Number",
            "toString(Object val)" : "return numberToString(((Number)val).doubleValue(), 10);"
        },
        {
            "val" : "val instanceof Scriptable",
            "toString(Object val)" : "throw errorWithClassName(\"msg.primitive.expected\", val);"
        },
        {
            "val" : "-",
            "toString(Object val)" : "return val.toString();"
        }    
    ]
}

{
    "Conditions" : {
        "toString(Object val)" : {
            "Type" : "string"
        },
        "d" : {
            "Type" : "boolean"
        },
        "base" : {
            "Type" : "boolean"
        }
    },
    "Conclusions" : {
        "numberToString(double d, int base)" : {
            "Type" : "string"
        }
    },
    "DecisionRules" : [
        {
            "toString(Object val)" : "return numberToString(((Number)val).doubleValue(), 10);",
            "d" : "d != d",
            "base" : "-",
            "numberToString(double d, int base)" : "return \"NaN\";"
        },
        {
            "toString(Object val)" : "return numberToString(((Number)val).doubleValue(), 10);",
            "d" : "d == Double.POSITIVE_INFINITY",
            "base" : "-",
            "numberToString(double d, int base)" : "return \"Infinity\";"
        },
        {
            "toString(Object val)" : "return numberToString(((Number)val).doubleValue(), 10);",
            "d" : "d == Double.NEGATIVE_INFINITY",
            "base" : "-",
            "numberToString(double d, int base)" : "return \"-Infinity\";"
        },
        {
            "toString(Object val)" : "return numberToString(((Number)val).doubleValue(), 10);",
            "d" : "d == 0.0",
            "base" : "-",
            "numberToString(double d, int base)" : "return \"0\";"
        },
        {
            "toString(Object val)" : "return numberToString(((Number)val).doubleValue(), 10);",
            "d" : "d == d && d != Double.POSITIVE_INFINITY && d != Double.NEGATIVE_INFINITY && d != 0.0",
            "base" : "(base < 2) || (base > 36)",
            "numberToString(double d, int base)" : "throw Context.reportRuntimeError1(\"msg.bad.radix\", Integer.toString(base));"
        },
        {
            "toString(Object val)" : "return numberToString(((Number)val).doubleValue(), 10);",
            "d" : "d == d && d != Double.POSITIVE_INFINITY && d != Double.NEGATIVE_INFINITY && d != 0.0",
            "base" : "base != 10",
            "numberToString(double d, int base)" : "return DToA.JS_dtobasestr(base, d);"
        },
        {
            "toString(Object val)" : "return numberToString(((Number)val).doubleValue(), 10);",
            "d" : "d == d && d != Double.POSITIVE_INFINITY && d != Double.NEGATIVE_INFINITY && d != 0.0",
            "base" : "(base >= 2 && base <= 36) && base == 10",
            "numberToString(double d, int base)" : "return result.toString();"
        } 
    ]
}

{
    "Decisions" : {
        "toString(Object val)" : {
            "Input" : ["val"]
        },
        "numberToString(double d, int base)" : {
            "Input" : ["toString(Object val)", "d", "base"]
        }
    },
    "InputData" : ["val", "d", "base"]
}
""")

case_5 = ("case5",
"""
{
    "Conditions" : {
        "val" : {
            "Type" : "boolean"
        }
    },
    "Conclusions" : {
        "toNumber(Object val)" : {
            "Type" : "string"
        }
    },
    "DecisionRules" : [
        {
            "val" : "val instanceof Number",
            "toNumber(Object val)" : "return ((Number) val).doubleValue();"
        },
        {
            "val" : "val == null",
            "toNumber(Object val)" : "return +0.0;"
        },
        {
            "val" : "val == Undefined.instance",
            "toNumber(Object val)" : "return NaN;"
        },
        {
            "val" : "val instanceof String",
            "toNumber(Object val)" : "return toNumber((String) val);"
        },
        {
            "val" : "val instanceof Boolean",
            "toNumber(Object val)" : "return ((Boolean) val).booleanValue() ? 1 : +0.0;"
        },
        {
            "val" : "val instanceof Scriptable",
            "toNumber(Object val)" : "throw errorWithClassName(\"msg.primitive.expected\", val);"
        },
        {
            "val" : "-",
            "toNumber(Object val)" : "return NaN;"
        }
    ]
}

{
    "Conditions" : {
        "toNumber(Object val)" : {
            "Type" : "string"
        },
        "start, len" : {
            "Type" : "boolean"
        },
        "startChar" : {
            "Type" : "boolean"
        },
        "c1" : {
            "Type" : "boolean"
        },
        "c2" : {
            "Type" : "boolean"
        },
        "endchar" : {
            "Type" : "boolean"
        },
        "start, end, s" : {
            "Type" : "boolean"
        },
        "MSJVM_BUG_WORKAROUND" : {
            "Type" : "boolean"
        },
        "c" : {
            "Type" : "boolean"
        },
        "ex" : {
            "Type" : "boolean"
        }
    },
    "Conclusions" : {
        "toNumber(String s)" : {
            "Type" : "string"
        }
    },
    "DecisionRules" : [
        {
            "toNumber(Object val)": "return toNumber((String) val);",
            "start, len": "start == len",
            "startChar": "-",
            "c1": "-",
            "c2": "-",
            "endchar": "-",
            "start, end, s": "-",
            "?": "-",
            "c": "-",
            "ex": "-",
            "toNumber(String s)": "return +0.0;"
        },
        {
            "toNumber(Object val)": "return toNumber((String) val);",
            "start, len": "start + 2 < len",
            "startChar": "startChar == '0'",
            "c1": "c1 == 'x' || c1 == 'X'",
            "c2": "-",
            "endchar": "-",
            "start, end, s": "-",
            "?": "-",
            "c": "-",
            "ex": "-",
            "toNumber(String s)": "return stringToNumber(s, start + 2, 16);"
        },
        {
            "toNumber(Object val)": "return toNumber((String) val);",
            "start, len": "start + 3 < len && s.charAt(start + 1) == '0'",
            "startChar": "startChar == '+' || startChar == '-'",
            "c1": "-",
            "c2": "c2 == 'x' || c2 == 'X'",
            "endchar": "-",
            "start, end, s": "-",
            "?": "-",
            "c": "-",
            "ex": "-",
            "toNumber(String s)": "return startChar == '-' ? -val : val;"
        },
        {
            "toNumber(Object val)": "return toNumber((String) val);",
            "start, len": "start != len",
            "startChar": "-",
            "c1": "-",
            "c2": "-",
            "endchar": "endChar == 'y'",
            "start, end, s": "start + 7 == end && s.regionMatches(start, \"Infinity\", 0, 8)",
            "?": "-",
            "c": "-",
            "ex": "-",
            "toNumber(String s)": "return startChar == '-' ? Double.NEGATIVE_INFINITY : Double.POSITIVE_INFINITY;"
        },
        {
            "toNumber(Object val)": "return toNumber((String) val);",
            "start, len": "start != len",
            "startChar": "-",
            "c1": "-",
            "c2": "-",
            "endchar": "endChar == 'y'",
            "start, end, s": "start + 7 != end && !(s.regionMatches(start, \"Infinity\", 0, 8))",
            "?": "-",
            "c": "-",
            "ex": "-",
            "toNumber(String s)": "return NaN;"
        },
        {
            "toNumber(Object val)": "return toNumber((String) val);",
            "start, len": "start != len",
            "startChar": "-",
            "c1": "-",
            "c2": "-",
            "endchar": "endChar != 'y'",
            "start, end, s": "-",
            "?": "MSJVM_BUG_WORKAROUNDS",
            "c": "('0' > c && c > '9') && c != '.' && c != 'e' && c != 'E' && c != '+' && c != '-'",
            "ex": "-",
            "toNumber(String s)": "return NaN;"
        },
        {
            "toNumber(Object val)": "return toNumber((String) val);",
            "start, len": "start != len",
            "startChar": "-",
            "c1": "-",
            "c2": "-",
            "endchar": "endChar != 'y'",
            "start, end, s": "-",
            "?": "-",
            "c": "-",
            "ex": "!(NumberFormatException ex)",
            "toNumber(String s)": "return Double.valueOf(sub).doubleValue();"
        },
        {
            "toNumber(Object val)": "return toNumber((String) val);",
            "start, len": "start != len",
            "startChar": "-",
            "c1": "-",
            "c2": "-",
            "endchar": "endChar != 'y'",
            "start, end, s": "-",
            "?": "-",
            "c": "-",
            "ex": "NumberFormatException ex",
            "toNumber(String s)": "return NaN;"
        }
    ]
}

{
    "Conditions" : {
        "toNumber(String s)" : {
            "Type" : "string"
        },
        "start, end" : {
            "Type" : "boolean"
        },
        "sum" : {
            "Type" : "boolean"
        },
        "radix" : {
            "Type" : "boolean"
        },
        "nfe" : {
            "Type" : "boolean"
        }
    },
    "Conclusions" : {
        "stringToNumber(String s, int start, int radix)" : {
            "Type" : "string"
        }
    },
    "DecisionRules" : [
        {
            "toNumber(String s)": "(return startChar == '-' ? -val : val;) || (return stringToNumber(s, start + 2, 16);)",
            "start, end": "start == end",
            "sum": "-",
            "radix": "-",
            "nfe": "-",
            "stringToNumber(String s, int start, int radix)": "return NaN;"
        },
        {
            "toNumber(String s)": "(return startChar == '-' ? -val : val;) || (return stringToNumber(s, start + 2, 16);)",
            "start, end": "start != end",
            "sum": "sum >= 9007199254740992.0",
            "radix": "radix == 10",
            "nfe": "!(NumberFormatException nfe)",
            "stringToNumber(String s, int start, int radix)": "return Double.valueOf(s.substring(start, end)).doubleValue();"
        },
        {
            "toNumber(String s)": "(return startChar == '-' ? -val : val;) || (return stringToNumber(s, start + 2, 16);)",
            "start, end": "start != end",
            "sum": "sum >= 9007199254740992.0",
            "radix": "radix == 10",
            "nfe": "NumberFormatException nfe",
            "stringToNumber(String s, int start, int radix)": "return NaN;"
        },
        {
            "toNumber(String s)": "(return startChar == '-' ? -val : val;) || (return stringToNumber(s, start + 2, 16);)",
            "start, end": "start != end",
            "sum": "-",
            "radix": "-",
            "nfe": "-",
            "stringToNumber(String s, int start, int radix)": "return NaN;"
        }
    ]
}

{
    "Decisions" : {
        "toNumber(Object val)" : {
            "Input" : ["val"]
        },
        "toNumber(String s)" : {
            "Input" : ["toNumber(Object val)", "c", "?", "endchar", "c1", "start, len", "startChar", "c2", "ex", "start, end, s"]
        },
        "stringToNumber(String s, int start, int radix)" : {
            "Input" : ["toNumber(String s)", "start, end", "sum", "radix", "nfe"]
        }
    },
    "InputData" : ["val", "start, end", "sum", "radix", "nfe", "c", "?", "endchar", "c1", "start, len", "startChar", "c2", "ex", "start, end, s"]
}
""")

example_1_input = """
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

def generate(question, temperature):
    client = genai.Client(
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
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        max_output_tokens=50000,
        temperature=temperature
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

temperatures = [0, 0.2, 0.4, 0.6, 0.8, 1]
cases = [case_1, case_2, case_3, case_4, case_5]

# example = ("example",
# """
# {
#     "Decisions" : {
#         "Cool" : {
#             "Input" : ["Niceness"]
#         }
#     },
#     "InputData" : ["Niceness"]
# }

# {
#     "Conditions" : {
#         "Niceness" : {
#             "Type" : "number"
#         }
#     },
#     "Conclusions" : {
#         "Cool" : {
#             "Type" : "boolean"
#         }
#     },
#     "DecisionRules" : [
#         {
#             "Niceness" : "0",
#             "Cool" : "false"
#         },
#         {
#             "Niceness" : "100",
#             "Cool" : "true"
#         }
#     ]
# }
# """)
# temperatures = [0]
# cases = [example]

def run_query(code, case_name, temperature):
    input = ['We will ask you two questions on Decision Model and Notation. Each question starts with "Q:", and each response should start with "A:" followed by your answer. Only provide an answer to the question which has not been answered yet. Respond using only regular sentences, unless specified otherwise. Do you know Decision Model and Notation and can you create a DMN XML?',
        f'Consider the following examples (3 examples): \n\n  \n\n Input: {example_1_input} \n Expected JSON output: {example_1_output} \n Input: {example_2_input} \n Expected JSON output: {example_2_output} \n Input: {example_3_input} \n Expected JSON output: {example_3_output} \nGiven multiple structured JSON objects, you are expected to generate a corresponding DMN XML file based on these JSON objects. Only provide the DMN XML. Do not write anything else. Analyze the following JSON objects: {code}',]
    
    query = ""
        
    for question in input:
        query += f"Q: {question} \n\n"
        response = generate(query, temperature)
        query += f"{response}\n\n"

    open(f"results/{case_name}_temp_{temperature}.txt", "w").write(query)

if __name__ == "__main__":
    for temperature in temperatures:
        for case in cases:
            case_name = case[0]
            code = case[1]

            print(f"Running {case_name} with temperature {temperature}...")

            run_query(code, case_name, temperature)