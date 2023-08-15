class InvalidDependencyError(Exception):
    def __init__(self, dependency_path: str):
        message = f'Error resolving dependency at path {dependency_path}.'
        super().__init__(message)