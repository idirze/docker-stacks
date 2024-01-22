# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from dataclasses import dataclass, field
from typing import Optional

from tagging.manifests import (
    AptPackagesManifest,
    CondaEnvironmentManifest,
    JuliaPackagesManifest,
    ManifestInterface,
    RPackagesManifest,
    SparkInfoManifest,
)
from tagging.taggers import (
    DateTagger,
    JavaVersionTagger,
    JuliaVersionTagger,
    JupyterHubVersionTagger,
    JupyterLabVersionTagger,
    JupyterNotebookVersionTagger,
    PythonMajorMinorVersionTagger,
    PythonVersionTagger,
    PytorchVersionTagger,
    RVersionTagger,
    SHATagger,
    SparkVersionTagger,
    TaggerInterface,
    TensorflowVersionTagger,
    UbuntuVersionTagger,
    ScalaVersionTagger,
    LongTagger,
)


@dataclass
class ImageDescription:
    parent_image: Optional[str]
    taggers: list[TaggerInterface] = field(default_factory=list)
    manifests: list[ManifestInterface] = field(default_factory=list)


ALL_IMAGES = {
    "docker-stacks-foundation": ImageDescription(
        parent_image=None,
        taggers=[
            SHATagger(),
            DateTagger(),
            UbuntuVersionTagger(),
            PythonMajorMinorVersionTagger(),
            PythonVersionTagger(),
            LongTagger(PythonVersionTagger(), DateTagger()),
        ],
        manifests=[CondaEnvironmentManifest(), AptPackagesManifest()],
    ),
    "base-notebook": ImageDescription(
        parent_image="docker-stacks-foundation",
        taggers=[
            JupyterNotebookVersionTagger(),
            JupyterLabVersionTagger(),
            JupyterHubVersionTagger(),
            LongTagger(PythonVersionTagger(), JupyterHubVersionTagger(), JupyterLabVersionTagger()),
            LongTagger(PythonVersionTagger(), JupyterHubVersionTagger(), JupyterLabVersionTagger(), DateTagger()),
        ],
    ),
    "minimal-notebook": ImageDescription(parent_image="base-notebook"),
    "scipy-notebook": ImageDescription(parent_image="minimal-notebook"),
    "r-notebook": ImageDescription(
        parent_image="minimal-notebook",
        taggers=[
            RVersionTagger(),
            LongTagger(PythonVersionTagger(), RVersionTagger(), JupyterHubVersionTagger(), JupyterLabVersionTagger()),
            LongTagger(PythonVersionTagger(), RVersionTagger(), JupyterHubVersionTagger(), JupyterLabVersionTagger(), DateTagger()),
        ],
        manifests=[RPackagesManifest()],
    ),
    "julia-notebook": ImageDescription(
        parent_image="minimal-notebook",
        taggers=[
            JuliaVersionTagger(),
            LongTagger(PythonVersionTagger(), JuliaVersionTagger(), JupyterHubVersionTagger(), JupyterLabVersionTagger()),
            LongTagger(PythonVersionTagger(), JuliaVersionTagger(), JupyterHubVersionTagger(), JupyterLabVersionTagger(), DateTagger()),
        ],
        manifests=[JuliaPackagesManifest()],
    ),
    "tensorflow-notebook": ImageDescription(
        parent_image="scipy-notebook", 
        taggers=[
            TensorflowVersionTagger(),
            LongTagger(PythonVersionTagger(), TensorflowVersionTagger(), JupyterHubVersionTagger(), JupyterLabVersionTagger()),
            LongTagger(PythonVersionTagger(), TensorflowVersionTagger(), JupyterHubVersionTagger(), JupyterLabVersionTagger(), DateTagger()),
        ]
    ),
    "pytorch-notebook": ImageDescription(
        parent_image="scipy-notebook", 
        taggers=[
            PytorchVersionTagger(),
            LongTagger(PythonVersionTagger(), PytorchVersionTagger(), JupyterHubVersionTagger(), JupyterLabVersionTagger()),
            LongTagger(PythonVersionTagger(), PytorchVersionTagger(), JupyterHubVersionTagger(), JupyterLabVersionTagger(), DateTagger()),
        ]
    ),
    "datascience-notebook": ImageDescription(
        parent_image="scipy-notebook",
        taggers=[
            RVersionTagger(), 
            JuliaVersionTagger(),
            LongTagger(PythonVersionTagger(), RVersionTagger(), JuliaVersionTagger(), JupyterHubVersionTagger(), JupyterLabVersionTagger()),
            LongTagger(PythonVersionTagger(), RVersionTagger(), JuliaVersionTagger(), JupyterHubVersionTagger(), JupyterLabVersionTagger(), DateTagger()),
        ],
        manifests=[RPackagesManifest(), JuliaPackagesManifest()],
    ),
    "pyspark-notebook": ImageDescription(
        parent_image="scipy-notebook",
        taggers=[
            SparkVersionTagger(), 
            JavaVersionTagger(),
            ScalaVersionTagger(),
            LongTagger(SparkVersionTagger(), PythonVersionTagger(), JavaVersionTagger(), ScalaVersionTagger(), JupyterHubVersionTagger(), JupyterLabVersionTagger()),
            LongTagger(SparkVersionTagger(), PythonVersionTagger(), JavaVersionTagger(), ScalaVersionTagger(), JupyterHubVersionTagger(), JupyterLabVersionTagger(), DateTagger()),
        ],
        manifests=[SparkInfoManifest()],
    ),
    "all-spark-notebook": ImageDescription(
        parent_image="pyspark-notebook",
        taggers=[
            RVersionTagger(),
            ScalaVersionTagger(),
            LongTagger(SparkVersionTagger(), PythonVersionTagger(), RVersionTagger(), JavaVersionTagger(), ScalaVersionTagger(), JupyterHubVersionTagger(), JupyterLabVersionTagger()),
            LongTagger(SparkVersionTagger(), PythonVersionTagger(), RVersionTagger(), JavaVersionTagger(), ScalaVersionTagger(), JupyterHubVersionTagger(), JupyterLabVersionTagger(), DateTagger()),
        ],
        manifests=[RPackagesManifest()],
    ),
}
