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