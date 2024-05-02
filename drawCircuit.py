import qiskit
import qiskit.circuit.library as circs
from qiskit.visualization.library import _generate_circuit_library_visualization

if __name__ == '__main__':
    A = [[6, 5, 3], [5, 4, 5], [3, 5, 1]]
    # qc = circs.IQP(A)
    qc = qiskit.QuantumCircuit.from_qasm_file('qasm/hlf/hidden_linear_function_28.qasm')
    print(qc)
    qc.draw(output='mpl', filename="HLF_circuit")
    _generate_circuit_library_visualization(qc.decompose())