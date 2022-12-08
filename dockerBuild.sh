#!/bin/bash

IMAGE_NAME=core-service-lib
VSCODE_CONTAINER_NAME=vscode-core-service-lib

#Should either be already built in the workspace or if the container is running, offer to build it
if docker inspect ${VSCODE_CONTAINER_NAME} -f '{{.State.Running}}' 2>/dev/null | grep true >/dev/null 2>&1; then
    read -p "vscode container is running, rebuild the project? [yN] " REBUILD_PROJECT
    if [[ "$REBUILD_PROJECT" =~ ^[yY]$ ]]; then
        docker exec -it -u vscode -w /workspace ${VSCODE_CONTAINER_NAME} bash -c "source <(ssh-agent) > /dev/null && ssh-add > /dev/null 2>&1 && poetry run make dist"
    fi
fi

# Get credentials from poetry + sagecipher
if [ -z "$ARTIFACTORY_USERNAME" ] || [ -z "$ARTIFACTORY_API_KEY" ]; then

    if ! docker image inspect ${IMAGE_NAME}:poetry > /dev/null; then
        read -p "Artifactory Username: " ARTIFACTORY_USERNAME
        read -s -p "Artifactory API key: " ARTIFACTORY_API_KEY
        ARTIFACTORY_USERNAME="${ARTIFACTORY_USERNAME}" ARTIFACTORY_API_KEY="${ARTIFACTORY_API_KEY}" docker build --pull --target with_poetry --build-arg ARTIFACTORY_USERNAME --build-arg ARTIFACTORY_API_KEY -t ${IMAGE_NAME}:poetry .
    fi

    ARTIFACTORY_USERNAME=$(docker run -it --rm \
        -v ~/.ssh:/root/.ssh:ro \
        -v ~/.config/pypoetry/:/root/.config/pypoetry/:ro \
        -v ~/.local/share/python_keyring/:/root/.local/share/python_keyring/:ro \
        ${IMAGE_NAME}:poetry bash -c "toml get --toml-path ~/.config/pypoetry/auth.toml http-basic.dfartifactory.username")
    ARTIFACTORY_USERNAME=${ARTIFACTORY_USERNAME%$'\r'}

    ARTIFACTORY_API_KEY=$(docker run -it --rm \
        -v ~/.ssh:/root/.ssh:ro \
        -v ~/.config/pypoetry/:/root/.config/pypoetry/:ro \
        -v ~/.local/share/python_keyring/:/root/.local/share/python_keyring/:ro \
        ${IMAGE_NAME}:poetry bash -c "source <(ssh-agent) > /dev/null && ssh-add > /dev/null 2>&1 && keyring get poetry-repository-dfartifactory $ARTIFACTORY_USERNAME")
    ARTIFACTORY_API_KEY=${ARTIFACTORY_API_KEY%$'\r'}
fi

# Prompt for credentials
if [ -z "$ARTIFACTORY_USERNAME" ]; then
    read -p "Artifactory Username: " ARTIFACTORY_USERNAME
fi
if [ -z "$ARTIFACTORY_API_KEY" ]; then
    read -s -p "Artifactory API key: " ARTIFACTORY_API_KEY
fi

#Build the docker
ARTIFACTORY_USERNAME="${ARTIFACTORY_USERNAME}" ARTIFACTORY_API_KEY="${ARTIFACTORY_API_KEY}" docker build --pull --build-arg ARTIFACTORY_USERNAME --build-arg ARTIFACTORY_API_KEY --build-arg PKG=/dist/*.whl -t ${IMAGE_NAME}:local .
