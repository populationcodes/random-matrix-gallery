import os
import __main__ as main
import typing

import numpy as np
import scipy


def init_randomness(seed=1):
    np.random.seed(seed)


def get_script_name() -> typing.Union[str, None]:
    try:
        file = main.__file__
    except AttributeError:
        try:
            file = main.__vsc_ipynb_file__
        except AttributeError:
            return None
    return os.path.splitext(os.path.basename(file))[0]


def sample_correlated(N, Mu, Sigma):
    w = np.random.multivariate_normal(Mu, Sigma, int(N*(N-1)/2))
    assert np.all(w.shape == (int(N*(N-1)/2), 2))

    X = np.zeros((N, N))
    c = 0
    for i in range(N):
        for j in range(N):
            if i >= j:
                continue
            X[i, j] = w[c, 0]
            X[j, i] = w[c, 1]
            c += 1
    assert c == int(N*(N-1)/2)
    return X


def sample_2d_real(N, P, tau, mu=np.array([0, 0])):
    s1 = np.random.rand()*2
    s2 = np.random.rand()*2
    covs = np.array([[s1**2/N, s1*s2*tau/N], [s1*s2*tau/N, s2**2/N]])
    V = np.random.multivariate_normal(mu, covs, N*P).astype('complex')
    return V


def sample_2d_indepeddent_complex(N, P, tau, mu=np.array([0, 0])):
    s1 = np.random.rand()*2
    s2 = np.random.rand()*2
    covs1 = np.array([[s1**2/N, s1*s2*tau/N], [s1*s2*tau/N, s2**2/N]])
    s1 = np.random.rand()*2
    s2 = np.random.rand()*2
    covs2 = np.array([[s1**2/N, s1*s2*tau/N], [s1*s2*tau/N, s2**2/N]])
    Vr = np.random.multivariate_normal(mu, covs1, N*P)
    Vi = np.random.multivariate_normal(mu, covs2, N*P)
    covs = covs1 + covs2
    V = Vr + 1j*Vi
    return V, covs


def sample_2d_complex(N, P, mu=np.zeros(4)):
    assert len(mu) == 4
    eigs = np.random.rand(4)
    eigs *= 4/np.sum(eigs)
    C = scipy.stats.random_correlation.rvs(eigs)/N
    v = np.random.multivariate_normal(mu, C, N*P)
    assert v.shape == (N*P, 4)
    V = v[:, :2] + 1j*v[:, 2:]
    return V
