# Copyright (c) 2022, NVIDIA CORPORATION.
#
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

import argparse
from pathlib import Path

from cugraph_service_client import defaults
from cugraph_service_client.cugraph_service_thrift import create_server
from cugraph_service_server.cugraph_handler import CugraphHandler


def create_handler(graph_creation_extension_dir=None,
                   dask_scheduler_file=None):
    """
    Create and return a CugraphHandler instance initialized with
    options. Setting graph_creation_extension_dir to a valid dir results in the
    handler loading graph creation extensions from that dir.
    """
    handler = CugraphHandler()
    if graph_creation_extension_dir is not None:
        handler.load_graph_creation_extensions(graph_creation_extension_dir)
    if dask_scheduler_file is not None:
        # FIXME: if initialize_dask_client(None) is called, it creates a
        # LocalCUDACluster. Add support for this via a different CLI option?
        handler.initialize_dask_client(dask_scheduler_file)
    return handler


def start_server_blocking(handler, host, port):
    """
    Start the cugraph_service server on host/port, using handler as the request
    handler instance. This call blocks indefinitely until Ctrl-C.
    """
    server = create_server(handler, host=host, port=port)
    server.serve()  # blocks until Ctrl-C (kill -2)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--host",
                            type=str,
                            default=defaults.host,
                            help="hostname the server should use, default is "
                            f"{defaults.host}")
    arg_parser.add_argument("--port",
                            type=int,
                            default=defaults.port,
                            help="port the server should listen on, default "
                            f"is {defaults.port}")
    arg_parser.add_argument("--graph-creation-extension-dir",
                            type=Path,
                            help="dir to load graph creation extension "
                            "functions from")
    arg_parser.add_argument("--dask-scheduler-file",
                            type=Path,
                            help="file generated by a dask scheduler, used "
                            "for connecting to a dask cluster for MG support")
    args = arg_parser.parse_args()
    handler = create_handler(args.graph_creation_extension_dir,
                             args.dask_scheduler_file)
    print("Starting the cugraph_service server...", flush=True)
    start_server_blocking(handler, args.host, args.port)
    print("done.")
