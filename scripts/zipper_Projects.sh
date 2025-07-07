SOURCE_FOLDER="/home/happio/Documents/coding/repos/HappioCrz-Projects/"
SYSTEM_NAME="PROJECTS"

DEST_FOLDER="/home/happio/Documents/coding/backup/HappioCrz-Projects/"
CURRENT_DATETIME=$(date +"%Y-%m-%d_%H-%M-%S")
ZIP_NAME="$SYSTEM_NAME+$CURRENT_DATETIME.zip"

echo "creating zip .. $ZIP_NAME"

cd "$SOURCE_FOLDER"

zip -r "$DEST_FOLDER/$ZIP_NAME" "$SOURCE_FOLDER"/* 


echo "created zip at $DEST_FOLDER"
echo "created zip .. $ZIP_NAME"
echo "of files"
