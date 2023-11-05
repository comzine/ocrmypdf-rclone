#!/bin/bash

# Function to check if a directory is mounted
is_mounted() {
  mountpoint -q "$1"
}

echo "Running as user: $(whoami)"

# Mount the first Dropbox folder
rclone mount dropbox:Dokumente/_Eingang/withOCR /output --daemon --log-file=/var/log/rclone-output.log --log-level INFO

# Mount the second Dropbox folder
rclone mount dropbox:Dokumente/_Eingang/withoutOCR /input --daemon --log-file=/var/log/rclone-input.log --log-level INFO

# Give rclone some time to establish the mounts
sleep 5

# Check if /output is mounted, retry if not
for i in 1 2 3 4 5; do
  if is_mounted /output; then
    echo "/output is mounted."
    break
  else
    echo "/output not mounted, waiting..."
    sleep 5
  fi
done

# Check if /input is mounted, retry if not
for i in 1 2 3 4 5; do
  if is_mounted /input; then
    echo "/input is mounted."
    break
  else
    echo "/input not mounted, waiting..."
    sleep 5
  fi
done

python3 -u watchit.py
