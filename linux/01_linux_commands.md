# Linux Commands — Organized Cheat Sheets

A concise, topic-wise collection of Linux commands useful for MLOps engineers.

---

## Files & Directories
- `pwd` — print working directory
- `ls` — list directory contents
- `ls -l` — long listing (permissions, owner, size, date)
- `ls -a` — show hidden files
- `cd <dir>` — change directory
- `mkdir <dir>` — create directory
- `rmdir <dir>` — remove empty directory
- `rm <file>` — delete file
- `rm -rf <dir>` — remove directory recursively
- `tree` — show directory tree (may need `sudo apt install tree`)

---

## File Operations (view/copy/move)
- `touch <file>` — create empty file / update timestamp
- `cp <src> <dst>` — copy files or directories (`-r` for dirs)
- `mv <src> <dst>` — move/rename
- `cat <file>` — print file
- `tac <file>` — reverse cat
- `less <file>` — pager (scrollable)
- `head -n 20 <file>` — first 20 lines
- `tail -n 20 <file>` — last 20 lines
- `tail -f <file>` — follow file (live logs)

---

## Permissions & Ownership
- `chmod <mode> <file>` — change permissions (e.g., `chmod 755 script.sh`)
- `chmod +x <file>` — add execute
- `chown <user>:<group> <file>` — change owner and group
- `stat <file>` — detailed file status

---

## Processes & Jobs
- `ps aux` — list all processes
- `top` — interactive process viewer
- `htop` — improved top (install separately)
- `pgrep <pattern>` — find process IDs by name
- `kill <pid>` — send TERM signal
- `kill -9 <pid>` — force kill SIGKILL
- `nohup <cmd> &` — run command immune to hangups
- `jobs` / `bg` / `fg` — job control (shell background/foreground)

---

## Disk & Storage
- `df -h` — disk filesystem usage (human readable)
- `du -sh <path>` — folder size
- `lsblk` — block devices
- `mount` / `umount <device|mountpoint>` — mount/unmount
- `fdisk -l` — partition table (run as root)

---

## Networking
- `ping <host>` — check connectivity
- `curl <url>` — HTTP requests
- `wget <url>` — download files
- `ss -tuln` / `netstat -tuln` — open ports & listeners
- `ifconfig` or `ip addr` — show network interfaces (`ip` preferred)
- `traceroute <host>` — network route
- `nslookup <host>` / `dig <host>` — DNS lookup

---

## Search & Text Processing
- `find <path> -name "pattern"` — find files
- `grep -R "pattern" <path>` — recursive search inside files
- `egrep` / `fgrep` — extended/ fixed string grep
- `awk '{print $1}' file` — column processing
- `sed 's/old/new/g' file` — stream editing
- `sort` / `uniq -c` — sort and unique count
- `xargs` — build and execute command lines

---

## Compression & Archiving
- `tar -czf archive.tar.gz folder/` — create gzipped tar
- `tar -xzf archive.tar.gz` — extract gzipped tar
- `zip file.zip files...` / `unzip file.zip`

---

## Package Management (Debian/Ubuntu)
- `sudo apt update` — refresh package lists
- `sudo apt upgrade` — upgrade packages
- `sudo apt install <pkg>` — install package
- `sudo apt remove <pkg>` — remove package

(For RHEL/CentOS use `yum`/`dnf`, for Arch use `pacman`.)

---

## Users & Groups
- `whoami` — current user
- `id` — user & group info
- `who` / `w` — who is logged in
- `sudo <command>` — run as root
- `adduser <user>` / `useradd` — create user
- `passwd <user>` — change password

---

## System Info & Logs
- `uname -a` — kernel & system info
- `uptime` — system uptime & load
- `dmesg` — kernel ring buffer (hardware messages)
- `journalctl -u <service>` — systemd logs for a service
- `tail -n 200 /var/log/syslog` or `/var/log/messages`

---

## Services (systemd)
- `sudo systemctl status <service>`
- `sudo systemctl start <service>`
- `sudo systemctl stop <service>`
- `sudo systemctl restart <service>`
- `sudo systemctl enable <service>`
- `sudo systemctl disable <service>`

---

## SSH & Remote
- `ssh user@host` — remote shell
- `scp src user@host:dest` — secure copy
- `rsync -avz src/ user@host:dest/` — efficient sync (useful for model files)

---

## Useful Shortcuts / Tips
- `ctrl + r` — reverse-i-search command history
- `!!` — repeat last command
- `!n` — repeat nth history command
- `command > file` — redirect stdout
- `command >> file` — append stdout
- `command 2>&1` — redirect stderr to stdout
- `<cmd> | tee file` — pipe and save output

---
