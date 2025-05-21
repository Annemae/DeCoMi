/**
 * Returns the next element in {@code iterator} or {@code defaultValue} if the iterator is empty.
 * The {@link Iterables} analog to this method is {@link Iterables#getFirst}.
 *
 * @param defaultValue the default value to return if the iterator is empty
 * @return the next element of {@code iterator} or the default value
 * @since 7.0
 */
public static <T> @Nullable T getNext(Iterator<? extends T> iterator, @Nullable T defaultValue) {
    return iterator.hasNext() ? iterator.next() : defaultValue;
}