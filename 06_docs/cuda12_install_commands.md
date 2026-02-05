# CUDA 12 Installation Commands (Ubuntu 24.04 / Pop!_OS)

**Status check (2026-02-05)**  
- **NVIDIA driver 580**: Already installed (580.119.02, `nvidia-driver-580-open`). No action needed.  
- **CUDA Toolkit**: Not installed (no `nvcc`, no `/usr/local/cuda`). Install using the steps below.

Run the following in your terminal (sudo required).

## 1. Add NVIDIA CUDA repository

```bash
cd /tmp
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
```

## 2. Update and install CUDA 12 toolkit

```bash
sudo apt update
sudo apt install -y cuda-toolkit-12-8
```

If `cuda-toolkit-12-8` is not found, list available CUDA 12 packages:

```bash
apt-cache search cuda-toolkit | grep 12
```

Then install the desired package (e.g. `cuda-toolkit-12-6`).

## 3. Set up environment (add to `~/.bashrc` or run in shell)

```bash
export PATH=/usr/local/cuda-12.8/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```

If you installed a different 12.x version (e.g. 12.6), replace `12.8` with that version.

## 4. Verify

```bash
nvcc --version
nvidia-smi
```

## Optional: Create `/usr/local/cuda` symlink

If your apps expect `/usr/local/cuda`:

```bash
sudo ln -sf /usr/local/cuda-12.8 /usr/local/cuda
```

(Adjust `12.8` if you installed another 12.x version.)
