# ROS2-Based Thermal Camera Driver and Data Acquisition Node
[YouTube Demo](https://youtu.be/_SpAnm0MlPA)

A complete ROS2 Humble driver for the **UNI-T UTi721M** thermal camera, deployed on an **NVIDIA Jetson Orin Nano**. The system publishes calibrated per-pixel temperature data through standard ROS2 topics and serves as the thermal sensing layer of a UAV-based forest fire detection pipeline.

> **Graduation Thesis — B2 Project**  
> Erdem Kandilci · Computer Engineering · Cukurova University · 2026  
> Advisor: Lect. PhD Yunus Emre Cogurcu

---

## Key Contributions

- Discovery and documentation of the UTi721M **split-frame data structure** (256x384 composite frame encoding pseudocolor image + 16-bit raw temperature matrix)
- Empirical validation of the calibration formula **T(C) = raw / 64.0 - 273.15**
- Real-time ROS2 pipeline achieving sustained **25 FPS** on the Jetson Orin Nano across 4 simultaneous topics
- Characterization of a **~1.0 C/m** linear distance-dependent temperature decrease for future UAV altitude correction

---

## Hardware Requirements

| Component | Details |
|-----------|---------|
| Thermal Camera | UNI-T UTi721M (USB 2.0 / UVC) |
| Deployment Platform | NVIDIA Jetson Orin Nano (8 GB) |
| Development Platform | Any Ubuntu 22.04 machine |

---

## Software Requirements

| Component | Version |
|-----------|---------|
| Ubuntu | 22.04 LTS |
| ROS2 | Humble Hawksbill |
| Python | 3.10 |
| OpenCV | 4.5.4 |
| cv_bridge | Humble |
| image_transport | Humble |
| rosbag2 | Humble |

---

## Installation

```bash
sudo apt install ros-humble-desktop
sudo apt install python3-colcon-common-extensions
sudo apt install ros-humble-cv-bridge ros-humble-image-transport
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/ErdemKand/thermal-camera-ros2-driver
cd ~/ros2_ws
colcon build --packages-select thermal_camera_driver
source install/setup.bash
```

---

## Camera Verification

```bash
lsusb
ls /dev/video*
v4l2-ctl --device=/dev/video0 --list-formats-ext
```

Expected output includes: `YUYV 4:2:2, 256x384 @ 25 FPS`

---

## Running the Driver

```bash
ros2 launch thermal_camera_driver thermal_camera.launch.py
```

For a different device path:

```bash
ros2 launch thermal_camera_driver thermal_camera.launch.py device:=/dev/video1
```

Verify topics:

```bash
ros2 topic list
ros2 topic hz /thermal/image_raw
```

---

## ROS2 Topic Structure

| Topic | Message Type | Description |
|-------|-------------|-------------|
| `/thermal/image_raw` | `sensor_msgs/Image` | Grayscale image from upper frame half (bgr8) |
| `/thermal/image_raw16` | `sensor_msgs/Image` | 16-bit raw temperature array (mono16) |
| `/thermal/temperature_map` | `sensor_msgs/Image` | Calibrated per-pixel temperature in C (32FC1) |
| `/thermal/temperature_map/visual` | `sensor_msgs/Image` | False-color temperature map with dynamic scale (bgr8) |

---

## Split-Frame Data Structure

The UTi721M delivers a single **256x384 composite frame** via V4L2 (YUYV 4:2:2):

```
+-------------------------+
|   Upper half (256x192)  |  ->  Pseudocolor BGR image (camera firmware)
+-------------------------+
|   Lower half (256x192)  |  ->  16-bit raw temperature data
+-------------------------+
```

16-bit raw value reconstruction:

```python
raw = blue_channel + (green_channel * 256)
```

---

## Temperature Calibration

```python
T(C) = raw / 64.0 - 273.15
```

Validation results:

| Target | Reference (C) | Camera (C) | Error (C) |
|--------|--------------|------------|-----------|
| Cold water (ice) | 1.7 | 1.7 | 0.0 |
| Room temperature water | 27.0 | 27.0 | 0.0 |
| Hot water | 78.0 | 72.0 | 6.0 |
| Human body surface | ~36.5 | ~36.0 | <1.0 |
| Lighter flame | N/A | 119.8-190.0 | N/A |

---

## Data Recording

```bash
ros2 bag record /thermal/image_raw /thermal/image_raw16 /thermal/temperature_map /thermal/temperature_map/visual -o thermal_recording
ros2 bag info thermal_recording/
ros2 bag play thermal_recording/
```

---

## Package Structure

```
thermal_camera_driver/
├── thermal_camera_driver/
│   ├── thermal_camera_driver_node.py
│   └── temperature_map_node.py
├── config/
│   └── camera_params.yaml
├── launch/
│   └── thermal_camera.launch.py
├── docs/
│   └── development_notes.md
├── package.xml
└── setup.py
```

---

## System Architecture

<img width="872" height="376" alt="Ekran görüntüsü 2026-05-22 095441" src="https://github.com/user-attachments/assets/10b9e922-7120-4e76-af0e-e5b5c13a036e" />
