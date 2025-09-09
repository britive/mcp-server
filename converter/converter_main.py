import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from converter.core.file_writer import copy_component_file
from converter.core.generator import generate_tools_package

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--all", action="store_true")

    args = parser.parse_args()
    out_dir = args.output.replace("\\", "/")

    # Step 1: Generate tools and init/runner
    generate_tools_package(generate_all=args.all, output_dir=out_dir)

    # Step 2: Copy shared components to output
    copy_component_file("converter/components/auth_provider.py", f"{out_dir}/auth/")
    copy_component_file("converter/components/utils.py", out_dir)