# Tensorflow Installation with GPU and Anaconda

The Tensorflow [Download and Setup](https://www.tensorflow.org/versions/r0.10/get_started/os_setup.html#download-and-setup) is very thorough actually very straightforward. However, it does cover quite a lot of bases such as different ways of getting Tensorflow, different OSes, etc. 

Below is my step by step process of setting up Tensorflow to use GPU and more importantly, run Tensorflow code inside Jupyter Notebook.

At the time of writing I'm still simply running through tutorials so I haven't done anything crazy advanced yet. However, if I run into issues I will update this page with notes.

## Pre-requisites
* Anaconda Python

## Setup Steps
1. Download CUDA from https://developer.nvidia.com/cuda-downloads
2. Download cuDNN from https://developer.nvidia.com/cudnn

## WIP
1. Create a conda environment in shell (I'm using python 2.7)
```shell
$ conda create -n tensorflow python=2.7
```
2. Activate new conda environment
```shell
$ source activate tensorflow
```
3. Install using Pip (since conda only has CPU version at the time of writing)
```shell
(tensorflow)$ export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow-0.10.0-cp27-none-linux_x86_64.whl
(tensorflow)$ pip install --ignore-installed --upgrade $TF_BINARY_URL
```