import sys
from plugins.vps.cli_plugin import VPSCLIPlugin
from plugins.ip_security.cli_plugin import IPSecurityCLIPlugin


_cli_plugins = [
    VPSCLIPlugin(),
    IPSecurityCLIPlugin(),
]


def main():
    if len(sys.argv) < 2:
        print("Usage: cli.py <plugin> <command> [args]")
        print("\nAvailable plugins:")
        for plugin in _cli_plugins:
            print(f"- {plugin.get_name()}")
        sys.exit(1)

    plugin_name = sys.argv[1]

    for plugin in _cli_plugins:
        if plugin.get_name() == plugin_name:
            if len(sys.argv) < 3 or sys.argv[2] in ("-h", "--help", "help"):
                print(f"Available commands for {plugin.get_name()}:")
                print(plugin.get_help())
                sys.exit(0 if len(sys.argv) >= 3 and sys.argv[2] in ("-h", "--help", "help") else 1)

            command = sys.argv[2]
            args = sys.argv[3:]

            if command in plugin.get_commands():
                try:
                    result = plugin.run_command(command, *args)
                    print(result)
                except Exception as e:
                    print(f"Error: {e}")
                    sys.exit(1)
                break
            else:
                print(f"Unknown command: {command}")
                print(f"\nAvailable commands for {plugin.get_name()}:")
                print(plugin.get_help())
                sys.exit(1)
    else:
        print(f"Unknown plugin: {plugin_name}")
        print("\nAvailable plugins:")
        for plugin in _cli_plugins:
            print(f"- {plugin.get_name()}")
        sys.exit(1)


if __name__ == "__main__":
    main()
