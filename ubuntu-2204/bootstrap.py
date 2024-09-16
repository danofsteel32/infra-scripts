"""Ubuntu 22.04 VM and Container Host."""

from pyinfra.operations import files, apt, server, systemd


# Make sure can run sudo commands w/o password
files.line(
    name="Allow 'dan' to run sudo commands without a password",
    path="/etc/sudoers.d/dan",
    line="dan ALL=(ALL) NOPASSWD: ALL",
    present=True,
    _sudo=True,
)


## BEGIN SSH ##
files.directory(
    name="Ensure ~/.ssh exists with correct permissions",
    path="/home/dan/.ssh",
    present=True,
    user="dan",
    group="dan",
    mode="700",
)

files.file(
    name="Ensure ~/.ssh/authorized_keys exists with correct permissions",
    path="/home/dan/.ssh/authorized_keys",
    present=True,
    user="dan",
    group="dan",
    mode="600",
)

for pub_key in [
    "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDltlXe+Q5cPdcY/vtNcrWM/R+PpSUPwFrnDCrq99jKk dan@fedora-nuc",
    "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJcdjrnF94EU4a5SVrHmzKv7XTSPPTpwyN7XJX+Bzaa2 dan@sway-t480",
]:
    files.line(
        name="Add public key to ~/.ssh/authorized_keys",
        path="/home/dan/.ssh/authorized_keys",
        line=pub_key,
        present=True,
    )

# 8. Secure SSH
files.line(
    name="Update PermitRootLogin to prohibit-password",
    path="/etc/ssh/sshd_config",
    line="PermitRootLogin",
    replace="PermitRootLogin prohibit-password",
    present=True,
    backup=True,
    _sudo=True,
)
files.line(
    name="Disable password authentication in SSH",
    path="/etc/ssh/sshd_config",
    line="PasswordAuthentication",
    replace="PasswordAuthentication no",
    present=True,
    backup=True,
    _sudo=True,
)
systemd.service(
    name="Restart SSH service",
    service="ssh.service",
    running=True,
    enabled=True,
    restarted=True,
    _sudo=True,
)
## END SSH ##

## BEGIN PACKAGES ##
apt.packages(
    name="Ensure required packages are installed",
    packages=[
        "apt-transport-https",
        "ca-certificates",
        "software-properties-common",
        "curl",
        "ripgrep",
        "python-is-python3",
        "foot-terminfo",
        "neovim",
        "git",
        "bat",
    ],
    update=True,
    _sudo=True,
)
## END PACKAGES ##

## BEGIN FILES ##
# .gitconfig
# .bashrc
## END FILES ##
