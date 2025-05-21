protected void checkInterval(long start, long end) {
  if (end < start) {
      throw new IllegalArgumentException("The end instant must be greater than the start instant");
  }
}