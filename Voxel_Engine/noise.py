from numba import njit
from opensimplex.internals import _noise2, _noise3, _init

from Voxel_Engine.engine_settings import SEED


perm, perm_grad_index3 = _init(seed=SEED)


@njit(cache=True)
def noise2(x, y):
    return _noise2(x, y, perm)


@njit(cache=True)
def noise3(x, y, z):
    return _noise3(x, y, z, perm, perm_grad_index3)
