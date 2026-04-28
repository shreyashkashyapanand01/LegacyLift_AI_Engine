# import subprocess
# import uuid
# import os
# import logging

# logger = logging.getLogger(__name__)


# class DockerManager:

#     def __init__(self):
#         self.container_name = f"exec_{uuid.uuid4().hex[:8]}"

#     # ---------------------------
#     # 🐳 RUN PYTHON CODE (SECURE)
#     # ---------------------------
#     def run_python(self, file_path: str):
#         try:
#             command = [
#                 "docker", "run", "--rm",
#                 "--name", self.container_name,

#                 # 🔒 SECURITY HARDENING
#                 "--network", "none",
#                 "--read-only",
#                 "--pids-limit", "64",

#                 # 🔒 RESOURCE LIMITS
#                 "--memory", "128m",
#                 "--cpus", "0.5",

#                 # 📂 SAFE MOUNT (READ-ONLY)
#                 "-v", f"{os.path.dirname(file_path)}:/app:ro",
#                 "-w", "/app",

#                 "python:3.10",

#                 "python", os.path.basename(file_path)
#             ]

#             result = subprocess.run(
#                 command,
#                 capture_output=True,
#                 text=True,
#                 timeout=5
#             )

#             return result.stdout, result.stderr

#         except subprocess.TimeoutExpired:
#             return "", "Execution timed out"

#         except Exception as e:
#             logger.exception("Docker python execution failed")
#             return "", str(e)

#     # ---------------------------
#     # ☕ RUN JAVA CODE (SECURE)
#     # ---------------------------
#     def run_java(self, file_path: str):
#         try:
#             command = [
#                 "docker", "run", "--rm",
#                 "--name", self.container_name,

#                 # 🔒 SECURITY HARDENING
#                 "--network", "none",
#                 "--read-only",
#                 "--pids-limit", "64",

#                 # 🔒 RESOURCE LIMITS
#                 "--memory", "256m",
#                 "--cpus", "1",

#                 # 📂 SAFE MOUNT
#                 "-v", f"{os.path.dirname(file_path)}:/app:ro",
#                 "-w", "/app",

#                 # ✅ FIXED IMAGE
#                 "eclipse-temurin:17",

#                 "bash", "-c",
#                 f"javac {os.path.basename(file_path)} && java Runner"
#             ]

#             result = subprocess.run(
#                 command,
#                 capture_output=True,
#                 text=True,
#                 timeout=7
#             )

#             return result.stdout, result.stderr

#         except subprocess.TimeoutExpired:
#             return "", "Execution timed out"

#         except Exception as e:
#             logger.exception("Docker java execution failed")
#             return "", str(e)






import subprocess
import uuid
import os
import logging

logger = logging.getLogger(__name__)


class DockerManager:

    def __init__(self):
        self.container_name = f"exec_{uuid.uuid4().hex[:8]}"

    # ---------------------------
    # 🐳 RUN PYTHON CODE (SECURE)
    # ---------------------------
    def run_python(self, file_path: str):
        try:
            command = [
                "docker", "run", "--rm",
                "--name", self.container_name,

                # 🔒 SECURITY HARDENING
                "--network", "none",
                "--read-only",
                "--pids-limit", "64",

                # 🔒 RESOURCE LIMITS
                "--memory", "128m",
                "--cpus", "0.5",

                # 📂 SAFE MOUNT (READ-ONLY)
                "-v", f"{os.path.dirname(file_path)}:/app:ro",
                "-w", "/app",

                "python:3.10",

                "python", os.path.basename(file_path)
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=5
            )

            return result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            return "", "Execution timed out"

        except Exception as e:
            logger.exception("Docker python execution failed")
            return "", str(e)

    # ---------------------------
    # ☕ RUN JAVA CODE (SECURE + FIXED)
    # ---------------------------
    def run_java(self, file_path: str):
        try:
            command = [
                "docker", "run", "--rm",
                "--name", self.container_name,

                # 🔒 SECURITY HARDENING
                "--network", "none",
                "--pids-limit", "64",

                # 🔥 ALLOW TEMP WRITE (ONLY HERE)
                "--tmpfs", "/tmp",

                # 🔒 RESOURCE LIMITS
                "--memory", "256m",
                "--cpus", "1",

                # 📂 READ-ONLY CODE
                "-v", f"{os.path.dirname(file_path)}:/app:ro",
                "-w", "/app",

                "eclipse-temurin:17",

                "bash", "-c",
                f"javac -d /tmp {os.path.basename(file_path)} && java -cp /tmp Runner"
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=7
            )

            return result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            return "", "Execution timed out"

        except Exception as e:
            logger.exception("Docker java execution failed")
            return "", str(e)