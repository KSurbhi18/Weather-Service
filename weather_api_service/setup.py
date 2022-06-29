from setuptools import setup

setup(
    name='weather_api_service',
    packages=['weather_api_service'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)