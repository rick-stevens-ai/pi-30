import subprocess

def run_cli(input_str):
    process = subprocess.Popen(['python3', 'cli.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate(input=input_str)
    return stdout.strip()

print("Test 1 (Single):", run_cli("5"))
print("Test 2 (Odd count):", run_cli("1 2 3 4 5"))
print("Test 3 (Even count):", run_cli("1 2 3 4"))
print("Test 4 (Empty):", run_cli(""))
print("Test 5 (Whitespace/Newline):", run_cli("  1\n2\n \n 3 "))

