def compare_collections():
    print("=== Python Collection Types Comparison ===\n")
    
    # Sample data with duplicates
    data = [1, 2, 2, 3]

    # List
    list_example = list(data)
    print("List:")
    print(" Value:", list_example)
    print(" Ordered:", True)
    print(" Allows Duplicates:", True)
    print(" Mutable:", True)
    print()

    # Set
    set_example = set(data)
    print("Set:")
    print(" Value:", set_example)
    print(" Ordered (Python 3.7+):", True)
    print(" Allows Duplicates:", False)
    print(" Mutable:", True)
    print()

    # Tuple
    tuple_example = tuple(data)
    print("Tuple:")
    print(" Value:", tuple_example)
    print(" Ordered:", True)
    print(" Allows Duplicates:", True)
    print(" Mutable:", False)
    print()

    # Dict
    dict_example = {k: f"value_{k}" for k in data}  # Duplicate keys will be overwritten
    print("Dict:")
    print(" Value:", dict_example)
    print(" Ordered (Python 3.7+):", True)
    print(" Allows Duplicates (keys):", False)
    print(" Mutable:", True)
    print()

compare_collections()
