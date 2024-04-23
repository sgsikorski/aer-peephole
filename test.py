import sys
import qiskit

from qiskit_aer import AerSimulator

from qiskit_aer.noise import NoiseModel
from qiskit_ibm_runtime import QiskitRuntimeService
import time

def printReadableResults(result):
    print(f"Time taken to execute: {result.metadata['time_taken_execute']}\n"
          f"Time taken to transpile: {result.time_taken}\n"
          f"Max CPU Memory: {result.metadata['max_memory_mb']}\n"
          f"Max GPU Memory: {result.metadata['max_gpu_memory_mb']}")

if __name__ == '__main__':
    ##############################
    # Compile Args
    ##############################

    qc = qiskit.QuantumCircuit.from_qasm_file('qasm/qft_28.qasm')
    qc.measure_all()
    # print(qc)

    # Ideal simulator
    aersim = AerSimulator(method="automatic")

    aersim.set_options(fusion_enable=False)
    aersim.set_options(fusion_verbose=False)
    # TODO: Enable this option in configs
    # aersim.set_options(peephole_enable=True)

    print("RUNNING SIMULATION...")
    job = aersim.run(qc)
    result_ideal = job.result()
    print(result_ideal)
    print("SIMULATION DONE!")
    printReadableResults(result_ideal)