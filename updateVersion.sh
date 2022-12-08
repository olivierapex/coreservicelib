#!/bin/bash
set -e

echo "CI_COMMIT_TAG($CI_COMMIT_TAG) CI_PIPELINE_ID($CI_PIPELINE_ID)"

if [[ -z $CI_PIPELINE_ID ]]; then
    echo "ERROR: CI_PIPELINE_ID is mandatory"
    exit 1
fi

# Current version but no .dev#
CURRENT_WHEEL_VERSION=$(poetry version | awk '{print $2}' | sed 's/^\([0-9]*\.[0-9]*\.[0-9]*.*\)\.dev.*$/\1/')

if [[ -n $CI_COMMIT_TAG ]]; then 
    EXPECTED_TAG=$(echo $CURRENT_WHEEL_VERSION | sed 's/^\([0-9]*\.[0-9]*\.[0-9]*\).*$/\1/')
    echo "EXPECTED_TAG($EXPECTED_TAG)"
    if [[ "$CI_COMMIT_TAG" != "$EXPECTED_TAG" ]]; then
        echo "ERROR: CI_COMMIT_TAG($CI_COMMIT_TAG) is not equal to EXPECTED_TAG($EXPECTED_TAG). Check your version inside pyproject.toml vs tag name."
        exit 1
    fi
fi

if [[ -z $CI_COMMIT_TAG ]]; then 
    NEW_WHEEL_VERSION="${CURRENT_WHEEL_VERSION}.dev${CI_PIPELINE_ID}"; 
else 
    NEW_WHEEL_VERSION="$CI_COMMIT_TAG"
fi

echo "NEW_WHEEL_VERSION=$NEW_WHEEL_VERSION" >> build-python.env
echo "CURRENT_WHEEL_VERSION($CURRENT_WHEEL_VERSION) NEW_WHEEL_VERSION($NEW_WHEEL_VERSION)"

if [[ -z $NEW_WHEEL_VERSION ]]; then 
    echo "ERROR: empty NEW_WHEEL_VERSION is forbidden"
    exit 1
fi
poetry version $NEW_WHEEL_VERSION