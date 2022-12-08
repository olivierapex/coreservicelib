ARG IMAGE_NAME=python:3.8-buster
FROM $IMAGE_NAME AS base

    USER root

    RUN apt-get update \
        # Install ldap tools (https://www.python-ldap.org/en/python-ldap-3.2.0/installing.html#debian)
        && DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
        parallel \
        # Clean up
        && apt-get autoremove -y \
        && apt-get clean -y \
        && rm -rf /var/lib/apt/lists/*

FROM base as with_poetry
    ARG ARTIFACTORY_USERNAME
    ARG ARTIFACTORY_API_KEY
    RUN echo "machine ${ARTIFACTORY_URL}" >> ~/.netrc \
        && echo "    login ${ARTIFACTORY_USERNAME}" >> ~/.netrc \
        && echo "    password ${ARTIFACTORY_API_KEY}" >> ~/.netrc \
        && echo "machine ${ARTIFACTORY_URL}" >> ~/.netrc \
        && echo "    login ${ARTIFACTORY_USERNAME}" >> ~/.netrc \
        && echo "    password ${ARTIFACTORY_API_KEY}" >> ~/.netrc

    RUN mkdir -p /root/.pip
    COPY ci/pip.conf /root/.pip/pip.conf

     # Always keep poetry version in sync between pyproject.toml, Dockerfile and .devcontainer/Dockerfile
    ARG POETRY_VERSION=1.1.6
    ARG SAGECIPHER_VERSION=0.7.5
    ARG TOM_CLI_VERSION=0.1.3

    RUN pip3 --disable-pip-version-check --no-cache-dir install poetry==$POETRY_VERSION sagecipher==$SAGECIPHER_VERSION toml-cli==$TOM_CLI_VERSION \
        && poetry config virtualenvs.create false

FROM with_poetry as with_package
    ARG ARTIFACTORY_USERNAME
    ARG ARTIFACTORY_API_KEY

    ARG POETRY_HTTP_BASIC_DFARTIFACTORY_USERNAME=$ARTIFACTORY_USERNAME
    ARG POETRY_HTTP_BASIC_DFARTIFACTORY_PASSWORD=$ARTIFACTORY_API_KEY

    # Always install exact dependencies versions from lock file
    COPY pyproject.toml /dist/pyproject.toml
    COPY poetry.lock /dist/poetry.lock
    RUN cd /dist; \
        poetry install --no-dev --no-root;

    # build arg PKG override toward wheel local file. VERSION -> artifactory
    ARG VERSION
    ARG PKG=coreservicelib==${VERSION}
    # what is the pupose of the next line?
    #COPY dist /dist
    RUN bash -c "ls -l ~/.pip"
    RUN bash -c "time pip3 install --no-dependencies $PKG"

FROM base

    COPY --from=with_package /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
    COPY --from=with_package /usr/local/bin/ /usr/local/bin

#    ENTRYPOINT ["rbac_serv"]
