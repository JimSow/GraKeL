# This test case was found to be inconsistent when running on github action runners
# However the `test_lovasz` tests seem to pass locally. The test body comes from
# `LovaszTheta.parse_input` and is a minimal example which causes those tests to fail.
#
#   To enable the test, change `DISABLED` to False
#
# This test is here in case debugging is required in the future.
import pytest

DISABLED = True
cvxopt = True
try:
    import cvxopt
except ImportError:
    cvxopt = False

@pytest.mark.skipif(DISABLED or not cvxopt, reason="Skipping debugging test")
@pytest.mark.parametrize(
    "nv, ne, e_list, x_list",
    [
        (
            9,
            15,
            [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11,
                12, 12, 13, 13, 14, 14, 15, 15, 15, 15, 15, 15, 15, 15, 15],
            [2, 2, 3, 3, 6, 6, 7, 7, 12, 12, 14, 14, 15, 15, 21, 21, 22, 22, 23, 23, 25,
                25, 41, 41, 44, 44, 53, 53, 71, 71, 0, 10, 20, 30, 40, 50, 60, 70, 80],
        )
    ],
)
def test_windows_sdp(nv, ne, e_list, x_list) -> None:
    # initialise g sparse (to values -1, based on two list that
    # define index and one that defines shape
    from cvxopt.base import matrix, spmatrix
    from cvxopt.solvers import sdp

    print(nv, ne, e_list, x_list)
    g_sparse = spmatrix(-1, x_list, e_list, (nv * nv, ne + 1))

    # Initialise optimization parameters
    h = matrix(-1.0, (nv, nv))
    c = matrix([0.0] * ne + [1.0])

    # Solve the convex optimization problem
    # Should raise here on windows
    sol = sdp(c, Gs=[g_sparse], hs=[h])
    assert sol is not None
