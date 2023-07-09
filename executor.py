import subprocess


class Executor:
    class Executor:
        def execute(self, dependencies):
            for dependency in dependencies:
                print(f"Executing dependency: {dependency.dependency}")
                # Open a command line and execute the command specified by source_url
                try:
                    subprocess.run(dependency.source_url, shell=True, check=True)
                    print("Installation completed successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"Installation failed. Error: {e}")
