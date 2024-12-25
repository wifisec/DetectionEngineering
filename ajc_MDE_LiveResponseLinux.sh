#!/bin/bash

: <<'COMMENT_BLOCK'
# --------------------------------------------------------------------
# SYNOPSIS
#     Collects specified system and configuration files from a Linux host for DFIR (Digital Forensics and Incident Response) purposes.
#
# DESCRIPTION
#     This script collects various system and configuration files from a Linux host, logs details about the collected files (including file existence, size, permissions, and SHA1 hash), and compresses the collected files and log into a single archive. The script ensures all actions occur under a subfolder named with the current date and time under the MDTAP user's home directory.
#
#     The script includes functionalities to:
#         - Identify the home directory of the MDTAP user.
#         - Create a unique subfolder using the current date and time.
#         - Collect specified files and directories.
#         - Log detailed information about each collected file.
#         - Compress the collected files and log into a single archive.
#         - Clean up the collected files after compression.
#
# REFERENCES
#     https://techcommunity.microsoft.com/blog/microsoftdefenderatpblog/announcing-live-response-for-macos-and-linux/2864397
#     https://learn.microsoft.com/en-us/defender-endpoint/live-response
#
# AUTHOR
#     Adair John Collins
#
# VERSION
#     1.1
# --------------------------------------------------------------------
COMMENT_BLOCK

# Identify the MDTAP user's home directory
USER="MDTAP"
HOME_DIR=$(eval echo ~$USER)

if [ ! -d "$HOME_DIR" ]; then
    echo "The home directory for the user $USER does not exist. Exiting script."
    exit 1
fi

# Get the current date and time to create a unique subfolder
DATETIME=$(date +"%Y%m%d_%H%M%S")
BASE_DIR="$HOME_DIR/collected_files_$DATETIME"
DEST_DIR="$BASE_DIR/files"
LOG_FILE="$BASE_DIR/collection_log.txt"
ARCHIVE_PATH="$BASE_DIR/collected_files.zip"

# Create the necessary directories
mkdir -p "$DEST_DIR"

# Initialize the log file
: > "$LOG_FILE"

# Function to log information
log_info() {
    local message="$1"
    echo -e "$message" >> "$LOG_FILE"
}

# Function to collect a file if it exists and log details
collect_file() {
    local file_path="$1"
    if [ -f "$file_path" ]; then
        file_info=$(stat -c "%s %A" "$file_path")
        sha1_hash=$(sha1sum "$file_path" | awk '{print $1}')
        details="Collected: $file_path\nSize: ${file_info%% *} bytes\nPermissions: ${file_info##* }\nSHA1: $sha1_hash\n"
        log_info "$details"
        cp "$file_path" "$DEST_DIR"
    else
        log_info "File not found: $file_path"
    fi
}

# Function to collect all files in a directory and log details
collect_directory() {
    local dir_path="$1"
    if [ -d "$dir_path" ]; then
        cp -r "$dir_path"/* "$DEST_DIR"
        log_info "Collected all files from: $dir_path"
    else
        log_info "Directory not found: $dir_path"
    fi
}

# Function to clean up collected files
cleanup() {
    rm -rf "$DEST_DIR"
    echo "Cleanup complete. Collected files removed."
}

# Collect specified files
collect_file "/etc/ssh/sshd_config"
collect_file "/etc/ssh/ssh_config"
collect_file "/etc/sudoers"
collect_file "/etc/shells"
collect_file "/var/log/secure"
collect_file "/var/log/auth.log"
collect_file "/var/log/syslog"
collect_file "/var/log/kern.log"
collect_file "/var/log/boot.log"
collect_file "/var/log/dmesg"
collect_file "/var/log/messages"
collect_file "/var/log/cron.log"
collect_file "/var/log/mail.log"
collect_file "/etc/passwd"
collect_file "/etc/group"
collect_file "/etc/shadow"
collect_file "/etc/os-release"
collect_file "/etc/hosts"
collect_file "/etc/hosts.deny"
collect_file "/etc/hosts.allow"
collect_file "/etc/resolv.conf"
collect_file "/etc/hostname"
collect_file "/root/.bash_history"
collect_file "/root/.sh_history"
collect_directory "/root/.ssh"
collect_file "/root/.osquery/history"
collect_file "/etc/audit/audit.rules"
collect_file "/etc/audit/audit.log"
collect_file "/etc/audit/auditctl"
collect_directory "/etc/audit/audisp/plugins.d"
collect_file "/etc/audit/audisp.conf"
collect_file "/etc/audit/auditd.conf"
collect_directory "/etc/audit/audit.rules.d"
collect_file "/etc/audit/auditd/remote.conf"
collect_file "/etc/audit/auditd/remote.log"
collect_file "/var/ossec/logs/ossec.log"
collect_file "/var/ossec/logs/alerts/alerts.json"
collect_file "/etc/firewalld/zones/public.xml"
collect_file "/etc/apache2/apache2.conf"
collect_file "/var/log/apache2/access.log"
collect_file "/var/log/apache2/error.log"
collect_file "/etc/mysql/my.cnf"
collect_file "/var/log/mysql/error.log"
collect_file "/var/log/mysql/mysql.log"
collect_file "/etc/krb5.conf"
collect_file "/var/log/krb5libs.log"
collect_file "/var/log/krb5kdc.log"
collect_file "/var/log/kadmind.log"
collect_file "/var/log/apt/history.log"
collect_file "/var/log/apt/term.log"
collect_file "/var/log/rhsm/rhsm.log"
collect_file "/var/log/yum.log"
collect_directory "/etc/pam.d"
collect_file "/etc/nsswitch.conf"
collect_file "/etc/iptables/rules.v4"
collect_file "/etc/iptables/rules.v6"
collect_file "/etc/network/interfaces"
collect_directory "/etc/sysconfig/network-scripts"
collect_directory "/etc/ufw"

# Collect fstab and other file system configuration files
collect_file "/etc/fstab"

# Collect GRUB configuration files
collect_file "/boot/grub/grub.cfg"
collect_directory "/etc/grub.d"

# Collect SMB/AFS/NIS file sharing configurations and logs
collect_file "/etc/samba/smb.conf"
collect_file "/var/log/samba/log.smbd"
collect_file "/var/log/samba/log.nmbd"
collect_file "/etc/nfs.conf"
collect_file "/usr/afs/etc/afs.conf"
collect_file "/usr/afs/logs/FileLog"
collect_file "/usr/afs/logs/VolserLog"

# Collect user cron files and crontab
collect_directory "/var/spool/cron/crontabs"
collect_file "/etc/crontab"

# Collect systemd configuration files
collect_directory "/etc/systemd/system"

# Compress all collected files into a single archive
zip -r "$ARCHIVE_PATH" "$DEST_DIR" "$LOG_FILE"

# Clean up collected files
cleanup

echo "File collection complete. Collected files are stored in $ARCHIVE_PATH. Log file is included in the archive."
