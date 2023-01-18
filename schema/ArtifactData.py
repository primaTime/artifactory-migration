from typing import TypedDict


class ArtifactData(TypedDict):
    pom: str
    sources: str
    javadoc: str
    jar: str
    jar_with_dependencies: str
    war: str