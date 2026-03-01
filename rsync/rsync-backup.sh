#!/bin/sh

user="user"
folders="dev docs media uni work"
# backup_path="/mnt/backup/@"
# backup_path="/run/media/veracrypt1"
backup_path=$1

if [ -z "$backup_path" ]; then
  echo "Backup path not set!"
  exit 1
fi

for folder in $folders; do
  rsync -abvPht --no-links --perms --no-owner --no-group --delete-excluded --exclude-from="rsync-exclude.txt" --backup-dir="${backup_path}/backup/${folder}_$(date +%Y-%m-%d)" --delete "/home/${user}/${folder}/" "${backup_path}/${folder}/"
done
