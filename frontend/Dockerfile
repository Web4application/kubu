# Base image: Universal devcontainer image (good for multi-language dev)
FROM mcr.microsoft.com/devcontainers/universal:2

# Metadata labels for better traceability and provenance
LABEL org.opencontainers.image.source="https://github.com/Web4application/kubu.git"
LABEL org.opencontainers.image.description="Kubu: AI webapp blockchain multi-language dev environment."
LABEL org.opencontainers.image.maintainer="Web4application <your-email@example.com>"

# Set working directory inside container
WORKDIR /workspace/kubu

# Copy everything from the local directory to container workspace
COPY . .

# Install any dependencies if needed (example for Python, C++, Ruby)
# Adjust or remove this section based on your project requirements
RUN apt-get update && apt-get install -y \
    python3 python3-pip build-essential ruby-full \
 && pip3 install -r requirements.txt \
 && gem install bundler \
 && rm -rf /var/lib/apt/lists/*

# Build steps if any (example)
# RUN make all

# Default command to run when container starts
CMD ["bash"]
