FROM nvidia/cuda:12.0.0-cudnn8-devel-ubuntu22.04

# Install necessary packages
RUN apt-get update && \
    apt-get install -y wget python3-pip python3-dev git ffmpeg libsm6 libxext6

# Install Python packages
RUN python3 -m pip install paddlepaddle==2.6.0 -i https://mirror.baidu.com/pypi/simple
RUN pip3 install waitress
RUN pip3 install paddleseg

# Set up a shell variable
ENV SHELL=/bin/bash

# Link python3 to python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Set up PaddleSeg
RUN mkdir -p /home/PaddleSeg
WORKDIR /home/PaddleSeg

COPY ./requirements.txt ./
RUN chmod +x requirements.txt
# Install Python dependencies from requirements
RUN pip3 install -r requirements.txt

# Install and configure waitress for production
COPY . .
RUN pip3 install -v -e .
CMD ["waitress-serve", "--port=8080", "--call", "main:create_app"]
