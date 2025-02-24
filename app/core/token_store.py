class TokenStore:
    _instance = None
    _token = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TokenStore, cls).__new__(cls)
        return cls._instance

    @classmethod
    def set_token(cls, token):
        cls._token = token

    @classmethod
    def get_token(cls):
        return cls._token

token_store = TokenStore() 