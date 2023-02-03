# Temportal-Causality-in-Quantum-Teleportation-using-Qiskit

Code implementation of Temporal Causality Techniques into the Standard Protocol of Teleportation.

The implementation of an environment that produces noise on the protocols of teleportation is managed by the entanglement of an extra qubit. The average fidelity is used as test value in order to examine the dependence of the interaction noise-systems. 

This provides an easy model to spy on the effects of noise on state-of-art quantum devices. The results of this model show how the entanglement between the system environment can modify the information that was sent, increasing the average fidelity to the classical value. These results can be checked here: https://repositorio.yachaytech.edu.ec/handle/123456789/562.

# Code Explanation

We have implemented for this kind of protocol two scenarios of noise. The first is placed after the creation of the input state and the entangled state, and the second one is placed after the Bell State Measurement. Once the code runs, we can check how the fidelity changes by changing the theta parameter of the crx-gate. We can see that the code possesses the second scenario commented. It is just needed to comment on the first part and uncomment the second one in order to compare how the fidelity curves change, which is the main definition of temporal causality. 
