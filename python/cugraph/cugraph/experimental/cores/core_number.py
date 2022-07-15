# Copyright (c) 2019-2022, NVIDIA CORPORATION.
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

from cugraph.utilities import ensure_cugraph_obj_for_nx
import cudf

from pylibcugraph.experimental import core_number as \
    pylibcugraph_core_number

from pylibcugraph import (ResourceHandle,
                          GraphProperties,
                          SGGraph
                          )


def EXPERIMENTAL__core_number(G, degree_type=0):
    """
    Compute the core numbers for the nodes of the graph G. A k-core of a graph
    is a maximal subgraph that contains nodes of degree k or more.
    A node has a core number of k if it belongs a k-core but not to k+1-core.
    This call does not support a graph with self-loops and parallel
    edges.

    Parameters
    ----------
    G : cuGraph.Graph or networkx.Graph
        The graph should contain undirected edges where undirected edges are
        represented as directed edges in both directions. While this graph
        can contain edge weights, they don't participate in the calculation
        of the core numbers.
    
    degree_type: int, optional (default=0) 
        Flag determining whether the core number computation should be based
        of incoming edges, outgoing edges or both which are respectively
        0, 1 and 2

    Returns
    -------
    df : cudf.DataFrame or python dictionary (in NetworkX input)
        GPU data frame containing two cudf.Series of size V: the vertex
        identifiers and the corresponding core number values.

        df['vertex'] : cudf.Series
            Contains the vertex identifiers
        df['core_number'] : cudf.Series
            Contains the core number of vertices

    Examples
    --------
    >>> gdf = cudf.read_csv(datasets_path / 'karate.csv', delimiter=' ',
    ...                     dtype=['int32', 'int32', 'float32'], header=None)
    >>> G = cugraph.Graph()
    >>> G.from_cudf_edgelist(gdf, source='0', destination='1')
    >>> df = cugraph.core_number(G)

    """

    G, _ = ensure_cugraph_obj_for_nx(G)

    if G.is_directed():
        raise ValueError("input graph must be undirected")

    if degree_type not in [0, 1, 2]:
        raise ValueError(f"degree_type must be either 0, 1 and 2 which "
                         f"represent respectively incoming edge, outgoing "
                         f"or both")

    srcs = G.edgelist.edgelist_df['src']
    dsts = G.edgelist.edgelist_df['dst']
    weights = G.edgelist.edgelist_df['weights']

    if srcs.dtype != 'int32':
        raise ValueError(f"Graph vertices must have int32 values, "
                         f"got: {srcs.dtype}")

    resource_handle = ResourceHandle()
    graph_props = GraphProperties(
        is_symmetric=True, is_multigraph=G.is_multigraph())
    store_transposed = False

    # FIXME:  This should be based on the renumber parameter set when creating
    # the graph
    renumber = False
    do_expensive_check = False

    sg = SGGraph(resource_handle, graph_props, srcs, dsts, weights,
                 store_transposed, renumber, do_expensive_check)

    vertex, core_number = pylibcugraph_core_number(
        resource_handle, sg, degree_type, do_expensive_check)

    df = cudf.DataFrame()
    df["vertex"] = vertex
    df["core_number"] = core_number

    if G.renumbered:
        df = G.unrenumber(df, "vertex")

    return df
