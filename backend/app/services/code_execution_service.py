import subprocess
import tempfile
import time
import os


class CodeExecutionService:
    @staticmethod
    def run_python(source_code: str):
        """
        Execute Python code safely and return execution result.
        """

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8",
        ) as temp_file:
            temp_file.write(source_code)
            temp_file_path = temp_file.name

        try:
            start_time = time.perf_counter()

            result = subprocess.run(
                ["python", temp_file_path],
                capture_output=True,
                text=True,
                timeout=5,
            )

            execution_time = round(time.perf_counter() - start_time, 4)

            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "execution_time": execution_time,
            }

        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": "Execution timed out.",
                "return_code": -1,
                "execution_time": 5,
            }

        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)