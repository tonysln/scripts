#!/bin/sh


folders="slavin"
backup_path="/media/anton/Storage"

for folder in $folders;
do
	rsync -abvPht --no-links --perms --no-owner --no-group --delete-excluded --exclude-from="rsync-exclude.txt" --backup-dir="${backup_path}/Backup/${folder}_$(date +%Y-%m-%d)" --delete "/home/anton/${folder}/" "${backup_path}/${folder}/"
done

