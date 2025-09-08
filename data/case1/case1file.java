/**
 * Ensures the truth of an expression involving one or more parameters to the calling method.
 *
 * @param expression a boolean expression
 * @throws IllegalArgumentException if {@code expression} is false
 */
public static void checkArgument(boolean expression) {
    if (!expression) {
        throw new IllegalArgumentException();
    }
}
