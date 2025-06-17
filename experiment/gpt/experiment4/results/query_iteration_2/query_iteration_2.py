from openai import AzureOpenAI

case_1 = ("case1",
"""
DMN JSON OBJECTS:

Decision Logic Level:
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

Decision Requirement Level:
{
    "Decisions" : {
        "checkArgument(boolean expression)" : {
            "Input" : ["expression"]
        }
    },
    "InputData" : ["expression"]
}


CORRESPONDING CODE:

public static void checkArgument(boolean expression) {
  if (!expression) {
    throw new IllegalArgumentException();
  }
}
""")

case_2 = ("case2",
"""
DMN JSON OBJECTS:

Decision Logic Level:
{
    "Conditions" : {
        "s" : {
            "Type" : "boolean"
        },
        "pageParts.length" : {
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
            "pageParts.length" : "-",
            "format(String s)" : "return \"\";"	
        },
        {
            "s" : "s != null",
            "pageParts.length" : "pageParts.length == 2",
            "format(String s)" : "return pageParts[1];"	
        },
        {
            "s" : "s != null",
            "pageParts.length" : "pageParts.length >= 1",
            "format(String s)" : "return pageParts[0];"	
        },
        {
            "s" : "s != null",
            "pageParts.length" : "-",
            "format(String s)" : "return \"\";"	
        }
    ]
}

Decision Requirement Level:
{
    "Decisions" : {
        "format(String s)" : {
            "Input" : ["s", "pageParts"]
        }
    },
    "InputData" : ["s", "pageParts"]
}


CORRESPONDING CODE:

public String format(String s) {
    if (s == null) {
        return "";
    }
    String[] pageParts = s.split("[\\-]+");
    if (pageParts.length == 2) {
        return pageParts[1];
    } else if (pageParts.length >= 1) {
        return pageParts[0];
    } else {
        return "";
    }

}
""")

case_3 = ("case3",
"""
DMN JSON OBJECTS:

Decision Logic Level:
{
    "Conditions" : {
        "targetsNonExistent" : {
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
            "targetsNonExistent" : "neTargets > 0",
            "neSources" : "-",
            "uptodate(ResourceCollection src, ResourceCollection target)" : "return false;"
        },
        {
            "targetsNonExistent" : "neTargets <= 0",
            "neSources" : "neSources > 0",
            "uptodate(ResourceCollection src, ResourceCollection target)" : "return false;"
        },
        {
            "targetsNonExistent" : "neTargets <= 0",
            "neSources" : "neSources <= 0",
            "uptodate(ResourceCollection src, ResourceCollection target)" : "return oldestTarget.getLastModified() >= newestSource.getLastModified();"
        }
    ]
}

Decision Requirement Level:
{
    "Decisions" : {
        "uptodate(ResourceCollection src, ResourceCollection target)" : {
            "Input" : ["neTargets", "neSources", "oldestTarget, newestSource"]
        }
    },
    "InputData" : ["neTargets", "neSources", "oldestTarget, newestSource"]
}


CORRESPONDING CODE:

private boolean uptodate(ResourceCollection src, ResourceCollection target) {
    org.apache.tools.ant.types.resources.selectors.Date datesel
        = new org.apache.tools.ant.types.resources.selectors.Date();
    datesel.setMillis(System.currentTimeMillis());
    datesel.setWhen(TimeComparison.AFTER);
    // don't whine because a file has changed during the last
    // second (or whatever our current granularity may be)
    datesel.setGranularity(0);
    logFuture(targets, datesel);

    NonExistent missingTargets = new NonExistent(targets);
    int neTargets = missingTargets.size();
    if (neTargets > 0) {
        log(neTargets + " nonexistent targets", Project.MSG_VERBOSE);
        logMissing(missingTargets, "target");
        return false;
    }
    Resource oldestTarget = getOldest(targets);
    logWithModificationTime(oldestTarget, "oldest target file");

    logFuture(sources, datesel);

    NonExistent missingSources = new NonExistent(sources);
    int neSources = missingSources.size();
    if (neSources > 0) {
        log(neSources + " nonexistent sources", Project.MSG_VERBOSE);
        logMissing(missingSources, "source");
        return false;
    }
    Resource newestSource = getNewest(sources);
    logWithModificationTime(newestSource, "newest source");
    return oldestTarget.getLastModified() >= newestSource.getLastModified();
}
""")

case_4 = ("case4",
"""
DMN JSON OBJECTS:

Decision Logic Level:
{
    "Conditions": {
        "isValNull": {
            "Type": "boolean"
        },
        "isValUndefined": {
            "Type": "boolean"
        },
        "isValString": {
            "Type": "boolean"
        },
        "isValNumber": {
            "Type": "boolean"
        },
        "isValInitiallyScriptable": {
            "Type": "boolean"
        },
        "isValAfterDefaultScriptable": {
            "Type": "boolean"
        }
    },
    "Conclusions": {
        "toString(Object val)": {
            "Type": "string"
        }
    },
    "DecisionRules": [
        {
            "isValNull": "val == null",
            "isValUndefined": "-",
            "isValString": "-",
            "isValNumber": "-",
            "isValInitiallyScriptable": "-",
            "isValAfterDefaultScriptable": "-",
            "toString(Object val)": "return \"null\";"
        },
        {
            "isValNull": "!(val == null)",
            "isValUndefined": "val == Undefined.instance",
            "isValString": "-",
            "isValNumber": "-",
            "isValInitiallyScriptable": "-",
            "isValAfterDefaultScriptable": "-",
            "toString(Object val)": "return \"undefined\";"
        },
        {
            "isValNull": "!(val == null)",
            "isValUndefined": "!(val == Undefined.instance)",
            "isValString": "val instanceof String",
            "isValNumber": "-",
            "isValInitiallyScriptable": "-",
            "isValAfterDefaultScriptable": "-",
            "toString(Object val)": "return (String)val;"
        },
        {
            "isValNull": "!(val == null)",
            "isValUndefined": "!(val == Undefined.instance)",
            "isValString": "!(val instanceof String)",
            "isValNumber": "val instanceof Number",
            "isValInitiallyScriptable": "-",
            "isValAfterDefaultScriptable": "-",
            "toString(Object val)": "return numberToString(((Number)val).doubleValue(), 10);"
        },
        {
            "isValNull": "!(val == null)",
            "isValUndefined": "!(val == Undefined.instance)",
            "isValString": "!(val instanceof String)",
            "isValNumber": "!(val instanceof Number)",
            "isValInitiallyScriptable": "val instanceof Scriptable",
            "isValAfterDefaultScriptable": "val instanceof Scriptable",
            "toString(Object val)": "throw errorWithClassName(\"msg.primitive.expected\", val);"
        },
        {
            "isValNull": "!(val == null)",
            "isValUndefined": "!(val == Undefined.instance)",
            "isValString": "!(val instanceof String)",
            "isValNumber": "!(val instanceof Number)",
            "isValInitiallyScriptable": "!(val instanceof Scriptable)",
            "isValAfterDefaultScriptable": "-",
            "toString(Object val)": "return val.toString();"
        }
    ]
}

{
    "Conditions" : {
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
            "d" : "d != d",
            "base" : "-",
            "numberToString(double d, int base)" : "return \"NaN\";"
        },
        {
            "d" : "d == Double.POSITIVE_INFINITY",
            "base" : "-",
            "numberToString(double d, int base)" : "return \"Infinity\";"
        },
        {
            "d" : "d == Double.NEGATIVE_INFINITY",
            "base" : "-",
            "numberToString(double d, int base)" : "return \"-Infinity\";"
        },
        {
            "d" : "d == 0.0",
            "base" : "-",
            "numberToString(double d, int base)" : "return \"0\";"
        },
        {
            "d" : "d == d && d != Double.POSITIVE_INFINITY && d != Double.NEGATIVE_INFINITY && d != 0.0",
            "base" : "(base < 2) || (base > 36)",
            "numberToString(double d, int base)" : "throw Context.reportRuntimeError1(\"msg.bad.radix\", Integer.toString(base));"
        },
        {
            "d" : "d == d && d != Double.POSITIVE_INFINITY && d != Double.NEGATIVE_INFINITY && d != 0.0",
            "base" : "base != 10",
            "numberToString(double d, int base)" : "return DToA.JS_dtobasestr(base, d);"
        },
        {
            "d" : "d == d && d != Double.POSITIVE_INFINITY && d != Double.NEGATIVE_INFINITY && d != 0.0",
            "base" : "(base >= 2 && base <= 36) && base == 10",
            "numberToString(double d, int base)" : "return result.toString();"
        } 
    ]
}

Decision Requirement Level:
{
    "Decisions" : {
        "toString(Object val)" : {
            "Input" : ["val", "numberToString(double d, int base)"]
        },
        "numberToString(double d, int base)" : {
            "Input" : ["d", "base"]
        }
    },
    "InputData" : ["val", "d", "base"]
}


CORRESPONDING CODE:

public static String toString(Object val) {
    for (;;) {
        if (val == null) {
            return "null";
        }
        if (val == Undefined.instance) {
            return "undefined";
        }
        if (val instanceof String) {
            return (String)val;
        }
        if (val instanceof Number) {
            // XXX should we just teach NativeNumber.stringValue()
            // about Numbers?
            return numberToString(((Number)val).doubleValue(), 10);
        }
        if (val instanceof Scriptable) {
            val = ((Scriptable) val).getDefaultValue(StringClass);
            if (val instanceof Scriptable) {
                throw errorWithClassName("msg.primitive.expected", val);
            }
            continue;
        }
        return val.toString();
    }
}

public static String numberToString(double d, int base) {
    if (d != d)
        return "NaN";
    if (d == Double.POSITIVE_INFINITY)
        return "Infinity";
    if (d == Double.NEGATIVE_INFINITY)
        return "-Infinity";
    if (d == 0.0)
        return "0";

    if ((base < 2) || (base > 36)) {
        throw Context.reportRuntimeError1(
            "msg.bad.radix", Integer.toString(base));
    }

    if (base != 10) {
        return DToA.JS_dtobasestr(base, d);
    } else {
        StringBuffer result = new StringBuffer();
        DToA.JS_dtostr(result, DToA.DTOSTR_STANDARD, 0, d);
        return result.toString();
    }

}
""")

case_5 = ("case5",
"""
DMN JSON OBJECTS:

Decision Logic Level:
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
            "start, len": "start == len",
            "startChar": "-",
            "c1": "-",
            "c2": "-",
            "endchar": "-",
            "start, end, s": "-",
            "MSJVM_BUG_WORKAROUND": "-",
            "c": "-",
            "ex": "-",
            "toNumber(String s)": "return +0.0;"
        },
        {
            "start, len": "start + 2 < len",
            "startChar": "startChar == '0'",
            "c1": "c1 == 'x' || c1 == 'X'",
            "c2": "-",
            "endchar": "-",
            "start, end, s": "-",
            "MSJVM_BUG_WORKAROUND": "-",
            "c": "-",
            "ex": "-",
            "toNumber(String s)": "return stringToNumber(s, start + 2, 16);"
        },
        {
            "start, len": "start + 3 < len && s.charAt(start + 1) == '0'",
            "startChar": "startChar == '+' || startChar == '-'",
            "c1": "-",
            "c2": "c2 == 'x' || c2 == 'X'",
            "endchar": "-",
            "start, end, s": "-",
            "MSJVM_BUG_WORKAROUND": "-",
            "c": "-",
            "ex": "-",
            "toNumber(String s)": "return startChar == '-' ? -val : val;"
        },
        {
            "start, len": "start != len",
            "startChar": "-",
            "c1": "-",
            "c2": "-",
            "endchar": "endChar == 'y'",
            "start, end, s": "start + 7 == end && s.regionMatches(start, \"Infinity\", 0, 8)",
            "MSJVM_BUG_WORKAROUND": "-",
            "c": "-",
            "ex": "-",
            "toNumber(String s)": "return startChar == '-' ? Double.NEGATIVE_INFINITY : Double.POSITIVE_INFINITY;"
        },
        {
            "start, len": "start != len",
            "startChar": "-",
            "c1": "-",
            "c2": "-",
            "endchar": "endChar == 'y'",
            "start, end, s": "start + 7 != end && !(s.regionMatches(start, \"Infinity\", 0, 8))",
            "MSJVM_BUG_WORKAROUND": "-",
            "c": "-",
            "ex": "-",
            "toNumber(String s)": "return NaN;"
        },
        {
            "start, len": "start != len",
            "startChar": "-",
            "c1": "-",
            "c2": "-",
            "endchar": "endChar != 'y'",
            "start, end, s": "-",
            "MSJVM_BUG_WORKAROUND": "MSJVM_BUG_WORKAROUNDS",
            "c": "('0' > c && c > '9') && c != '.' && c != 'e' && c != 'E' && c != '+' && c != '-'",
            "ex": "-",
            "toNumber(String s)": "return NaN;"
        },
        {
            "start, len": "start != len",
            "startChar": "-",
            "c1": "-",
            "c2": "-",
            "endchar": "endChar != 'y'",
            "start, end, s": "-",
            "MSJVM_BUG_WORKAROUND": "-",
            "c": "-",
            "ex": "!(NumberFormatException ex)",
            "toNumber(String s)": "return Double.valueOf(sub).doubleValue();"
        },
        {
            "start, len": "start != len",
            "startChar": "-",
            "c1": "-",
            "c2": "-",
            "endchar": "endChar != 'y'",
            "start, end, s": "-",
            "MSJVM_BUG_WORKAROUND": "-",
            "c": "-",
            "ex": "NumberFormatException ex",
            "toNumber(String s)": "return NaN;"
        }
    ]
}

{
    "Conditions" : {
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
            "start, end": "start == end",
            "sum": "-",
            "radix": "-",
            "nfe": "-",
            "stringToNumber(String s, int start, int radix)": "return NaN;"
        },
        {
            "start, end": "start != end",
            "sum": "sum >= 9007199254740992.0",
            "radix": "radix == 10",
            "nfe": "!(NumberFormatException nfe)",
            "stringToNumber(String s, int start, int radix)": "return Double.valueOf(s.substring(start, end)).doubleValue();"
        },
        {
            "start, end": "start != end",
            "sum": "sum >= 9007199254740992.0",
            "radix": "radix == 10",
            "nfe": "NumberFormatException nfe",
            "stringToNumber(String s, int start, int radix)": "return NaN;"
        },
        {
            "start, end": "start != end",
            "sum": "-",
            "radix": "-",
            "nfe": "-",
            "stringToNumber(String s, int start, int radix)": "return NaN;"
        }
    ]
}

Decision Requirement Level:
{
    "Decisions" : {
        "toNumber(Object val)" : {
            "Input" : ["val", "toNumber(String s)"]
        },
        "toNumber(String s)" : {
            "Input" : ["c", "endchar", "c_one", "start, len", "startChar", "c_second", "start, end, s", "stringToNumber(String s, int start, int radix)"]
        },
        "stringToNumber(String s, int start, int radix)" : {
            "Input" : ["start, len, end", "sum", "radix", "nfe"]
        }
    },
    "InputData" : ["val", "start, end", "sum", "radix", "nfe", "c", "MSJVM_BUG_WORKAROUND", "endchar", "c1", "start, len", "startChar", "c2", "ex", "start, end, s"]
}


CORRESPONDING CODE:

public static double toNumber(Object val)
{
    for (;;) {
        if (val instanceof Number)
            return ((Number) val).doubleValue();
        if (val == null)
            return +0.0;
        if (val == Undefined.instance)
            return NaN;
        if (val instanceof String)
            return toNumber((String) val);
        if (val instanceof Boolean)
            return ((Boolean) val).booleanValue() ? 1 : +0.0;
        if (val instanceof Scriptable) {
            val = ((Scriptable) val).getDefaultValue(NumberClass);
            if (val instanceof Scriptable)
                throw errorWithClassName("msg.primitive.expected", val);
            continue;
        }
        warnAboutNonJSObject(val);
        return NaN;
    }
}

static double stringToNumber(String s, int start, int radix) {
    char digitMax = '9';
    char lowerCaseBound = 'a';
    char upperCaseBound = 'A';
    int len = s.length();
    if (radix < 10) {
        digitMax = (char) ('0' + radix - 1);
    }
    if (radix > 10) {
        lowerCaseBound = (char) ('a' + radix - 10);
        upperCaseBound = (char) ('A' + radix - 10);
    }
    int end;
    double sum = 0.0;
    for (end=start; end < len; end++) {
        char c = s.charAt(end);
        int newDigit;
        if ('0' <= c && c <= digitMax)
            newDigit = c - '0';
        else if ('a' <= c && c < lowerCaseBound)
            newDigit = c - 'a' + 10;
        else if ('A' <= c && c < upperCaseBound)
            newDigit = c - 'A' + 10;
        else
            break;
        sum = sum*radix + newDigit;
    }
    if (start == end) {
        return NaN;
    }
    if (sum >= 9007199254740992.0) {
        if (radix == 10) {
            /* If we're accumulating a decimal number and the number
                * is >= 2^53, then the result from the repeated multiply-add
                * above may be inaccurate.  Call Java to get the correct
                * answer.
                */
            try {
                return Double.valueOf(s.substring(start, end)).doubleValue();
            } catch (NumberFormatException nfe) {
                return NaN;
            }
        } else if (radix == 2 || radix == 4 || radix == 8 ||
                    radix == 16 || radix == 32)
        {
            /* The number may also be inaccurate for one of these bases.
                * This happens if the addition in value*radix + digit causes
                * a round-down to an even least significant mantissa bit
                * when the first dropped bit is a one.  If any of the
                * following digits in the number (which haven't been added
                * in yet) are nonzero then the correct action would have
                * been to round up instead of down.  An example of this
                * occurs when reading the number 0x1000000000000081, which
                * rounds to 0x1000000000000000 instead of 0x1000000000000100.
                */
            int bitShiftInChar = 1;
            int digit = 0;

            final int SKIP_LEADING_ZEROS = 0;
            final int FIRST_EXACT_53_BITS = 1;
            final int AFTER_BIT_53         = 2;
            final int ZEROS_AFTER_54 = 3;
            final int MIXED_AFTER_54 = 4;

            int state = SKIP_LEADING_ZEROS;
            int exactBitsLimit = 53;
            double factor = 0.0;
            boolean bit53 = false;
            // bit54 is the 54th bit (the first dropped from the mantissa)
            boolean bit54 = false;

            for (;;) {
                if (bitShiftInChar == 1) {
                    if (start == end)
                        break;
                    digit = s.charAt(start++);
                    if ('0' <= digit && digit <= '9')
                        digit -= '0';
                    else if ('a' <= digit && digit <= 'z')
                        digit -= 'a' - 10;
                    else
                        digit -= 'A' - 10;
                    bitShiftInChar = radix;
                }
                bitShiftInChar >>= 1;
                boolean bit = (digit & bitShiftInChar) != 0;

                switch (state) {
                    case SKIP_LEADING_ZEROS:
                        if (bit) {
                        --exactBitsLimit;
                        sum = 1.0;
                        state = FIRST_EXACT_53_BITS;
                    }
                    break;
                    case FIRST_EXACT_53_BITS:
                        sum *= 2.0;
                    if (bit)
                        sum += 1.0;
                    --exactBitsLimit;
                    if (exactBitsLimit == 0) {
                        bit53 = bit;
                        state = AFTER_BIT_53;
                    }
                    break;
                    case AFTER_BIT_53:
                    bit54 = bit;
                    factor = 2.0;
                    state = ZEROS_AFTER_54;
                    break;
                    case ZEROS_AFTER_54:
                    if (bit) {
                        state = MIXED_AFTER_54;
                    }
                    // fallthrough
                    case MIXED_AFTER_54:
                    factor *= 2;
                    break;
                }
            }
            switch (state) {
                case SKIP_LEADING_ZEROS:
                sum = 0.0;
                break;
                case FIRST_EXACT_53_BITS:
                case AFTER_BIT_53:
                // do nothing
                break;
                case ZEROS_AFTER_54:
                // x1.1 -> x1 + 1 (round up)
                // x0.1 -> x0 (round down)
                if (bit54 & bit53)
                    sum += 1.0;
                sum *= factor;
                break;
                case MIXED_AFTER_54:
                // x.100...1.. -> x + 1 (round up)
                // x.0anything -> x (round down)
                if (bit54)
                    sum += 1.0;
                sum *= factor;
                break;
            }
        }
        /* We don't worry about inaccurate numbers for any other base. */
    }
    return sum;
}

public static double toNumber(String s) {
    int len = s.length();
    int start = 0;
    char startChar;
    for (;;) {
        if (start == len) {
            // Empty or contains only whitespace
            return +0.0;
        }
        startChar = s.charAt(start);
        if (!Character.isWhitespace(startChar))
            break;
        start++;
    }

    if (startChar == '0') {
        if (start + 2 < len) {
            int c1 = s.charAt(start + 1);
            if (c1 == 'x' || c1 == 'X') {
                // A hexadecimal number
                return stringToNumber(s, start + 2, 16);
            }
        }
    } else if (startChar == '+' || startChar == '-') {
        if (start + 3 < len && s.charAt(start + 1) == '0') {
            int c2 = s.charAt(start + 2);
            if (c2 == 'x' || c2 == 'X') {
                // A hexadecimal number with sign
                double val = stringToNumber(s, start + 3, 16);
                return startChar == '-' ? -val : val;
            }
        }
    }

    int end = len - 1;
    char endChar;
    while (Character.isWhitespace(endChar = s.charAt(end)))
        end--;
    if (endChar == 'y') {
        // check for "Infinity"
        if (startChar == '+' || startChar == '-')
            start++;
        if (start + 7 == end && s.regionMatches(start, "Infinity", 0, 8))
            return startChar == '-'
                ? Double.NEGATIVE_INFINITY
                : Double.POSITIVE_INFINITY;
        return NaN;
    }
    // A non-hexadecimal, non-infinity number:
    // just try a normal floating point conversion
    String sub = s.substring(start, end+1);
    if (MSJVM_BUG_WORKAROUNDS) {
        // The MS JVM will accept non-conformant strings
        // rather than throwing a NumberFormatException
        // as it should.
        for (int i=sub.length()-1; i >= 0; i--) {
            char c = sub.charAt(i);
            if (('0' <= c && c <= '9') || c == '.' ||
                c == 'e' || c == 'E'  ||
                c == '+' || c == '-')
                continue;
            return NaN;
        }
    }
    try {
        return Double.valueOf(sub).doubleValue();
    } catch (NumberFormatException ex) {
        return NaN;
    }
}
""")

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
        model="gpt-4.1"
    )

    return response.choices[0].message.content

temperatures = [0, 0.2, 0.4, 0.6, 0.8, 1]
cases = [case_1, case_2, case_3, case_4, case_5]

query_2 = f"""
Consider the following examples (3 examples):

Input: {example_1_input}
Expected JSON output: {example_1_output}

Input: {example_2_input}
Expected JSON output: {example_2_output}

Input: {example_3_input}
Expected JSON output: {example_3_output}

Could you generate a DMN XML file based on the following JSON objects?

Inconsistencies in naming and relationships between these JSON objects must be resolved to produce a valid DMN XML representation. Please note that these inconsistencies are not present in the examples because the examples focus on showing how the JSON objects are translated to DMN XML.
Follow the rules below to address these inconsistencies by addressing them in the final DMN XML file. To help resolve the inconsistencies, the corresponding Java source code (marked CORRESPONDING CODE) is provided for reference. Refer to this code where necessary to ensure alignment.

1) There are some naming inconsistencies between the `Decision Requirement Level` and `Decision Logic Level` JSON objects, i.e., different names are sometimes used for the same DMN element. Ensure that the DMN XML uses consistent naming at both levels when the same DMN element appears under different names. When choosing between conflicting names, use the one that best aligns with the Java source code. For example, do not use made-up names or names that include field/property accesses (e.g., use user, not user.name).
2) Sometimes multiple (different) names are used for the same DMN element across the `Decision Logic Level` and/or `Decision Requirement Level` JSON objects. In such cases, combine these into a single, consistently named DMN element within the DMN XML that best aligns with the Java source code. Again, please note that the selected name must be used consistently across both levels in the resulting DMN XML.
3) In the `Decision Requirement Level` JSON object, some decisions (i.e., functions) are used as inputs to other decisions. In each such case, ensure that the corresponding decision tables in the `Decision Logic Level` include input columns for these input decisions in the resulting DMN XML.

It is important to note that while DMN elements may be renamed or combined for consistency, no original DMN element or its underlying logic should be lost in the transformation process.

Only provide the DMN XML.
Do not write anything else.

Analyze the following JSON objects (marked as DMN JSON OBJECTS) and corresponding Java source code (marked as CORRESPONDING CODE):
"""

def run_query(code, case_name, temperature):
    input = ['We will ask you two questions on Decision Model and Notation. Each question starts with "Q:", and each response should start with "A:" followed by your answer. Only provide an answer to the question which has not been answered yet. Respond using only regular sentences, unless specified otherwise. Do you know Decision Model and Notation and can you create a DMN XML?',
        query_2 + code]
    
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