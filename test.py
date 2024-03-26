import sys
import qiskit

from qiskit_aer import AerSimulator

from qiskit_aer.noise import NoiseModel
from qiskit_ibm_runtime import QiskitRuntimeService
import time

import argparse

qc = qiskit.QuantumCircuit.from_qasm_file('qasm_data/iqp_28.qasm')
# print(qc)

# Generate 3-qubit GHZ state
circ = qiskit.QuantumCircuit(3)
circ.h(0)
circ.cx(0, 1)
circ.cx(1, 2)
circ.measure_all()

# noise_model = NoiseModel.from_backend(backend)
# Construct an ideal simulator
aersim = AerSimulator(method="statevector")
# aersim.set_options(device="GPU")
aersim.set_options(fusion_enable=False)
# aersim.set_options(peephole_enable=True)

# Perform an ideal simulation
job = aersim.run(circ)
result_ideal = job.result()
counts_ideal = result_ideal.get_counts(0)
# time_ = job.time_taken()
print('Counts(ideal):', counts_ideal)
# Counts(ideal): {'000': 493, '111': 531}