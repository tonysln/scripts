#!/bin/sh


user="user"
folders="dev docs media photos uni videos work"
backup_path="/media/user/Storage"

for folder in $folders;
do
	rsync -abvPht --no-links --perms --no-owner --no-group --delete-excluded --exclude-from="rsync-exclude.txt" --backup-dir="${backup_path}/Backup/${folder}_$(date +%Y-%m-%d)" --delete "/home/${user}/${folder}/" "${backup_path}/${folder}/"
done

