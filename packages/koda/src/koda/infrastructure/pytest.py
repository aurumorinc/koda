import os
import sys
import subprocess

# Clear BROWSER to prevent pydantic environment crashes
os.environ.pop("BROWSER", None)


def main() -> None:
    """
    Wrapper around pytest that automatically applies pytest-xdist file-level load distribution
    (-n auto --dist=loadfile) when running directories/multiple files, while bypassing xdist worker
    spawn overhead when targeting a single specific test file or test ID.
    """
    args = sys.argv[1:]

    # Check if a single test file or specific test ID (with '::') is targeted
    positional_args = [a for a in args if not a.startswith("-")]
    is_single_target = any("::" in arg for arg in args) or (
        len(positional_args) == 1 and os.path.isfile(positional_args[0])
    )

    # Use xdist for multi-file/directory test runs, but bypass worker initialization for single targets
    if not any(arg.startswith("-n") for arg in args) and not is_single_target:
        xdist_args = ["-n", "auto", "--dist", "loadfile"]
    else:
        xdist_args = []

    cmd = [sys.executable, "-m", "pytest"] + xdist_args + args
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
