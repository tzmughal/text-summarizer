import json
import os


class ConfigManager:
    """
    Loads and provides access to application configuration.
    """

    def __init__(self, config_path="config.json"):

        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Configuration file '{config_path}' not found."
            )

        with open(config_path, "r", encoding="utf-8") as file:
            self.config = json.load(file)

    def get(self, key, default=None):
        """
        Retrieve a configuration value.

        Parameters:
            key (str): Configuration key.
            default: Value returned if the key is not found.

        Returns:
            The configuration value or the default.
        """
        return self.config.get(key, default)