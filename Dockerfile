FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

ENV PYTHONUNBUFFERED=1 

# SYSTEM
RUN apt-get update --yes --quiet && DEBIAN_FRONTEND=noninteractive apt-get install --yes --quiet --no-install-recommends \
    software-properties-common \
    build-essential apt-utils \
    wget curl vim git ca-certificates kmod \
    nvidia-driver-525 \
 && rm -rf /var/lib/apt/lists/*

# PYTHON 3.10
RUN add-apt-repository --yes ppa:deadsnakes/ppa && apt-get update --yes --quiet
RUN DEBIAN_FRONTEND=noninteractive apt-get install --yes --quiet --no-install-recommends \
    python3.10 \
    python3.10-dev \
    python3.10-distutils \
    python3.10-lib2to3 \
    python3.10-gdbm \
    python3.10-tk \
    pip\
    gdal-bin \
    libgdal-dev \
    r-base \
    python3.10\
    python3.10-venv \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 999 \
    && update-alternatives --config python3 && ln -s /usr/bin/python3 /usr/bin/python

RUN pip install --upgrade pip

# Set R_HOME and update PATH
ENV R_HOME=/usr/lib/R
ENV PATH="${R_HOME}/bin:${PATH}"

# Create a virtual environment and activate it
RUN python3.10 -m venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install Python dependencies with NVIDIA's PyPI URL
RUN pip install --upgrade pip
RUN pip install -i https://pypi.org/simple --extra-index-url https://pypi.nvidia.com -r requirements.txt

# Install additional Python packages like ipywidgets
RUN pip install ipywidgets

# Copy the rest of the application's source code to the container
COPY . .

# Expose the port for Jupyter Notebook
EXPOSE 8811

# Command to run Jupyter Notebook and keep the container running
CMD ["sh", "-c", "jupyter notebook --ip=0.0.0.0 --port=8811 --no-browser --allow-root && tail -f /dev/null"]
