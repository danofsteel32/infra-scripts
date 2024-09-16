from io import StringIO

from pyinfra.operations import files, server, apt

# Download the GPG key
files.download(
    name="Download the NVIDIA GPG key",
    src="https://nvidia.github.io/libnvidia-container/gpgkey",
    dest="/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg",
    user="root",
    group="root",
    mode="644",
    _sudo=True,
)

# Download the NVIDIA container toolkit list and update it
files.put(
    name="Install the NVIDIA container toolkit list",
    src=StringIO(
        "deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://nvidia.github.io/libnvidia-container/stable/deb/$(ARCH) /"
    ),
    dest="/etc/apt/sources.list.d/nvidia-container-toolkit.list",
    user="root",
    group="root",
    mode="644",
    _sudo=True,
)


apt.packages(
    name="Install nvidia-container-toolkit package",
    packages=["nvidia-container-toolkit"],
    update=True,
    _sudo=True,
)

server.shell(
    name="Configure nvidia-ctk docker runtime",
    commands=[
        "nvidia-ctk runtime configure --runtime=docker",
    ],
    _sudo=True,
)
