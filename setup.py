from setuptools import setup

setup(
    name='my_finances',
    version='1.0',
    long_description=__doc__,
    packages=['app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
      'Flask==1.1.2',
      'mysql-connector-python==8.0.20',
    ]
)
