import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", os.path.abspath(target_dir)]
        if not args == None:
            command.extend(args)

        completed_subprocess = subprocess.run(command, capture_output=True, text=True, timeout=30)
        output_string = ""
        if not completed_subprocess.returncode == 0:
            output_string += f"Process exted with code {completed_subprocess.returncode}"
        if completed_subprocess.stdout == None and completed_subprocess.stderr == None:
            output_string += "No output produced"
        else:
            output_string += f"STDOUT: {completed_subprocess.stdout} STDERR: {completed_subprocess.stderr}"
        

        return output_string
    
    
    except Exception as e:
        return f"Error: executing Python file: {e}"