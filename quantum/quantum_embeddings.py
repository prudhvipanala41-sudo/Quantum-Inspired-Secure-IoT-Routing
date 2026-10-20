"""
Quantum State Amplitude Hilbert Embedding (QSAHE) and Quantum Overlap Metrics.
Provides foundational mathematical transformations for encoding classical IoT node
feature vectors into normalized complex Hilbert space states, calculating density
matrices, quantum fidelity, Von Neumann entropy, and Bloch sphere projections.
"""

import numpy as np


def normalize_vector(v):
    """Normalize a vector to unit L2 norm."""
    norm = np.linalg.norm(v)
    if norm < 1e-12:
        return v
    return v / norm


def quantum_state_embedding(features, method="amplitude"):
    r"""
    Quantum State Amplitude Hilbert Embedding (QSAHE).
    Maps a d-dimensional classical feature vector x into a quantum statevector |psi(x)>.

    Parameters
    ----------
    features : np.ndarray, shape (N, D) or (D,)
        Classical feature array (e.g., [x, y, energy, trust, distance_to_bs]).
    method : str
        'amplitude' : Amplitude encoding into 2^n dimensional Hilbert space.
        'angle'     : Multi-qubit tensor product angle encoding |psi> = \otimes [cos(theta_k)|0> + sin(theta_k)|1>].

    Returns
    -------
    np.ndarray : Statevectors for each node, shape (N, Dim) with ||psi_i|| = 1.
    """
    features = np.asarray(features, dtype=float)
    single = features.ndim == 1
    if single:
        features = features.reshape(1, -1)

    n_samples, n_features = features.shape

    if method == "amplitude":
        # Pad with zeros to nearest power of 2
        dim = int(2 ** np.ceil(np.log2(max(n_features, 2))))
        padded = np.zeros((n_samples, dim), dtype=complex)
        padded[:, :n_features] = features

        # Normalize each row to unit L2 norm (sum of squared amplitudes = 1)
        norms = np.linalg.norm(padded, axis=1, keepdims=True)
        norms[norms < 1e-12] = 1.0
        psi = padded / norms

    elif method == "angle":
        # Feature values scaled to [0, pi]
        # |psi_k> = cos(theta_k)|0> + sin(theta_k)|1>
        # Tensor product across features produces 2^n dimensional state
        thetas = features * (np.pi / (np.max(features, axis=0, keepdims=True) + 1e-9))
        psi_list = []
        for i in range(n_samples):
            state = np.array([1.0], dtype=complex)
            for theta in thetas[i]:
                qubit_state = np.array([np.cos(theta), np.sin(theta)], dtype=complex)
                state = np.kron(state, qubit_state)
            psi_list.append(state)
        psi = np.array(psi_list)
    else:
        raise ValueError(f"Unknown embedding method: {method}")

    return psi[0] if single else psi


def quantum_density_matrix(psi, purity=1.0):
    """
    Constructs the Quantum Density Matrix rho = purity * |psi><psi| + (1-purity) * (I/D).
    Allows modeling quantum decoherence and environmental noise in IoT channels.
    """
    psi = np.asarray(psi, dtype=complex)
    if psi.ndim == 1:
        psi = psi.reshape(1, -1)

    n_samples, dim = psi.shape
    rhos = np.zeros((n_samples, dim, dim), dtype=complex)
    identity = np.eye(dim, dtype=complex) / dim

    for i in range(n_samples):
        state = psi[i].reshape(-1, 1)
        pure_rho = state @ state.conj().T
        rhos[i] = purity * pure_rho + (1.0 - purity) * identity

    return rhos[0] if n_samples == 1 else rhos


def quantum_state_fidelity(psi1, psi2):
    """
    Computes Quantum State Overlap Fidelity F(|psi1>, |psi2>) = |<psi1|psi2>|^2.
    For pure states: F in [0, 1].
    Distance metric: D_Q = 1 - F.
    """
    orig_psi1_single = (psi1.ndim == 1)
    orig_psi2_single = (psi2.ndim == 1)

    if orig_psi1_single and orig_psi2_single:
        inner = np.vdot(psi1, psi2)
        return float(np.abs(inner) ** 2)

    if psi1.ndim == 1:
        psi1 = psi1.reshape(1, -1)
    if psi2.ndim == 1:
        psi2 = psi2.reshape(1, -1)

    # Matrix of fidelities (N1, N2)
    inners = psi1 @ psi2.conj().T
    res = np.abs(inners) ** 2

    if orig_psi2_single:
        return res.ravel()
    if orig_psi1_single:
        return res.ravel()
    return res


def quantum_von_neumann_entropy(rho):
    """
    Computes Quantum Von Neumann Entropy S(rho) = -Tr(rho ln rho).
    Measures quantum entanglement and state uncertainty.
    """
    eigenvalues = np.linalg.eigvalsh(rho)
    eigenvalues = eigenvalues[eigenvalues > 1e-12]
    return -float(np.sum(eigenvalues * np.log2(eigenvalues)))


def bloch_sphere_coordinates(psi):
    """
    Maps 2D or projected multi-qubit quantum statevectors to 3D Bloch sphere coordinates (x, y, z).
    |psi> = cos(theta/2)|0> + e^(i*phi)*sin(theta/2)|1>
    Bloch vector:
        r_x = 2 * Re(c0 * c1*)
        r_y = 2 * Im(c1 * c0*)
        r_z = |c0|^2 - |c1|^2
    """
    psi = np.asarray(psi, dtype=complex)
    single = psi.ndim == 1
    if single:
        psi = psi.reshape(1, -1)

    n_samples, dim = psi.shape
    coords = np.zeros((n_samples, 3))

    for i in range(n_samples):
        c0 = psi[i, 0]
        c1 = psi[i, 1] if dim > 1 else 0.0 + 0.0j

        # Normalize 2-level subspace
        sub_norm = np.sqrt(np.abs(c0)**2 + np.abs(c1)**2)
        if sub_norm > 1e-9:
            c0_norm = c0 / sub_norm
            c1_norm = c1 / sub_norm
        else:
            c0_norm, c1_norm = 1.0, 0.0

        rx = 2.0 * np.real(c0_norm * np.conj(c1_norm))
        ry = 2.0 * np.imag(c1_norm * np.conj(c0_norm))
        rz = float(np.abs(c0_norm)**2 - np.abs(c1_norm)**2)

        coords[i] = [rx, ry, rz]

    return coords[0] if single else coords


if __name__ == "__main__":
    sample_nodes = np.array([
        [10.0, 20.0, 95.0, 1.0, 15.0],
        [80.0, 85.0, 45.0, 0.4, 70.0],
        [45.0, 50.0, 80.0, 0.9, 2.0],
    ])
    psi = quantum_state_embedding(sample_nodes)
    print("Embedded Quantum Statevectors shape:", psi.shape)
    print("State 0 L2 Norm:", np.linalg.norm(psi[0]))
    f = quantum_state_fidelity(psi[0], psi[1])
    print(f"Fidelity between Node 0 and Node 1: {f:.5f}")
    bloch = bloch_sphere_coordinates(psi)
    print("Bloch Sphere Coordinates (x,y,z):\n", bloch)
