# -*- coding: utf-8 -*-


def main(args=None) -> None:
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="The material microstructure simulation."
    )

    parser.add_argument(
        "-n", "--name", required=True, help="The name of the model to run."
    )
    parser.add_argument(
        "-i", "--input", required=True, help="The input file for simulation settings."
    )
    parser.add_argument(
        "-o", "--output", required=True, help="The output folder for smulation results."
    )
    parser.add_argument(
        "-s", "--steps", required=True, help="The number of smulation steps."
    )

    parser.add_argument("-V", "--verbose", action="store_true", help="A verbose mode")

    options = parser.parse_args()

    print(options)

    # Simulation here

    print("[---FINISHED---]")

    sys.exit(0)


if __name__ == "__main__":
    main()
