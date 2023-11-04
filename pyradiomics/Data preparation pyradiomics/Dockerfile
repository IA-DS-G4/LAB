FROM radiomics/pyradiomics:CLI
MAINTAINER https://github.com/Radiomics

FROM debian:bullseye
# Install git, cmake, and a C++ compiler
RUN apt-get update && apt-get install -y \
    git \
    cmake \
    wget \
    unzip \
    build-essential \
    xutils-dev \
    default-jre \
    g++
# Update and install dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Install required dcm2niix converions tools
WORKDIR /usr/src
RUN git clone https://github.com/rordenlab/dcm2niix.git && \
  cd dcm2niix && \
  mkdir build && cd build && \
  cmake .. && \
  make install

# Install additional needed python packages
# Prevent pandas from installing version 0.25.0, as this version is unable to import
# module _lzma (in package lmza). See also https://github.com/pandas-dev/pandas/issues/27543
WORKDIR /usr/src
RUN pip3 install pandas!=0.25.0 && \
  pip3 install pydicom && \
  pip3 install pyradiomics && \
RUN pip3 install wget
RUN pip3 install requests

WORKDIR /usr/src
RUN apt-get install -y dcmtk
RUN apt-get install -y plastimatch

# Copy the required DCMQI tools from the latest DCMQI docker image
COPY --from=qiicr/dcmqi:v1.2.2 /usr/bin/tid1500writer /usr/bin/segimage2itkimage /usr/bin/
# Copy the pyradiomics-dcm.py script to ensure latest changes are included in the image
COPY ./labs/pyradiomics-dcm/* /usr/src/pyradiomics/labs/pyradiomics-dcm/

WORKDIR /usr/src/pyradiomics/labs/pyradiomics-dcm
ENTRYPOINT ["python3", "pyradiomics-dcm.py"]

