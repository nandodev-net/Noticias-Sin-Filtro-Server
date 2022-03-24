"""
    Define how versions from the client are managed, telling the client if their
    current version are valid or not.
"""

# Local imports
from typing import List
from noticias_sin_filtro_server.settings import (
    LAST_VERSION,
    COMPATIBLE_UPGRADABLE,
    DEPRECATED_VERSIONS,
)

# Python imports
import enum


class Compatibility(enum.Enum):
    """
    Possible compatibility variations
        - not_compatible: can't provide service to this version
        - upgradable_compatible: can provide service to this version, and there's an available update
        - last_version: Client is currently in the last available version, so it's compatible.
    """

    NOT_COMPATIBLE = "not_compatible"
    UPGRADABLE_COMPATIBLE = "upgradable_compatible"
    LAST_VERSION = "last_version"


class Platforms(enum.Enum):
    """
    Supported platforms
    """

    ANDROID = "android"
    IOS = "ios"

    @classmethod
    def values(cls) -> List[str]:
        """
        All posible values
        """
        return [x.value for x in cls]


class KillSwtich:
    """
    This class will process the client version to
    specify if it's a valid one
    """

    @staticmethod
    def compatibility(version: str, platform: str) -> Compatibility:
        """
        Tells if the provided version for the given platform is
        compatible with the current server version

        # Parameters
            - version : `str` = version string in format vX.Y.Z. Should be a valid version or will raise value error otherwise.
            - platform : `str` = client's platform, should be a member of the `Platforms` enum.
        # Returns
            Type of compatibility according to the rules of compatibility
        """

        # Check if this is a valid version
        if (
            version != LAST_VERSION
            and version not in COMPATIBLE_UPGRADABLE
            and version not in DEPRECATED_VERSIONS
        ):
            raise ValueError(f"Invalid version: {version}")

        # Check if this is a valid platform
        if platform not in Platforms.values():
            raise ValueError(
                f"Invalid platform: {platform}. Possible platforms: {', '.join(Platforms.values())}"
            )

        # Check compatibility
        if version == LAST_VERSION:
            return Compatibility.LAST_VERSION
        elif version in COMPATIBLE_UPGRADABLE:
            return Compatibility.UPGRADABLE_COMPATIBLE
        else:
            return Compatibility.NOT_COMPATIBLE
