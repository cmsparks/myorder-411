from setuptools import setup

setup(
    name='myorder_server',
    packages=['myorder_server'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
