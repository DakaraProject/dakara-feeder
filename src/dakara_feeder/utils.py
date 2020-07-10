def divide_chunks(iterable, chunk_size):
    """Yield successive chunk_size-sized
    chunks from iterable."""
    # looping till length iterable
    for i in range(0, len(iterable), chunk_size):
        yield iterable[i : i + chunk_size]
