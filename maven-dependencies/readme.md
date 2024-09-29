This directory is where the Dockerfile expects to find jar dependencies. The script that builds the Docker images will fetch dependencies and store them here, and then the Dockerfile will pick them up from this directory.

We download jars here because maven should be installed in your CI/CD environment. It's not needed at runtime.