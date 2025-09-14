# example tiny local agent by A.I. Christianson, founder of gobii.ai, builder of ra-aid.ai
#
# to run: uv run --with 'smolagents[mlx-lm]' --with ddgs smol.py 'how much free disk space do I have?'

from smolagents import CodeAgent, MLXModel, tool
from subprocess import run
import sys
import os
import shutil

def confirm_risky_operation(operation: str, details: str) -> bool:
    """Ask user for confirmation before risky operations."""
    print(f"\n⚠️  RISKY OPERATION: {operation}")
    print(f"Details: {details}")
    while True:
        response = input("Do you want to proceed? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' or 'n'")

def is_risky_file_operation(path: str) -> tuple[bool, str]:
    """Check if file operation is risky."""
    abs_path = os.path.abspath(path)
    
    # Check if file exists (overwrite risk)
    if os.path.exists(abs_path):
        return True, f"File {path} already exists and will be overwritten"
    
    # Check if in system directories
    system_dirs = ['/bin', '/sbin', '/usr/bin', '/usr/sbin', '/boot', '/sys', '/proc']
    if any(abs_path.startswith(d) for d in system_dirs):
        return True, f"Writing to system directory: {path}"
    
    # Check file extension for executables
    risky_extensions = ['.sh', '.py', '.exe', '.bat', '.cmd', '.ps1']
    if any(path.lower().endswith(ext) for ext in risky_extensions):
        return True, f"Creating executable file: {path}"
    
    return False, ""

@tool
def write_file(path: str, content: str) -> str:
    """Write text.
    Args:
      path (str): File path.
      content (str): Text to write.
    Returns:
      str: Status.
    """
    try:
        is_risky, risk_reason = is_risky_file_operation(path)
        if is_risky:
            if not confirm_risky_operation("FILE WRITE", risk_reason):
                return "operation cancelled by user"
        
        open(path, "w", encoding="utf-8").write(content)
        return f"saved:{path}"
    except Exception as e:
        return f"error:{e}"

def is_risky_shell_command(cmd: str) -> tuple[bool, str]:
    """Check if shell command is risky."""
    cmd_lower = cmd.lower().strip()
    
    # Commands that modify/delete files
    destructive_commands = ['rm ', 'rmdir ', 'del ', 'format ', 'fdisk ', 'mkfs']
    if any(cmd_lower.startswith(dc) for dc in destructive_commands):
        return True, f"Destructive command: {cmd}"
    
    # Network operations
    network_commands = ['curl ', 'wget ', 'nc ', 'netcat ', 'ssh ', 'scp ', 'rsync ']
    if any(cmd_lower.startswith(nc) for nc in network_commands):
        return True, f"Network operation: {cmd}"
    
    # System modification commands
    system_commands = ['chmod +x ', 'chown ', 'sudo ', 'su ', 'passwd ', 'useradd ', 'userdel ']
    if any(cmd_lower.startswith(sc) for sc in system_commands):
        return True, f"System modification: {cmd}"
    
    # Package installation
    install_commands = ['apt install', 'yum install', 'brew install', 'pip install']
    if any(ic in cmd_lower for ic in install_commands):
        return True, f"Package installation: {cmd}"
    
    # File creation with redirection
    if '>' in cmd or '>>' in cmd:
        return True, f"File redirection: {cmd}"
    
    return False, ""

@tool
def sh(cmd: str) -> str:
    """Run a shell command.
    Args:
      cmd (str): Command to execute.
    Returns:
      str: stdout+stderr.
    """
    try:
        is_risky, risk_reason = is_risky_shell_command(cmd)
        if is_risky:
            if not confirm_risky_operation("SHELL COMMAND", risk_reason):
                return "operation cancelled by user"
        
        r = run(cmd, shell=True, capture_output=True, text=True)
        return r.stdout + r.stderr
    except Exception as e:
        return f"error:{e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python agent.py 'your prompt'"); sys.exit(1)
    common = "use cat/head to read files, use rg to search, use ls and standard shell commands to explore."
    agent = CodeAgent(
        model=MLXModel(model_id="mlx-community/Qwen3-Coder-30B-A3B-Instruct-4bit-dwq-v2", max_tokens=8192, trust_remote_code=True),
        tools=[write_file, sh],
        add_base_tools=True,
    )
    print(agent.run(" ".join(sys.argv[1:]) + " " + common))
