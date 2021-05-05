import os

CUDA_PATH = "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.0\\bin"
CUDNN_PATH = "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDNN\\8.0.4_for_cuda_11.0\\bin"

path = os.environ["path"]
if path.find(CUDA_PATH) == -1:
    path = ";".join((CUDA_PATH, path))
if path.find(CUDNN_PATH) == -1:
    path = ";".join((CUDNN_PATH, path))
os.environ["path"] = path
