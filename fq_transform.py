from openfermion.transforms import jordan_wigner, bravyi_kitaev, binary_code_transform, parity_code


def get_parity_transform(n_spinorbital):
    def parity_transform(FermionOperator):
        return binary_code_transform(FermionOperator, parity_code(n_spinorbital))
    return parity_transform


def get_transform_dict(n_spinorbital):
    trans_dict = {
        "JW": jordan_wigner,
        "BK": bravyi_kitaev,
        "P": get_parity_transform(n_spinorbital)
    }
    return trans_dict