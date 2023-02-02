#!/usr/bin/env python
# coding: utf-8
#In[1]:
from numpy import *
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile,execute, BasicAer, Aer,IBMQ
import matplotlib.pyplot as plt
import numpy as np
import math
from qiskit.visualization import plot_histogram, plot_bloch_vector, plot_bloch_multivector, plot_state_qsphere
from qiskit.extensions import Initialize
from qiskit.quantum_info import state_fidelity, partial_trace, Statevector
from qiskit.ignis.verification.tomography import state_tomography_circuits, StateTomographyFitter
#In[2]:
#Choosing the desired device
IBMQ.load_account()
provider = IBMQ.get_provider('ibm-q')
backend = provider.get_backend('ibmq_manila')
simulator = Aer.get_backend('qasm_simulator')
#In[3]:
#Number of input states
ntheta = 25
nphi = 25
dtheta = pi/(ntheta)
dphi = 2*pi/(nphi)
#Rotation of noisy action
nalpha = 1
dalpha = pi/(nalpha)
#Values for computation of state fidelity

for ialpha in range(0, nalpha+1):
    alpha = dalpha * ialpha
    avef = 0
    for iphi in range(0,nphi):
        phi = dphi*iphi
        for itheta in range(0,ntheta):
            theta = dtheta*itheta
                #Circuit creation
            qrA = QuantumRegister(2)
            qrB = QuantumRegister(1)
            qrN = QuantumRegister(1)
            cr1 = ClassicalRegister(1)
            cr2 = ClassicalRegister(1)
            mycircuit = QuantumCircuit(qrA, qrB, qrN,cr1, cr2)
                #Initial State setup
            sv = [cos(theta/2), sin(theta/2)*exp(1j*phi)]
            mycircuit.initialize(sv,[0])
                #Entanglement between alice2 and bob qubits
            mycircuit.h(qrA[1])
            mycircuit.cx(qrA[1], qrB[0])
            mycircuit.barrier()
                #First Stage of Noise
            mycircuit.h(qrN[0])
            mycircuit.crx(alpha, qrN[0], qrA[0])
            mycircuit.barrier()
                #Bell State Measurement on Alice's parties
            mycircuit.cx(qrA[0], qrA[1])
            mycircuit.h(qrA[0])
            mycircuit.barrier()
                #Second Stage of Noise
            #mycircuit.h(qrN[0])
            #mycircuit.crx(alpha, qrN[0], qrA[0])
            #mycircuit.barrier()
                #DMP - Recovery operation on bob's qubit
            mycircuit.cx(qrA[1], qrB[0])
            mycircuit.cz(qrA[0], qrB[0])
            mycircuit.barrier()
                #Quantum State Tomography Circuits
            qstom = state_tomography_circuits(mycircuit, qrB[0])
            nshots = 1_000
        #REAL Device Execution
            #qstcir = transpile(qstom, backend = backend, optimization_level=3, layout_method='sabre', routing_method='sabre')
            #result = execute(qstcir, backend = backend, shots = nshots).result()
                #Data Fit and State fidelity computation
            #qst_cir = StateTomographyFitter(result, qstom)
            #sv_qst = qst_cir.fit(method='lstsq')
            #sf = state_fidelity(sv, sv_qst, validate=False)
        
        #QASM Simulator Execution
            result = execute(qstom, backend = simulator, optimization_level = 3,shots = nshots).result()
                #Data Fit and State fidelity computation
            qst_cir = StateTomographyFitter(result, qstom)
            sv_qst = qst_cir.fit(method='cvx')
            sf = state_fidelity(sv, sv_qst, validate=False)
            #Fidelities sum
            avef += sf*sin(theta)
    #Average fidelity
    avet = avef/(4*pi)*dtheta*dphi
    print(alpha, avet)