# Start from an NVIDIA CUDA image
FROM nvidia/cuda:12.0.0-devel-ubuntu20.04

# Install necessary packages
RUN apt-get update && apt-get install -y wget

# Download and install cuDNN (replace this with the actual commands to install cuDNN v8.1.1)
# Note: You need to follow NVIDIA's instructions and comply with their terms of service.
# The below commands are placeholders and need to be replaced with actual download and install commands.

# Install Jupyter Notebook
RUN apt-get install -y python3-pip python3-dev
RUN pip3 install notebook

# RUN wget [CUDNN_DOWNLOAD_LINK] && \
#     tar -xzvf [CUDNN_TAR_FILE] && \
#     cp cuda/include/cudnn*.h /usr/local/cuda/include && \
#     cp cuda/lib64/libcudnn* /usr/local/cuda/lib64 && \
#     chmod a+r /usr/local/cuda/include/cudnn*.h /usr/local/cuda/lib64/libcudnn*

# Expose port for Jupyter Notebook
EXPOSE 8888

# Set up the volume directory
VOLUME /notebooks
WORKDIR /notebooks

# Run Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
