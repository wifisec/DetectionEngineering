#!/bin/bash
# rsync_ssh_transfer.sh
# Usage: ./rsync_ssh_transfer.sh /path/to/source user@remote:/path/to/destination

# Exit on error
set -e

# Check arguments
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <source_path> <user@host:destination_path>"
  exit 1
fi

SOURCE=$1
DEST=$2

# Run rsync with SSH
rsync -avz -e ssh "$SOURCE" "$DEST"
