from setuptools import find_packages, setup

package_name = 'thermal_camera_driver'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='erdem',
    maintainer_email='erdem@todo.todo',
    description='TODO: Package description',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'fake_thermal_publisher = thermal_camera_driver.fake_thermal_publisher:main',
	    'image_publisher = thermal_camera_driver.image_publisher:main',
	    'video_publisher = thermal_camera_driver.video_publisher:main',
	    'thermal_camera_driver_node = thermal_camera_driver.thermal_camera_driver_node:main',
	],
    },
)
