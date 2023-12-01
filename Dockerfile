# FROM nvidia/cuda:12.0.0-devel-ubuntu20.04
FROM nvidia/cuda:12.0.0-cudnn8-devel-ubuntu22.04

RUN apt-get update && apt-get install -y wget
RUN apt-get install -y python3-pip python3-dev

RUN pip3 install notebook
RUN python3 -m pip install paddlepaddle-gpu==2.5.2.post120 -f https://www.paddlepaddle.org.cn/whl/linux/cudnnin/stable.html
RUN apt-get install git ffmpeg libsm6 libxext6  -y

RUN export SHELL=/bin/bash
RUN ln -s /usr/bin/python3 /usr/bin/python

# paddleseg
RUN mkdir -p /home/PaddleSeg
WORKDIR /home/PaddleSeg
COPY . .
RUN pip3 install -r requirements.txt
RUN pip3 install -v -e .
RUN pip3 install paddleseg

# flask
EXPOSE 5000


# notebooks
EXPOSE 8888

VOLUME /notebooks
WORKDIR /notebooks

# Run Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root"]


# https://developer.download.nvidia.com/compute/cudnn/secure/8.9.1/local_installers/12.x/cudnn-local-repo-ubuntu2004-8.9.1.23_1.0-1_amd64.deb?QdzzSVnG_inA2QnYi8Bs6Stg1dhEW86q4OTs9RRpC4bvDgQMROKcbF_vNGw1W84BsIv6P7Ots5mKmTJBzgNKNxR0je4Kkm6L_e57TT3ZW0TqLwDY94LQLmc-fCPEqQNdiENenpDJTXejB9Y_1-eYbLnMDPfhfKnZShQZe0-dKRx_MJJojOAvR5gUTHOItEWD0ordhv7IkN_4pTWU8eZee0QH358=&t=eyJscyI6ImdzZW8iLCJsc2QiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyJ9
# apt-get install libcudnn8=8.9.1-1+cuda12.0
#
#
#
