import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import main


def cli():
    if len(sys.argv) < 2:
        print("Usage: vault-insight <command>")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]  # flags ex: (--force)

    main(command, args)


if __name__ == "__main__":
    cli()
