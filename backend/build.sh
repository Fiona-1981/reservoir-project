#!/usr/bin/env bash
# Builds lambda.zip for AWS Lambda (Python 3.14 on arm64).
# Run with the project's virtual environment activated.
set -euo pipefail

cd "$(dirname "$0")"

rm -rf package lambda.zip
mkdir package

python3 -m pip install \
    --requirement requirements.txt \
    --target package \
    --platform manylinux2014_aarch64 \
    --implementation cp \
    --python-version 3.14 \
    --only-binary=:all:

cp handler.py scrape_uu.py models.py package/

(cd package && zip -r -q ../lambda.zip .)

echo "Built backend/lambda.zip"
