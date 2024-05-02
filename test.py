import sys
import qiskit

from qiskit_aer import AerSimulator

from qiskit_aer.noise import NoiseModel
from qiskit_ibm_runtime import QiskitRuntimeService
import time
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_state_city

def printReadableResults(result):
    print(f"Time taken to execute: {result.metadata['time_taken_execute']}\n"
          f"Time taken: {result.time_taken}\n"
          f"Max CPU Memory: {result.metadata['max_memory_mb']}\n"
          f"Max GPU Memory: {result.metadata['max_gpu_memory_mb']}")

if __name__ == '__main__':
    ##############################
    # Compile Args
    ##############################

    qc = qiskit.QuantumCircuit.from_qasm_file('qasm/grover_search_28.qasm')
    qc.measure_all()

    # Ideal simulator
    aersim = AerSimulator(method="automatic", device="GPU", shots=1000)

    aersim.set_options(fusion_enable=False)
    aersim.set_options(fusion_verbose=False)

    transpiled_circuit = qiskit.transpile(qc, aersim, optimization_level=0)
    # TODO: Enable this option in configs
    # aersim.set_options(peephole_enable=True)

    print("RUNNING SIMULATION...")
    job = aersim.run(qc)
    result_ideal = job.result()
    print(result_ideal)
    print("SIMULATION DONE!")
    printReadableResults(result_ideal)

    gate_counts = transpiled_circuit.count_ops()
    print(gate_counts)

    #state = Statevector(qc)
    #plot = plot_state_city(state, alpha=1)
    #plot.savefig("state_city", format="jpeg")