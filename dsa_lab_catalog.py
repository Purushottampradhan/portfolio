"""Problem catalog for the DSA visual lab. Each topic has one solvable function."""


def register(add):
    from catalog_foundations import register as part
    part(add)
    from catalog_arrays import register as part
    part(add)
    from catalog_search import register as part
    part(add)
    from catalog_structures import register as part
    part(add)
    from catalog_graphs import register as part
    part(add)
    from catalog_advanced import register as part
    part(add)
