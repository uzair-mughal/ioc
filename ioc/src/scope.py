class Scope:
    # Singleton object will be used through out the application's life cycle
    SINGLETON = "singleton"

    # Transient scope will allow the object to be recreated whenever its requested
    TRANSIENT = "transient"