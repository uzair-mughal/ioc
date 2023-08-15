import os
import yaml
from typing import List
from ioc.src import Scope
from ioc.src import Container


def build(file_paths: List[str], container=Container()) -> Container:
    # Reads list of yml files then build dependencies as specified in the files.

    for file_path in file_paths:
        with open(file_path) as file:
            results = yaml.load(file, Loader=yaml.FullLoader)

            for key, value in results.get("parameters", {}).items():
                if (
                    isinstance(value, str)
                    and value.startswith("${")
                    and value.endswith("}")
                ):
                    value = os.getenv(value[2:-1])

                container.add(name=key, scope=Scope.SINGLETON, value=value)

            for key, value in results.get("services", {}).items():
                module_path = value.get("class")
                scope = value.get("scope", Scope.SINGLETON)
                construct = value.get("construct", True)
                kwargs = value.get("kwargs", {})

                container.add(
                    name=key,
                    scope=scope,
                    module_path=module_path,
                    construct=construct,
                    kwargs=kwargs,
                )

    return container
