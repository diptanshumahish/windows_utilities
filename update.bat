#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd "$SCRIPT_DIR/.."

git pull

cp -r utilities/* "$SCRIPT_DIR/../path/to/destination/folder/"

echo "Update complete!"
