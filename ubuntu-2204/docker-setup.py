from io import StringIO

from pyinfra.operations import apt, server, files, docker

# TODO: Check if official docker already installed and bail early
apt.packages(
    name="Remove unofficial distro packages",
    packages=[
        "docker.io",
        "docker-doc",
        "docker-compose",
        "docker-compose-v2",
        "podman-docker",
        "containerd",
        "runc",
    ],
    present=False,
    update=True,
    _sudo=True,
)

server.shell(
    name="Create APT keyring directory",
    commands=[
        "install -m 0755 -d /etc/apt/keyrings",
    ],
    _sudo=True,
)

# Download Docker's official GPG key and place it in the keyrings directory
files.download(
    name="Download Docker GPG key",
    src="https://download.docker.com/linux/ubuntu/gpg",
    dest="/etc/apt/keyrings/docker.asc",
    user="root",
    group="root",
    mode="644",
    _sudo=True,
)

files.put(
    name="Add docker to APT sources",
    src=StringIO(
        "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu   jammy stable"
    ),
    dest="/etc/apt/sources.list.d/docker.list",
    user="root",
    group="root",
    mode="644",
    _sudo=True,
)

apt.packages(
    name="Install official docker packages",
    packages=[
        "docker-ce",
        "docker-ce-cli",
        "containerd.io",
        "docker-buildx-plugin",
        "docker-compose-plugin",
    ],
    update=True,
    _sudo=True,
)

docker.container(
    name="Test docker with hello-world container",
    container="hello-world",
    image="hello-world",
    force=True,
    start=True,
    _sudo=True,
)
