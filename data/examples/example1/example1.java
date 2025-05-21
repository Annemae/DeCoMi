public static <T> @Nullable T getNext(Iterator<? extends T> iterator, @Nullable T defaultValue) {
    return iterator.hasNext() ? iterator.next() : defaultValue;
}