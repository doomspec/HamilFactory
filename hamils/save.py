import pickle
def save_hamil(hamil, n_qubit, category, title, other_info=None):
    data = {
        "term" : hamil.terms,
        "n_site": n_qubit
    }
    data.update(other_info or {})
    with open(f"./hamils/{category}/{title}.op", "wb") as f:
        pickle.dump(data, f)