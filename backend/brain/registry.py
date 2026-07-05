from typing import Dict, Any

class ServiceRegistry:
    """
    Subsystem catalog registering instantiated service classes for all modules.
    """

    def __init__(self):
        self._services: Dict[str, Any] = {}

    def register_service(self, name: str, service: Any) -> None:
        """Add a service instance to the catalog registry."""
        self._services[name] = service

    def get_service(self, name: str) -> Any:
        """Fetch a registered service instance by name."""
        return self._services.get(name)
