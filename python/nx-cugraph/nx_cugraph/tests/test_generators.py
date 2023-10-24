# Copyright (c) 2023, NVIDIA CORPORATION.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import networkx as nx
import pytest

import nx_cugraph as nxcg


def assert_graphs_equal(Gnx, Gcg):
    assert Gnx.number_of_nodes() == Gcg.number_of_nodes()
    assert Gnx.number_of_edges() == Gcg.number_of_edges()
    assert Gnx.is_directed() == Gcg.is_directed()
    assert Gnx.is_multigraph() == Gcg.is_multigraph()
    G = nxcg.to_networkx(Gcg)
    rv = nx.utils.graphs_equal(G, Gnx)
    if not rv:
        print("GRAPHS ARE NOT EQUAL!")
        assert sorted(G) == sorted(Gnx)
        assert sorted(G._adj) == sorted(Gnx._adj)
        assert sorted(G._node) == sorted(Gnx._node)
        for k in sorted(G._adj):
            print(k, sorted(G._adj[k]), sorted(Gnx._adj[k]))
        print(nx.to_scipy_sparse_array(G).todense())
        print(nx.to_scipy_sparse_array(Gnx).todense())
    assert rv


def compare(name, create_using, *args, is_vanilla=False):
    exc1 = exc2 = None
    func = getattr(nx, name)
    if isinstance(create_using, nxcg.Graph):
        nx_create_using = nxcg.to_networkx(create_using)
    elif isinstance(create_using, type) and issubclass(create_using, nxcg.Graph):
        nx_create_using = create_using.to_networkx_class()
    else:
        nx_create_using = create_using
    try:
        if is_vanilla:
            G = func(*args)
        else:
            G = func(*args, create_using=nx_create_using)
    except Exception as exc:
        exc1 = exc
    try:
        if is_vanilla:
            Gcg = func(*args, backend="cugraph")
        else:
            Gcg = func(*args, create_using=create_using, backend="cugraph")
    except ZeroDivisionError:
        raise
    except Exception as exc:
        if exc1 is None:  # pragma: no cover (debug)
            raise
        exc2 = exc
    if exc1 is not None or exc2 is not None:
        assert type(exc1) is type(exc2)
    else:
        assert_graphs_equal(G, Gcg)


N = list(range(-1, 5))
CREATE_USING = [nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph]
COMPLETE_CREATE_USING = [
    nx.Graph,
    nx.DiGraph,
    nx.MultiGraph,
    nx.MultiDiGraph,
    nxcg.Graph,
    nxcg.DiGraph,
    nxcg.MultiGraph,
    nxcg.MultiDiGraph,
    nx.Graph(),
    nx.DiGraph(),
    nx.MultiGraph(),
    nx.MultiDiGraph(),
    nxcg.Graph(),
    nxcg.DiGraph(),
    nxcg.MultiGraph(),
    nxcg.MultiDiGraph(),
    None,
    object,  # Bad input
    7,  # Bad input
]
GENERATORS_NOARG = [
    # classic
    "null_graph",
    "trivial_graph",
]
GENERATORS_NOARG_VANILLA = [
    # classic
    "karate_club_graph",
]
GENERATORS_N = [
    # classic
    "circular_ladder_graph",
    "complete_graph",
    "cycle_graph",
    "empty_graph",
    "ladder_graph",
    "path_graph",
    "star_graph",
    "wheel_graph",
]
GENERATORS_M_N = [
    # classic
    "barbell_graph",
    "lollipop_graph",
]
GENERATORS_M_N_VANILLA = [
    # community
    "caveman_graph",
]


@pytest.mark.parametrize("name", GENERATORS_NOARG)
@pytest.mark.parametrize("create_using", COMPLETE_CREATE_USING)
def test_generator_noarg(name, create_using):
    print(name, create_using)
    compare(name, create_using)


@pytest.mark.parametrize("name", GENERATORS_NOARG_VANILLA)
def test_generator_noarg_vanilla(name):
    print(name)
    compare(name, None, is_vanilla=True)


@pytest.mark.parametrize("name", GENERATORS_N)
@pytest.mark.parametrize("n", N)
@pytest.mark.parametrize("create_using", CREATE_USING)
def test_generator_n(name, n, create_using):
    print(name, n, create_using)
    compare(name, create_using, n)


@pytest.mark.parametrize("name", GENERATORS_N)
@pytest.mark.parametrize("n", [1, 4])
@pytest.mark.parametrize("create_using", COMPLETE_CREATE_USING)
def test_generator_n_complete(name, n, create_using):
    print(name, n, create_using)
    compare(name, create_using, n)


@pytest.mark.parametrize("name", GENERATORS_M_N)
@pytest.mark.parametrize("create_using", CREATE_USING)
@pytest.mark.parametrize("m", N)
@pytest.mark.parametrize("n", N)
def test_generator_m_n(name, create_using, m, n):
    print(name, m, n, create_using)
    compare(name, create_using, m, n)


@pytest.mark.parametrize("name", GENERATORS_M_N_VANILLA)
@pytest.mark.parametrize("m", N)
@pytest.mark.parametrize("n", N)
def test_generator_m_n_vanilla(name, m, n):
    print(name, m, n)
    compare(name, None, m, n, is_vanilla=True)


@pytest.mark.parametrize("name", GENERATORS_M_N)
@pytest.mark.parametrize("create_using", COMPLETE_CREATE_USING)
@pytest.mark.parametrize("m", [4])
@pytest.mark.parametrize("n", [4])
def test_generator_m_n_complete(name, create_using, m, n):
    print(name, m, n, create_using)
    compare(name, create_using, m, n)


@pytest.mark.parametrize("name", GENERATORS_M_N_VANILLA)
@pytest.mark.parametrize("m", [4])
@pytest.mark.parametrize("n", [4])
def test_generator_m_n_complete_vanilla(name, m, n):
    print(name, m, n)
    compare(name, None, m, n, is_vanilla=True)


def test_bad_lollipop_graph():
    compare("lollipop_graph", None, [0, 1], [1, 2])
