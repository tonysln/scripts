#!/bin/sh


user="user"
folders="dev docs media photos uni videos work"
backup_path="/mnt/backup/@"

for folder in $folders;
do
	rsync -abvPht --no-links --perms --no-owner --no-group --delete-excluded --exclude-from="rsync-exclude.txt" --backup-dir="${backup_path}/backup/${folder}_$(date +%Y-%m-%d)" --delete "/home/${user}/${folder}/" "${backup_path}/${folder}/"
done

