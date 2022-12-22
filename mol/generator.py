from openfermion.transforms import bravyi_kitaev, get_fermion_operator
from openfermionpyscf import run_pyscf
from openfermion.chem import MolecularData

CHEMICAL_ACCURACY = 0.001

def make_molecular_hamil(geometry, basis="sto-3g", run_fci=False, fermi_qubit_transform=bravyi_kitaev):
    # Get fermion Hamiltonian
    multiplicity = 1
    charge = 0
    molecule = MolecularData(geometry, basis, multiplicity, charge)
    molecule.symmetry = True

    molecule = run_pyscf(molecule, run_fci=run_fci, verbose=False)

    fermion_hamiltonian = get_fermion_operator(molecule.get_molecular_hamiltonian())
    # Map fermion Hamiltonian to qubit Hamiltonian
    qubit_hamiltonian = fermi_qubit_transform(fermion_hamiltonian)
    # Ignore terms in Hamiltonian that close to zero
    qubit_hamiltonian.compress()

    return qubit_hamiltonian, fermion_hamiltonian, {"hf": molecule.hf_energy, "fci": molecule.fci_energy}
