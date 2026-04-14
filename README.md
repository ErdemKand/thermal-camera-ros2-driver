# thermal-camera-ros2-driver
## 1-Project Objective
This project aims to develop a fully functional camera driver that integrates a thermal camera with the ROS2 Humble ecosystem, broadcasting image data and capable of recording and visualizing this data. The developed driver will run on the Jetson Orin Nano and is planned to be integrated with unmanned aerial vehicle (UAV)-based forest fire detection systems in later stages.
### -Things to do 
- Recognizing and reading the thermal camera via the V4L2 interface in a Linux environment(ROS2_Humble).
- Publishing image data in sensor_msgs/Image format via the /thermal/image_raw topic.
- Providing support for compressed image streams with image_transport.
- Establishing a parametric and modular structure (YAML-based configuration)
- Providing real-time visualization with RViz2.
- Creating data recording and playback infrastructure with rosbag2.
- Running the system and completing the integration on the Jetson Orin Nano.
  ## 2-
