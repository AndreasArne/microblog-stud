# syntax=docker/dockerfile:1.4
#
# Development environment for the devops course.
#
# Tools are added to this file kmom by kmom, when the course reaches the kmom
# that needs them. Every tool version is a build arg without a default. The
# values are set in one place, devcontainer.json, and the build fails if one of
# them is empty. The Docker CLI is not installed here, see devcontainer.json.

ARG PYTHON_IMAGE
FROM ${PYTHON_IMAGE}

ARG TARGETARCH
ARG COMPOSE_VERSION

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Refuse to build with unpinned tools.
RUN <<EOF
    for v in COMPOSE_VERSION; do
        if [ -z "${!v}" ]; then
            echo "Build arg ${v} is empty. Set it in .devcontainer/devcontainer.json" >&2
            exit 1
        fi
    done
EOF

# Basic tools, versions follow the base image.
RUN <<EOF
    apt-get update
    apt-get install -y --no-install-recommends ca-certificates curl git make openssh-client
    rm -rf /var/lib/apt/lists/*
EOF

# Docker Compose, pinned here. The Docker CLI is installed, and pinned, by the
# docker-outside-of-docker feature in devcontainer.json, which also gives the
# non-root user access to the host's Docker socket. This plugin is found before
# the one the feature installs. `docker-compose` is linked because the course
# material uses that command.
RUN <<EOF
    case "${TARGETARCH}" in
        amd64) COMPOSE_ARCH=x86_64 ;;
        arm64) COMPOSE_ARCH=aarch64 ;;
        *) echo "Unsupported architecture ${TARGETARCH}" >&2; exit 1 ;;
    esac
    mkdir -p /usr/local/lib/docker/cli-plugins
    curl -fsSL -o /usr/local/lib/docker/cli-plugins/docker-compose \
        "https://github.com/docker/compose/releases/download/v${COMPOSE_VERSION}/docker-compose-linux-${COMPOSE_ARCH}"
    chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
    ln -s /usr/local/lib/docker/cli-plugins/docker-compose /usr/local/bin/docker-compose
EOF

# A non-root user, so files created in the repo belong to the student. devcontainer.json
# sets remoteUser to it and the Dev Containers tooling adjusts its uid to the host user's.
RUN useradd --create-home --uid 1000 --shell /bin/bash dev

# Python packages (pytest, pylint, ...) are installed from the repo's
# requirements files into ./venv by postCreateCommand in devcontainer.json.
