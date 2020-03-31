from setuptools import setup, find_packages

setup(
    name='app-cli',
    version='0.0.1',
    author_email='chakshugupta@gmail.com',
    packages=['shamir39'],
    package_data={},
    install_requires=[
        'click', 'pyseltongue', 'Werkzeug', 'mnemonic', 'Flask'
    ],
    entry_points={
        'console_scripts': ['shamir39 = shamir39.app_cli:main']
      }
)