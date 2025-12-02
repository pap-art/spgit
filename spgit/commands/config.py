"""config command implementation"""

import json
from pathlib import Path
from ..core.repository import find_repository
from ..utils.colors import success, error, info


def config_command(args):
    """Configure spgit settings."""
    try:
        # Determine if we're setting global or local config
        is_global = hasattr(args, 'global_config') and args.global_config

        if is_global:
            # Global config in ~/.spgit/config
            config_dir = Path.home() / ".spgit"
            config_dir.mkdir(parents=True, exist_ok=True)
            config_path = config_dir / "config"

            if config_path.exists():
                with open(config_path, "r") as f:
                    config = json.load(f)
            else:
                config = {}
        else:
            # Local config in repository
            repo = find_repository()
            if not repo:
                print(error("Fatal: not a spgit repository"))
                return 1
            config = repo.read_config()
            config_path = repo.config_path

        # Handle different config operations
        if hasattr(args, 'list') and args.list:
            # List all configuration
            _print_config(config)
            return 0

        if hasattr(args, 'get') and args.get:
            # Get a specific value
            value = _get_config_value(config, args.get)
            if value is not None:
                print(value)
                return 0
            else:
                print(error(f"Configuration key '{args.get}' not found"))
                return 1

        if hasattr(args, 'set') and args.set:
            # Set a value
            key, value = args.set
            _set_config_value(config, key, value)

            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)

            print(success(f"Set {key} = {value}"))
            return 0

        if hasattr(args, 'unset') and args.unset:
            # Unset a value
            if _unset_config_value(config, args.unset):
                with open(config_path, "w") as f:
                    json.dump(config, f, indent=2)
                print(success(f"Unset {args.unset}"))
            else:
                print(error(f"Configuration key '{args.unset}' not found"))
                return 1
            return 0

        # Interactive setup
        print(info("Spotify API Configuration"))
        print("You need to create a Spotify app at https://developer.spotify.com/dashboard")
        print()

        client_id = input("Enter your Spotify Client ID: ").strip()
        client_secret = input("Enter your Spotify Client Secret: ").strip()

        if not client_id or not client_secret:
            print(error("Both Client ID and Client Secret are required"))
            return 1

        config.setdefault("spotify", {})
        config["spotify"]["client_id"] = client_id
        config["spotify"]["client_secret"] = client_secret

        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        print(success("Configuration saved successfully"))
        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        return 1


def _print_config(config, prefix=""):
    """Print configuration recursively."""
    for key, value in config.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            _print_config(value, full_key)
        else:
            print(f"{full_key}={value}")


def _get_config_value(config, key):
    """Get a configuration value by dotted key."""
    parts = key.split(".")
    current = config

    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None

    return current


def _set_config_value(config, key, value):
    """Set a configuration value by dotted key."""
    parts = key.split(".")
    current = config

    for part in parts[:-1]:
        if part not in current:
            current[part] = {}
        current = current[part]

    current[parts[-1]] = value


def _unset_config_value(config, key):
    """Unset a configuration value by dotted key."""
    parts = key.split(".")
    current = config

    for part in parts[:-1]:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return False

    if parts[-1] in current:
        del current[parts[-1]]
        return True

    return False
