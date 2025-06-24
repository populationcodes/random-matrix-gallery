import os
import __main__ as main
import typing
import numpy as np


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
