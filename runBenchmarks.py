import sys
import os
import argparse
import time
import tqdm
import numpy as np

import matplotlib.pyplot as plt

import qiskit
from qiskit_aer import AerSimulator
import qiskit_aer as qa
from qiskit_aer.noise import NoiseModel
from qiskit_ibm_runtime import QiskitRuntimeService

def plotSweepingResults(means, std_devs, benchmark):
    x = [3, 7, 11, 28, 29]

    # Plotting the means with error bars
    plt.errorbar(x, means, yerr=std_devs, fmt='o', capsize=5)

    # Adding labels and title
    plt.xlabel('Number of Qubits')
    plt.ylabel('Time (s)')
    plt.title(f'Execution Time Means for {benchmark} with Standard Deviations')
    plt.savefig(f'plots/{benchmark}_2')


def printReadableResults(result, bm, sIdx, fus, p):
    fus = "" if not fus else "fus"
    p = "" if not p else "p"
    transpileTime = result.time_taken - result.metadata['time_taken_execute'] \
                    - result.metadata['time_taken_parameter_binding']
    with open(f"results/{bm}/{bm}_{fus}_{p}.txt", "a+") as f:
        f.write("\n===================================\n")
        f.write(f"{bm}: {sIdx}\n")
        f.write(f"Time taken to execute: {result.metadata['time_taken_execute']}\n"
                f"Time taken to transpile: {transpileTime}\n"
                f"Max CPU Memory: {result.metadata['max_memory_mb']}\n"
                f"Max GPU Memory: {result.metadata['max_gpu_memory_mb']}")
        f.write("\n===================================\n")

def printMeanStd(transpile_times, execute_times, bm, fus, p):
    fus = "" if not fus else "fus"
    p = "" if not p else "p"
    mean_transpile = np.mean(transpile_times)
    std_transpile = np.std(transpile_times)
    
    mean_execute = np.mean(execute_times)
    std_execute = np.std(execute_times)

    with open(f"results/{bm}/{bm}_{fus}_{p}.txt", "a+") as f:
        f.write(f"Mean execute: {mean_execute}\n"
            f"STD execute: {std_execute}\n"
            f"Mean transpile: {mean_transpile}\n"
            f"STD transpile: {std_transpile}\n")

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--fusion", action="store_true")
    ap.add_argument("-b", "--benchmarks", required=True)
    ap.add_argument("-p", "--peephole", action="store_true")
    args = ap.parse_args()

    sample_count = 5

    # Ideal simulator
    # TODO: Enable this option in configs
    # aersim.set_options(peephole_enable=True)

    benchmarks = os.listdir(f'qasm/{args.benchmarks.lower()}')
    benchmarks = ["iqp_3.qasm", "iqp_7.qasm", "iqp_11.qasm", "iqp_28.qasm", "iqp-29.qasm"]
    execute_time = np.zeros(sample_count)
    transpile_times = np.zeros(sample_count)

    eMean = []
    tMean = []
    eStd = []
    tStd = []
    for qasm_code in benchmarks: #tqdm.tqdm(benchmarks, desc="Running simulation..."):
        execute_times = np.zeros(sample_count)
        transpile_times = np.zeros(sample_count)
        qc = qiskit.QuantumCircuit.from_qasm_file(f'qasm/{args.benchmarks.lower()}/{qasm_code}')
        qc.measure_all()
        # print(qc)
        aersim = AerSimulator(method="statevector", device="GPU", shots=100)
        aersim.set_options(fusion_enable=args.fusion)
        for i in range(sample_count):
            start_transpile = time.time()
            transpiled_circuit = qiskit.transpile(qc, aersim)
            end_transpile = time.time()
            transpile_times[i] = end_transpile - start_transpile

            job = aersim.run(qc)
            transpiled_circuit = job.circuits()
            gate_counts = transpiled_circuit[0].count_ops()
            #print(gate_counts)

            result_ideal = job.result()
            execute_times[i] = result_ideal.metadata['time_taken_execute']
            #printReadableResults(result_ideal, args.benchmarks.lower(), i, args.fusion, args.peephole)
        #printMeanStd(transpile_times, execute_times, args.benchmarks.lower(), args.fusion, args.peephole)
        eMean.append(np.mean(execute_times))
        tMean.append(np.mean(transpile_times))
        eStd.append(np.std(execute_times))
        tStd.append(np.std(transpile_times))
    
    plotSweepingResults(eMean, eStd, args.benchmarks.upper())
    plotSweepingResults(tMean, tStd, args.benchmarks.upper())