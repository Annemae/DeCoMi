public static void checkArgument(boolean expression) {
  if (!expression) {
    throw new IllegalArgumentException();
  }
}
