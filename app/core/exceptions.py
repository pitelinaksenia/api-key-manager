class AppError(Exception):
    pass


class NotFoundError(AppError):
    pass


class AlreadyExistsError(AppError):
    pass


class InvalidStateError(AppError):
    pass


class AuthenticationError(AppError):
    pass


class ClientNotFoundError(NotFoundError):
    def __init__(self, client_id):
        self.client_id = client_id
        super().__init__(f"Client {client_id} not found")


class ClientAlreadyExistsError(AlreadyExistsError):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Client with email {email} already exists")


class ScopeNotFoundError(NotFoundError):
    def __init__(self, identifier):
        super().__init__(f"Scope(s) not found: {identifier}")


class ScopeAlreadyExistsError(AlreadyExistsError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(f"Scope with code '{code}' already exists")


class ClientNotActiveError(InvalidStateError):
    def __init__(self, client_id):
        self.client_id = client_id
        super().__init__(f"Client {client_id} is not active")


class APIKeyNotFoundError(NotFoundError):
    def __init__(self, key_id):
        self.key_id = key_id
        super().__init__(f"API key {key_id} not found")


class APIKeyInvalidError(AuthenticationError):
    def __init__(self):
        super().__init__("Invalid API key")


class APIKeyAlreadyRevokedError(InvalidStateError):
    def __init__(self, key_id):
        self.key_id = key_id
        super().__init__(f"API key {key_id} was already revoked")
