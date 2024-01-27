# Use an official Rust image as a parent image
FROM rust:latest

# Install Python and venv
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Set up a virtual environment for Python
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Set the working directory in the container
WORKDIR /workspace

# Copy the Rust project files into the container
COPY rust_project/Cargo.toml /workspace/rust_project/
COPY rust_project/src /workspace/rust_project/src

# Build the Rust project
WORKDIR /workspace/rust_project
RUN cargo build --release
# The target directory (with the built artifacts) will be inside /workspace/rust_project

# Switch back to the main workspace directory
WORKDIR /workspace

# Copy the Python project files into the container
COPY python/requirements.txt /workspace/python/

# Install Python dependencies
RUN /venv/bin/pip install -r /workspace/python/requirements.txt

# Install Jupyter and ipykernel
RUN /venv/bin/pip install jupyter ipykernel
RUN /venv/bin/python -m ipykernel install --user --name=rust-project

# Copy the rest of the Python project
COPY python/ /workspace/python/

# (Optional) Any additional setup or environment variables

# Set the default command for the container
#CMD ["your-command-here"]
