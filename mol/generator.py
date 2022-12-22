from openfermion.transforms import bravyi_kitaev, get_fermion_operator

from mol.backend import run_pyscf
from mol.get_HF_operation import get_HF_operator

CHEMICAL_ACCURACY = 0.001
from openfermion.chem import MolecularData

"""
class MolecularData:
    def __init__(self, geometry, basis, multiplicity, charge, use_symmetry, info):
        self.geometry = geometry
        self.basis = basis
        self.multiplicity = multiplicity
        self.charge = charge
        self.symmetry = use_symmetry
        self.info = info

        self.n_orbitals = None
        self.n_electrons = None
"""


def make_molecular_hamil(geometry, basis="sto-3g", run_fci=False, annotation="Untitled", n_cancel_orbital=0,
                         n_frozen_orbital=0,
                         cas_irrep_nocc=None, cas_irrep_ncore=None, fermi_qubit_transform=bravyi_kitaev):
    # Get fermion Hamiltonian
    multiplicity = 1
    charge = 0

    molecule = MolecularData(geometry, basis, multiplicity, charge, annotation)
    molecule.symmetry = True

    molecule = run_pyscf(molecule, run_fci=run_fci, n_frozen_orbital=n_frozen_orbital,
                         n_cancel_orbital=n_cancel_orbital, cas_irrep_nocc=cas_irrep_nocc,
                         cas_irrep_ncore=cas_irrep_ncore, verbose=False)

    fermion_hamiltonian = get_fermion_operator(
        molecule.get_molecular_hamiltonian(occupied_indices=molecule.frozen_orbitals,
                                           active_indices=molecule.active_orbitals))

    # Map fermion Hamiltonian to qubit Hamiltonian
    qubit_hamiltonian = fermi_qubit_transform(fermion_hamiltonian)

    qubit_electron_operator = get_HF_operator(
        molecule.n_electrons, fermi_qubit_transform)

    # Ignore terms in Hamiltonian that close to zero
    qubit_hamiltonian.compress()

    return qubit_hamiltonian, fermion_hamiltonian, {"hf": molecule.hf_energy, "fci": molecule.fci_energy}
