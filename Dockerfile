# Use an official Ubuntu as a parent image
FROM ubuntu:latest

# Update the system and install dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common

# Update the system and install Python and build dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    gcc \
    curl \
    sqlite3 \
    gdb \
    libssl-dev \
    git

ENV DEBIAN_FRONTEND noninteractive

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Ensure uv is in path
ENV PATH="/root/.local/bin:${PATH}"

# Create a default venv for basic tests
RUN uv venv "/root/.venv"

# Could add some basic dependencies to venv here too

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Ensure Rust binaries are in PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Set the working directory in the container
WORKDIR /usr/src/app

# Any additional commands or environment variables can be added here

# Command to run when the container launches
CMD ["/bin/bash", "-c", "source /root/.venv/bin/activate && exec bash"]
