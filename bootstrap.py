# go1.18.10.darwin-arm64.pkg
# go1.18.10.linux-amd64.tar.gz

# https://go.dev/dl/go1.18.10.linux-amd64.tar.gz

# https://go.dev/dl/go1.18.10.windows-amd64.msi

# https://go.dev/dl/go1.18.10.darwin-amd64.pkg

# https://go.dev/dl/go1.18.10.darwin-arm64.pkg

import platform

# Get the name of the operating system
os_name = platform.system()

# Get the architecture
architecture = platform.machine()

# Get the OS version
os_version = platform.version()

print(f"Operating System: {os_name}")
print(f"Architecture: {architecture}")
print(f"OS Version: {os_version}")