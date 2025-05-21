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