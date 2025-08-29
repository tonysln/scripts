#!/bin/sh


folders="docs dev media uni work"

for folder in $folders;
do
	rsync -abvPh --delete-excluded --exclude-from="rsync-exclude.txt" --backup-dir="/Volumes/untitled/Backup/${folder}_$(date +%Y-%m-%d)" --delete "/Users/tony/${folder}/" "/Volumes/untitled/${folder}/" 
done

