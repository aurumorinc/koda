import sys
import subprocess
import re
import os

# Clear BROWSER to prevent pydantic crashes during import
os.environ.pop("BROWSER", None)

def main():
    """
    Wrapper around pytest to run tests sequentially in completely isolated processes.
    This prevents memory leaks and orphaned browser processes from accumulating.
    It perfectly mimics the original pytest stdout.
    """
    args = sys.argv[1:]
    
    # If the user is already running a specific test (contains '::') 
    # or just collecting tests, run the real pytest directly.
    is_specific_test = any("::" in arg for arg in args)
    is_collect_only = "--collect-only" in args
    is_help = "--help" in args or "-h" in args
    
    if is_specific_test or is_collect_only or is_help:
        result = subprocess.run([sys.executable, "-m", "pytest"] + args)
        sys.exit(result.returncode)
        
    # Step 1: Collect all target tests
    collect_cmd = [sys.executable, "-m", "pytest", "--collect-only", "-q"] + args
    collect_result = subprocess.run(collect_cmd, capture_output=True, text=True)
    
    if collect_result.returncode != 0 and not collect_result.stdout.strip():
        print(collect_result.stderr, file=sys.stderr)
        sys.exit(collect_result.returncode)
        
    # Extract test node IDs (lines containing '::')
    tests = [line.strip() for line in collect_result.stdout.splitlines() if "::" in line]
    
    if not tests:
        # If no tests, just run pytest normally to let it print its "no tests ran" message
        result = subprocess.run([sys.executable, "-m", "pytest"] + args)
        sys.exit(result.returncode)
        
    total_tests = len(tests)
    
    # Step 2: Print the authentic pytest header
    run_args = []
    skip_next = False
    for arg in args:
        if skip_next:
            skip_next = False
            run_args.append(arg)
            continue
            
        # Keep options that take paths so we don't accidentally drop their values
        if arg in ["--rootdir", "--ignore", "--ignore-glob", "-c", "--confcutdir", "--basetemp", "--junitxml", "--html", "-W"]:
            run_args.append(arg)
            skip_next = True
            continue
            
        if arg == "-q":
            continue
            
        # Skip positional arguments that are files or directories (these are test targets)
        if not arg.startswith("-") and (os.path.exists(arg) or "::" in arg):
            continue
            
        run_args.append(arg)
    
    # We will run the first test normally but capture it to extract the header
    first_test_cmd = [sys.executable, "-m", "pytest"] + run_args + [tests[0], "--no-summary", "--color=yes"]
    first_result = subprocess.run(first_test_cmd, capture_output=True, text=True)
    
    lines = first_result.stdout.splitlines()
    header_lines = []
    
    first_test_filename = tests[0].split("::")[0]
    for i, line in enumerate(lines):
        if first_test_filename in line and ("[" in line and "%]" in line):
            break
        header_lines.append(line)
        
    # Print the header
    for line in header_lines:
        print(line)
        
    failed_tests = []
    failures_output = []
    current_file = None
    
    def run_and_stream_test(cmd, test_id, current_idx):
        nonlocal failed_tests, failures_output, current_file
        
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
        
        in_failure = False
        failure_content = []
        test_filename = test_id.split("::")[0]
        
        if process.stdout:
            for line in process.stdout:
                clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line)
                
                # Capture failures for the summary
                if "FAILURES" in clean_line or "ERRORS" in clean_line or in_failure:
                    if "short test summary info" in clean_line or (clean_line.startswith("===") and clean_line.endswith("===") and " in " in clean_line):
                        in_failure = False
                    else:
                        if "FAILURES" in clean_line or "ERRORS" in clean_line:
                            in_failure = True
                        if in_failure:
                            failure_content.append(line.rstrip('\n'))
                    continue
                
                # Filter out pytest session start/end lines
                is_summary_line = clean_line.startswith("===") and clean_line.strip().endswith("===")
                is_session_line = "test session starts" in clean_line or "collected" in clean_line or is_summary_line
                if is_session_line or "short test summary info" in clean_line:
                    continue
                    
                # Process the actual test result line
                if test_filename in clean_line and ("[" in clean_line and "%]" in clean_line):
                    parts = clean_line.split()
                    filename = parts[0]
                    
                    if current_file != filename:
                        if current_file is not None:
                            print() # Newline for previous file
                        current_file = filename
                        print(f"{filename} ", end="")
                        
                    # Extract just the colored dot
                    dot = parts[1] if len(parts) > 1 else "."
                    print(dot, end="")
                    sys.stdout.flush()
                    continue
                    
                # Print any other output (e.g., stdout from the test itself)
                if clean_line.strip():
                    print(line, end="")
                    sys.stdout.flush()
                
        process.wait()
        
        if failure_content:
            failed_tests.append(test_id)
            failures_output.extend(failure_content)
            
        if process.returncode != 0 and test_id not in failed_tests:
            failed_tests.append(test_id)

    # Process first test
    in_failure = False
    test_filename = tests[0].split("::")[0]
    for line in first_result.stdout.splitlines(True):
        clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line)
            
        if "FAILURES" in clean_line or "ERRORS" in clean_line or in_failure:
            if "short test summary info" in clean_line or (clean_line.startswith("===") and clean_line.endswith("===") and " in " in clean_line):
                in_failure = False
            else:
                if "FAILURES" in clean_line or "ERRORS" in clean_line:
                    in_failure = True
                if in_failure:
                    failures_output.append(line.rstrip('\n'))
            continue
                    
        is_summary_line = clean_line.startswith("===") and clean_line.strip().endswith("===")
        is_session_line = "collected" in clean_line or is_summary_line
        if is_session_line or "short test summary info" in clean_line or line.rstrip('\n') in header_lines:
            continue
            
        if test_filename in clean_line and ("[" in clean_line and "%]" in clean_line):
            parts = clean_line.split()
            filename = parts[0]
            
            if current_file != filename:
                if current_file is not None:
                    print()
                current_file = filename
                print(f"{filename} ", end="")
                
            dot = parts[1] if len(parts) > 1 else "."
            print(dot, end="")
            sys.stdout.flush()
            continue
            
        if clean_line.strip():
            print(line, end="")
            sys.stdout.flush()
            
    if first_result.returncode != 0 and tests[0] not in failed_tests:
        failed_tests.append(tests[0])
            
    # Step 3: Run the rest of the tests
    for i in range(1, total_tests):
        test_id = tests[i]
        cmd = [sys.executable, "-m", "pytest"] + run_args + [test_id, "--no-header", "--no-summary", "--color=yes"]
        run_and_stream_test(cmd, test_id, i + 1)
        
    # Print the final percentage
    print(f" [{100:>3}%]")
        
    # Step 4: Print failures and summary
    if failures_output:
        print("")
        for line in failures_output:
            print(line)
            
    print("")
    print("=========================== short test summary info ============================")
    if failed_tests:
        for failed in failed_tests:
            print(f"FAILED {failed}")
        print(f"=================== {len(failed_tests)} failed, {total_tests - len(failed_tests)} passed in 0.00s ====================")
        sys.exit(1)
    else:
        print(f"============================== {total_tests} passed in 0.00s ===============================")
        sys.exit(0)

if __name__ == "__main__":
    main()
