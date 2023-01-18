from typing import TypedDict


class ArtifactData(TypedDict):
    pom: str
    sources: str
    javadoc: str
    jar: str
    war: str