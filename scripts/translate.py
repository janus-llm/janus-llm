import sys
from pathlib import Path

if __name__ == "__main__":
    args = sys.argv
    cli_path = Path(args[0]).parent / "cli.py"
    args[0] = str(cli_path)
    print(f'Please use command "{args[0]} translate" instead of this')
