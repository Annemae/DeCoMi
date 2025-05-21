from google import genai
from google.genai import types

case_1 = """
public static void checkArgument(boolean expression) {
  if (!expression) {
    throw new IllegalArgumentException();
  }
}
"""

case_2 = """
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
"""

case_3 = """
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
"""

case_4 = """
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
"""

case_5 = """
public static double toNumber(Object val)
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
"""

case_6 = """
/**
 * Backed up property.
 * @since jEdit 3.2pre2
 */
public static final String BACKED_UP = "Buffer__backedUp";

/**
 * Caret info properties.
 * @since jEdit 3.2pre1
 */
public static final String CARET = "Buffer__caret";
public static final String CARET_POSITIONED = "Buffer__caretPositioned";

/**
 * Stores a List of {@link org.gjt.sp.jedit.textarea.Selection} instances.
 */
public static final String SELECTION = "Buffer__selection";

/**
 * This should be a physical line number, so that the scroll
 * position is preserved correctly across reloads (which will
 * affect virtual line numbers, due to fold being reset)
 */
public static final String SCROLL_VERT = "Buffer__scrollVert";
public static final String SCROLL_HORIZ = "Buffer__scrollHoriz";

/**
 * Should jEdit try to set the encoding based on a UTF8, UTF16 or
 * XML signature at the beginning of the file?
 */
public static final String ENCODING_AUTODETECT = "encodingAutodetect";

/**
 * This property is set to 'true' if the file has a trailing newline.
 * @since jEdit 4.0pre1
 */
public static final String TRAILING_EOL = "trailingEOL";

/**
 * This property is set to 'true' if the file should be GZipped.
 * @since jEdit 4.0pre4
 */
public static final String GZIPPED = "gzipped";
"""

case_7 = """
public static CommonPattern compile(String pattern) {
  return Platform.compilePattern(pattern);
}
"""

case_8 = """
/** {@inheritDoc}. */
public void executeTargets(Project project, String[] targetNames)
    throws BuildException {
    BuildException thrownException = null;
    for (String targetName : targetNames) {
        try {
            project.executeTarget(targetName);
        } catch (BuildException ex) {
            if (project.isKeepGoingMode()) {
                thrownException = ex;
            } else {
                throw ex;
            }
        }
    }
    if (thrownException != null) {
        throw thrownException;
    }
}
"""

case_9 = """
private static NotationSettings initializeDefaultSettings() {
    NotationSettings settings = new NotationSettings();
    settings.parent = null;
    settings.setNotationLanguage(Notation.DEFAULT_NOTATION);
    settings.setFullyHandleStereotypes(false);
    settings.setShowAssociationNames(true);
    settings.setShowInitialValues(false);
    settings.setShowMultiplicities(false);
    settings.setShowPaths(false);
    settings.setShowProperties(false);
    settings.setShowSingularMultiplicities(true);
    settings.setShowTypes(true);
    settings.setShowVisibilities(false);
    settings.setUseGuillemets(false);
    return settings;
}
"""

case_10 = """
public synchronized void channelsProgress(String id, double p) {
    ProgressNode pn = progressNodes.get(id);
    boolean ins = false;
    if (pn == null) {
      pn = new ProgressNode();
      progressNodes.put(id, pn);
      ins = true;
    }
    if (!filesNodeInTree) {
      model.insertNodeInto(filesNode, rootNode, 0);
      filesNodeInTree = true;
      ins = true;
    }
    pn.setProgress(p);
    if (ins) {
      model.insertNodeInto(pn, filesNode, 0);
      dataTree.expandPath(new TreePath(filesNode.getPath()));
    }
    if (p == 1) {
      progressNodes.remove(id);
      filesNode.remove(pn);
    }
    dataTree.repaint();
}
"""

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
        max_output_tokens=10000,
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
cases = [case_1, case_2, case_3, case_4, case_5, case_6, case_7, case_8, case_9, case_10]

case_counter = 0
def run_query(code, temperature):
    global case_counter
    input = ['Do you know Decision Model and Notation and can you create a DRD?',
        f'Given a part of Java source code, you are expected to provide a DRD in a structured JSON format. Examples (6 examples): \n\n  \n\n Input: {example_1_input} \n Expected JSON output: {example_1_output} \n Input: {example_2_input} \n Expected JSON output: {example_2_output} \n Input: {example_3_input} \n Expected JSON output: {example_3_output} \n Input: {example_4_input} \n Expected JSON output: {example_4_output} \n Input: {example_5_input} \n Expected JSON output: {example_5_output} \n Input: {example_6_input} \n Expected JSON output: {example_6_output}\n\n Please provide the DRD as a complete, valid JSON object. The JSON object should contain the decisions and the input data, if they are present. Do not write anything else. Analyze the following part of Java source code: {code}',]
    
    query = ""
        
    for question in input:
        query += f"Q: {question} \n\n"
        response = generate(query, temperature)
        query += f"{response}\n\n"

    open(f"results/case_{case_counter}_temp_{temperature}.txt", "w").write(query)

    case_counter += 1


if __name__ == "__main__":
    for temperature in temperatures:
        for case in cases:
            print(f"Running case {case_counter} with temperature {temperature}...")
            run_query(case, temperature)