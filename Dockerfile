FROM pytorch/pytorch:1.8.1-cuda11.1-cudnn8-devel
RUN rm /etc/apt/sources.list.d/cuda.list
RUN rm /etc/apt/sources.list.d/nvidia-ml.list
RUN apt update
RUN apt install -y wget
RUN apt-key del 7fa2af80
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-keyring_1.0-1_all.deb
RUN dpkg -i cuda-keyring_1.0-1_all.deb
RUN apt update
RUN apt install -y gnupg2 apt-utils curl lsb-release
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt install -y python3-opencv git
RUN pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu111/torch1.8/index.html

RUN /bin/bash -c "pip install 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'"
RUN pip3 install scikit-image seaborn numpy
RUN mkdir /app
WORKDIR /app
