
FOLDER_PATH=$1
REPO_NAME=$2
cp ./tmp/$REPO_NAME/* $FOLDER_PATH/
sh $FOLDER_PATH/build_test.sh
