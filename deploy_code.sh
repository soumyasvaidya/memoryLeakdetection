
FOLDER_PATH=$1
REPO_NAME=$2
cp ./tmp/$REPO_NAME/* $FOLDER_PATH/
cd $FOLDER_PATH
ls -l .
chmod +x bootstrap

sh ./build_and_test.sh
