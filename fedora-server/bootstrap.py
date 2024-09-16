#!/usr/local/python

from pyinfra.operations import dnf, systemd, server, files

# 1. Update system and install packages
dnf.packages(
    name="Ensure required packages are installed",
    packages=[
        "foot-terminfo",
        "neovim",
        "podman",
        "git",
        "lsd",
        "bat",
        "tmux",
    ],
    update=True,  # will update before installing
)

# 2. Disable default services
systemd.service(
    name="Disable cockpit service",
    service="cockpit.service",
    running=False,
    enabled=False,
)

# 3. Configure firewalld to only allow incoming ssh connections
server.shell(
    name="Allow only SSH connections through firewalld",
    commands=[
        "firewall-cmd --permanent --remove-service=cockpit",
        "firewall-cmd --permanent --remove-service=dhcpv6-client",
        "firewall-cmd --permanent --add-service=ssh",
        "firewall-cmd --reload",
    ],
)

# 4. Create user 'dan'
server.user(
    name="Ensure user 'dan' exists with wheel group",
    user="dan",
    groups=["wheel"],
    present=True,
    create_home=True,
    public_keys=["/home/dan/.ssh/id_ed25519.pub"],
    password="$y$j9T$CslzALqb/s8hMrUgV8UN2/$pIKhrrRJpCOcPjc5OFFERtf/zIkJJ4HhmmdmpEkTx40",
)
# 5. Give 'dan' sudo with no password
files.line(
    name="Allow 'dan' to run sudo commands without a password",
    path="/etc/sudoers",
    line="dan ALL=(ALL) NOPASSWD: ALL",
    present=True,
    backup=True,
)

# 6. Copy local .bashrc to dan's home directory
files.put(
    name="Copy local .bashrc to dan's home directory",
    src="/home/dan/.bashrc",
    dest="/home/dan/.bashrc",
    user="dan",
    group="dan",
    mode="644",
)

# 7. Copy local .tmux.conf to dan's home directory
files.put(
    name="Copy local .tmux.conf to dan's home directory",
    src="/home/dan/.tmux.conf",
    dest="/home/dan/.tmux.conf",
    user="dan",
    group="dan",
    mode="644",
)

# 8. Secure SSH
files.replace(
    name="Update PermitRootLogin to prohibit-password",
    path="/etc/ssh/sshd_config",
    text="^PermitRootLogin .*$",
    replace="PermitRootLogin prohibit-password",
    backup=True,
)
files.replace(
    name="Disable password authentication in SSH",
    path="/etc/ssh/sshd_config",
    text="^PasswordAuthentication .*$",
    replace="PasswordAuthentication no",
    backup=True,
)
systemd.service(
    name="Restart SSH service",
    service="sshd",
    running=True,
    enabled=True,
    restarted=True,
)

# 8. Reboot the system
# server.reboot(
#     name="Rebooting the system",
#     delay=2
# )
