# Use a lightweight Ubuntu base image
FROM ubuntu:20.04

# Set noninteractive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    blender \
    python3 \
    python3-pip \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Set Python3 as default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Copy application and Blender script into the container
COPY app.py /app/
COPY enhance_screen_recording.py /app/
WORKDIR /app

# Expose Flask server port
EXPOSE 5000

# Define entrypoint to run Flask app
CMD ["python3", "app.py"]