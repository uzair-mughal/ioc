from pydoc import locate
from ioc.src.scope import Scope
from ioc.src.exceptions.invalid_dependency_error import InvalidDependencyError


class Container:
    def __init__(self):
        self._services = {}

    def add(
        self,
        name: str,
        scope: str = Scope.SINGLETON,
        value=None,
        module_path=None,
        construct: bool = True,
        kwargs: dict = {},
    ):
        if scope == Scope.SINGLETON and value is None:
            args = {}

            for k, v in kwargs.items():
                if isinstance(v, int):
                    resolved_value = v
                    args[k] = resolved_value

                if isinstance(v, str):
                    resolved_value = v

                    if v[0] == "@":
                        resolved_value = self.get(v[1:])

                    args[k] = resolved_value

                if isinstance(v, list):
                    values = []
                    for val in v:
                        resolved_value = val

                        if isinstance(val[0], str) and val[0] == "@":
                            resolved_value = self.get(val[1:])

                        values.append(resolved_value)

                    args[k] = values

                if isinstance(v, dict):
                    values = {}
                    for key, val in v.items():
                        resolved_value = val

                        if isinstance(val, str) and val[0] == "@":
                            resolved_value = self.get(val[1:])

                        values.update({key: resolved_value})

                    args[k] = values

            try:
                if construct:
                    value = locate(module_path)(**args)
                else:
                    value = locate(module_path)
            except TypeError:
                raise Exception(f"Path {module_path} not resolved.")
            except Exception as e:
                raise e

        self._services[name] = {
            "value": value,
            "scope": scope,
            "module_path": module_path,
            "construct": construct,
            "kwargs": kwargs,
        }

    def get(self, name: str):
        service = self._services.get(name, None)

        if service is not None:
            if service.get("scope") == Scope.SINGLETON:
                return service.get("value")

            elif service.get("scope") == Scope.TRANSIENT:
                args = {}

                for k, v in service.get("kwargs").items():
                    if isinstance(v, str):
                        resolved_value = v

                        if v[0] == "@":
                            resolved_value = self.get(v[1:])

                        args[k] = resolved_value

                    if isinstance(v, list):
                        values = []
                        for val in v:
                            resolved_value = val

                            if isinstance(val[0], str) and val[0] == "@":
                                resolved_value = self.get(val[1:])

                            values.append(resolved_value)

                        args[k] = values

                try:
                    if service.get("construct"):
                        return locate(service.get("module_path"))(**args)
                    else:
                        return locate(service.get("module_path"))
                except Exception as e:
                    raise InvalidDependencyError(service.get("module_path"))

        return None
