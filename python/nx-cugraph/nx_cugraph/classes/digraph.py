# Copyright (c) 2023-2024, NVIDIA CORPORATION.
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
from __future__ import annotations

from typing import TYPE_CHECKING

import cupy as cp
import networkx as nx
import numpy as np

import nx_cugraph as nxcg

from .graph import Graph

if TYPE_CHECKING:  # pragma: no cover
    from nx_cugraph.typing import AttrKey

__all__ = ["DiGraph"]

networkx_api = nxcg.utils.decorators.networkx_class(nx.DiGraph)


class DiGraph(Graph):
    #################
    # Class methods #
    #################

    @classmethod
    @networkx_api
    def is_directed(cls) -> bool:
        return True

    @classmethod
    def to_networkx_class(cls) -> type[nx.DiGraph]:
        return nx.DiGraph

    @networkx_api
    def size(self, weight: AttrKey | None = None) -> int:
        if weight is not None:
            raise NotImplementedError
        return self.src_indices.size

    ##########################
    # NetworkX graph methods #
    ##########################

    @networkx_api
    def reverse(self, copy: bool = True) -> DiGraph:
        return self._copy(not copy, self.__class__, reverse=True)

    # Many more methods to implement...

    ###################
    # Private methods #
    ###################

    def _in_degrees_array(self):
        if self.dst_indices.size == 0:
            return cp.zeros(self._N, dtype=np.int64)
        return cp.bincount(self.dst_indices, minlength=self._N)

    def _out_degrees_array(self):
        if self.src_indices.size == 0:
            return cp.zeros(self._N, dtype=np.int64)
        return cp.bincount(self.src_indices, minlength=self._N)
