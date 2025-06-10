from plugins.vps.cli_plugin import VPSCLIPlugin
import sys


_cli_plugins = [VPSCLIPlugin()]

def main():
    if len(sys.argv) < 3:
        print("Usage: cli.py <plugin> <command> [args]")
        sys.exit(1)


    plugin_name = sys.argv[1]
    command = sys.argv[2]
    args = sys.argv[3:]

    for plugin in _cli_plugins:
        if plugin.get_name() != plugin_name:
            continue

        if command in plugin.get_commands():
            try:
                result = plugin.run_command(command, *args)
                print(result)
            except Exception as e:
                print(f"Error: {e}")
            break
    else:
        print(f"Unknown command: {command}")
        for plugin in _cli_plugins:
            print()
            print(f"Available commands for {plugin.get_name()}:")
            print(plugin.get_help())
        sys.exit(1)

if __name__ == "__main__":
    main()
