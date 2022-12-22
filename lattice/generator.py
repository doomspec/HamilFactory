from openfermion import QubitOperator

def two_dimensional_transverse_field_ising_model(n_col, n_row, g, J=1.0):
    """
    Using the notation of https://en.wikipedia.org/wiki/Transverse-field_Ising_model
    """
    n_qubit = n_col * n_row

    terms = {}
    for i in range(n_row):
        for j in range(n_col - 1):
            left = i * n_col + j
            terms[((left, "Z"), (left + 1, "Z"))] = -J
    for i in range(n_row - 1):
        for j in range(n_col):
            up = i * n_col + j
            down = up + n_col
            terms[((up, "Z"), (down, "Z"))] = -J

    for i in range(n_qubit):
        terms[((i, "X"),)] = -J*g

    op = QubitOperator()
    op.terms = terms
    op.compress()

    return op
