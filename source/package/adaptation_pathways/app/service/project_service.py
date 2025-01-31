import base64

import jsonpickle

from ..model.pathways_project import PathwaysProject


class ProjectService:
    @staticmethod
    def to_json(project: PathwaysProject) -> str:
        text: str = jsonpickle.encode(project)
        return text

    @staticmethod
    def from_json(project_json: str) -> PathwaysProject:
        project = jsonpickle.decode(project_json)
        return project

    @staticmethod
    def to_data_url(project: PathwaysProject) -> str:
        text = ProjectService.to_json(project)
        text_bytes = text.encode("utf-8")
        text_64_bytes = base64.b64encode(text_bytes)
        text_64_str = text_64_bytes.decode("utf-8")
        return f"data:text/plain;base64,{text_64_str}"
