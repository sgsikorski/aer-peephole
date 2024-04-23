import sys
import os
import argparse
import time
import tqdm
import numpy as np

import qiskit
from qiskit_aer import AerSimulator
import qiskit_aer as qa
from qiskit_aer.noise import NoiseModel
from qiskit_ibm_runtime import QiskitRuntimeService


def printReadableResults(result, bm, sIdx, fus):
    fus = "" if not fus else "fus"
    transpileTime = result.time_taken - result.metadata['time_taken_execute'] \
                    - result.metadata['time_taken_parameter_binding']
    with open(f"results/{bm}/{bm}_{fus}_p.txt", "a+") as f:
        f.write("\n===================================\n")
        f.write(f"{bm}: {sIdx}\n")
        f.write(f"Time taken to execute: {result.metadata['time_taken_execute']}\n"
                f"Time taken to transpile: {transpileTime}\n"
                f"Max CPU Memory: {result.metadata['max_memory_mb']}\n"
                f"Max GPU Memory: {result.metadata['max_gpu_memory_mb']}")
        f.write("\n===================================\n")

def printMeanStd(transpile_times, execute_times, bm, fus):
    fus = "" if not fus else "fus"
    mean_transpile = np.mean(transpile_times)
    std_transpile = np.std(transpile_times)
    
    mean_execute = np.mean(execute_times)
    std_execute = np.std(execute_times)

    with open(f"results/{bm}/{bm}_{fus}_p.txt", "a+") as f:
        f.write(f"Mean execute: {mean_execute}\n"
            f"STD execute: {std_execute}\n"
            f"Mean transpile: {mean_transpile}\n"
            f"STD transpile: {std_transpile}\n")

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--fusion", action="store_true")
    ap.add_argument("-b", "--benchmarks", required=True)
    args = ap.parse_args()

    sample_count = 10

    # Ideal simulator
    aersim = AerSimulator(method="automatic", device="GPU", shots=1024)
    aersim.set_options(fusion_enable=args.fusion)
    aersim.set_options(fusion_verbose=args.fusion)
    # TODO: Enable this option in configs
    # aersim.set_options(peephole_enable=True)

    benchmarks = os.listdir(f'qasm/{args.benchmarks.lower()}')
    execute_time = np.zeros(sample_count)
    transpile_times = np.zeros(sample_count)

    
    for qasm_code in tqdm.tqdm(benchmarks, desc="Running simulation..."):
        execute_times = np.zeros(sample_count)
        transpile_times = np.zeros(sample_count)
        for i in range(sample_count):
            qc = qiskit.QuantumCircuit.from_qasm_file(f'qasm/{args.benchmarks.lower()}/{qasm_code}')
            qc.measure_all()
            # print(qc)

            start_transpile = time.time()
            transpiled_circuit = qiskit.transpile(qc, aersim)
            end_transpile = time.time()
            print(transpiled_circuit.count_ops())
            transpile_times[i] = end_transpile - start_transpile

            job = aersim.run(transpiled_circuit)

            result_ideal = job.result()
            execute_times[i] = result_ideal.metadata['time_taken_execute']
            # print(result_ideal)
            printReadableResults(result_ideal, args.benchmarks.lower(), i, args.fusion)
        printMeanStd(transpile_times, execute_times, args.benchmarks.lower(), args.fusion)