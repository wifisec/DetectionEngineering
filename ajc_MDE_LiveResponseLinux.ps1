<#
.SYNOPSIS
    Collects specified system and configuration files from a Linux host for DFIR (Digital Forensics and Incident Response) purposes.

.DESCRIPTION
    This script collects various system and configuration files from a Linux host, logs details about the collected files (including file existence, size, permissions, and SHA1 hash), and compresses the collected files and log into a single archive. The script ensures all actions occur under a subfolder named with the current date and time under the MDTAP user's home directory.
    
    The script includes functionalities to:
        - Identify the home directory of the MDTAP user.
        - Create a unique subfolder using the current date and time.
        - Collect specified files and directories.
        - Log detailed information about each collected file.
        - Compress the collected files and log into a single archive.

.REFERENCES
    https://techcommunity.microsoft.com/blog/microsoftdefenderatpblog/announcing-live-response-for-macos-and-linux/2864397
    https://learn.microsoft.com/en-us/defender-endpoint/live-response

.AUTHOR
    Adair John Collins

.VERSION
    1.0
#>

# Identify the MDTAP user's home directory
$User = "MDTAP"
$HomeDir = (Get-LocalUser -Name $User).HomeDirectory

if (-Not (Test-Path $HomeDir)) {
    Write-Output "The home directory for the user $User does not exist. Exiting script."
    exit
}

# Get the current date and time to create a unique subfolder
$DateTime = Get-Date -Format "yyyyMMdd_HHmmss"
$BaseDir = "$HomeDir/collected_files_$DateTime"
$DestDir = "$BaseDir/files"
$LogFile = "$BaseDir/collection_log.txt"
$ArchivePath = "$BaseDir/collected_files.zip"

# Create the necessary directories
if (-Not (Test-Path $DestDir)) {
    New-Item -Path $DestDir -ItemType Directory -Force
}

# Initialize the log file
if (Test-Path $LogFile) {
    Remove-Item $LogFile
}
New-Item -Path $LogFile -ItemType File -Force

# Function to log information
function Log-Info {
    param (
        [string]$Message
    )
    Add-Content -Path $LogFile -Value $Message
}

# Function to collect a file if it exists and log details
function Collect-File {
    param (
        [string]$FilePath
    )
    if (Test-Path $FilePath) {
        $FileInfo = Get-Item $FilePath
        $SHA1Hash = Get-FileHash -Path $FilePath -Algorithm SHA1 | Select-Object -ExpandProperty Hash
        $Details = "Collected: $FilePath`nSize: $($FileInfo.Length) bytes`nPermissions: $($FileInfo.Attributes)`nSHA1: $SHA1Hash`n"
        Log-Info $Details
        Copy-Item -Path $FilePath -Destination $DestDir
    } else {
        Log-Info "File not found: $FilePath"
    }
}

# Function to collect all files in a directory and log details
function Collect-Directory {
    param (
        [string]$DirPath
    )
    if (Test-Path $DirPath -PathType Container) {
        Copy-Item -Path "$DirPath/*" -Destination $DestDir -Recurse
        Log-Info "Collected all files from: $DirPath"
    } else {
        Log-Info "Directory not found: $DirPath"
    }
}

# Collect specified files
Collect-File "/etc/ssh/sshd_config"
Collect-File "/etc/ssh/ssh_config"
Collect-File "/etc/sudoers"
Collect-File "/etc/shells"
Collect-File "/var/log/secure"
Collect-File "/var/log/auth.log"
Collect-File "/var/log/syslog"
Collect-File "/var/log/kern.log"
Collect-File "/var/log/boot.log"
Collect-File "/var/log/dmesg"
Collect-File "/var/log/messages"
Collect-File "/var/log/cron.log"
Collect-File "/var/log/mail.log"
Collect-File "/etc/passwd"
Collect-File "/etc/group"
Collect-File "/etc/shadow"
Collect-File "/etc/os-release"
Collect-File "/etc/hosts"
Collect-File "/etc/hosts.deny"
Collect-File "/etc/hosts.allow"
Collect-File "/etc/resolv.conf"
Collect-File "/etc/hostname"
Collect-File "/root/.bash_history"
Collect-File "/root/.sh_history"
Collect-Directory "/root/.ssh"
Collect-File "/root/.osquery/history"
Collect-File "/etc/audit/audit.rules"
Collect-File "/etc/audit/audit.log"
Collect-File "/etc/audit/auditctl"
Collect-Directory "/etc/audit/audisp/plugins.d"
Collect-File "/etc/audit/audisp.conf"
Collect-File "/etc/audit/auditd.conf"
Collect-Directory "/etc/audit/audit.rules.d"
Collect-File "/etc/audit/auditd/remote.conf"
Collect-File "/etc/audit/auditd/remote.log"
Collect-File "/var/ossec/logs/ossec.log"
Collect-File "/var/ossec/logs/alerts/alerts.json"
Collect-File "/etc/firewalld/zones/public.xml"
Collect-File "/etc/apache2/apache2.conf"
Collect-File "/var/log/apache2/access.log"
Collect-File "/var/log/apache2/error.log"
Collect-File "/etc/mysql/my.cnf"
Collect-File "/var/log/mysql/error.log"
Collect-File "/var/log/mysql/mysql.log"
Collect-File "/etc/krb5.conf"
Collect-File "/var/log/krb5libs.log"
Collect-File "/var/log/krb5kdc.log"
Collect-File "/var/log/kadmind.log"
Collect-File "/var/log/apt/history.log"
Collect-File "/var/log/apt/term.log"
Collect-File "/var/log/rhsm/rhsm.log"
Collect-File "/var/log/yum.log"
Collect-Directory "/etc/pam.d"
Collect-File "/etc/nsswitch.conf"
Collect-File "/etc/iptables/rules.v4"
Collect-File "/etc/iptables/rules.v6"
Collect-File "/etc/network/interfaces"
Collect-Directory "/etc/sysconfig/network-scripts"
Collect-Directory "/etc/ufw"

# Collect fstab and other file system configuration files
Collect-File "/etc/fstab"

# Collect GRUB configuration files
Collect-File "/boot/grub/grub.cfg"
Collect-Directory "/etc/grub.d"

# Collect SMB/AFS/NIS file sharing configurations and logs
Collect-File "/etc/samba/smb.conf"
Collect-File "/var/log/samba/log.smbd"
Collect-File "/var/log/samba/log.nmbd"
Collect-File "/etc/nfs.conf"
Collect-File "/usr/afs/etc/afs.conf"
Collect-File "/usr/afs/logs/FileLog"
Collect-File "/usr/afs/logs/VolserLog"

# Collect user cron files and crontab
Collect-Directory "/var/spool/cron/crontabs"
Collect-File "/etc/crontab"

# Collect systemd configuration files
Collect-Directory "/etc/systemd/system"

# Compress all collected files into a single archive
if (Test-Path $ArchivePath) {
    Remove-Item $ArchivePath
}
Compress-Archive -Path "$DestDir/*" -DestinationPath $ArchivePath

# Include the log file in the archive
Compress-Archive -Path $LogFile -Update -DestinationPath $ArchivePath

Write-Output "File collection complete. Collected files are stored in $DestDir and compressed into $ArchivePath. Log file is included in the archive."
