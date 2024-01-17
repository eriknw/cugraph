# Copyright (c) 2022-2024, NVIDIA CORPORATION.
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

from cugraph.utilities.api_tools import experimental_warning_wrapper
from cugraph.utilities.api_tools import deprecated_warning_wrapper
from cugraph.utilities.api_tools import promoted_experimental_warning_wrapper

from cugraph.structure.property_graph import EXPERIMENTAL__PropertyGraph

PropertyGraph = experimental_warning_wrapper(EXPERIMENTAL__PropertyGraph)

from cugraph.structure.property_graph import EXPERIMENTAL__PropertySelection

PropertySelection = experimental_warning_wrapper(EXPERIMENTAL__PropertySelection)

from cugraph.dask.structure.mg_property_graph import EXPERIMENTAL__MGPropertyGraph

MGPropertyGraph = experimental_warning_wrapper(EXPERIMENTAL__MGPropertyGraph)

from cugraph.dask.structure.mg_property_graph import EXPERIMENTAL__MGPropertySelection

MGPropertySelection = experimental_warning_wrapper(EXPERIMENTAL__MGPropertySelection)

# FIXME: Remove experimental.triangle_count next release
from cugraph.community.triangle_count import triangle_count

triangle_count = promoted_experimental_warning_wrapper(triangle_count)

from cugraph.experimental.components.scc import EXPERIMENTAL__strong_connected_component

strong_connected_component = experimental_warning_wrapper(
    EXPERIMENTAL__strong_connected_component
)

from cugraph.experimental.structure.bicliques import EXPERIMENTAL__find_bicliques

find_bicliques = deprecated_warning_wrapper(
    experimental_warning_wrapper(EXPERIMENTAL__find_bicliques)
)

from cugraph.gnn.data_loading import BulkSampler

BulkSampler = promoted_experimental_warning_wrapper(BulkSampler)


from cugraph.link_prediction.jaccard import jaccard, jaccard_coefficient

jaccard = promoted_experimental_warning_wrapper(jaccard)
jaccard_coefficient = promoted_experimental_warning_wrapper(jaccard_coefficient)

from cugraph.link_prediction.sorensen import sorensen, sorensen_coefficient

sorensen = promoted_experimental_warning_wrapper(sorensen)
sorensen_coefficient = promoted_experimental_warning_wrapper(sorensen_coefficient)

from cugraph.link_prediction.overlap import overlap, overlap_coefficient

overlap = promoted_experimental_warning_wrapper(overlap)
overlap_coefficient = promoted_experimental_warning_wrapper(overlap_coefficient)
