#!/bin/bash

set -e

npm run build

git add dist && git commit -m "build & add dist subtree"
git subtree push --prefix dist origin gh-pages
