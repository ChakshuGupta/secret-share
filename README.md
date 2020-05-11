# Shamir Secret Sharing Scheme

## Run using Docker -

```
  docker build -t shamir-app .
  docker run  -it --env="DISPLAY" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" shamir-app
```

### Install and Setup Steps-

1. Install Python and pip -

```
  sudo apt install python3.8 python3.8-dev python3-pip
```

2. Install Requiremets -

```
  pip3 install -r requirements.txt
```

3. Install PyQT -

```
  sudo apt install python3-pyqt5 pyqt5-dev pyqt5-dev-tools
```

4. Setup environment -

```
  sudo python3 setup.py develop
```

### Run API-

```
python3 app.py
```

### Run CLI -

1. Usage -

```
  shamir39 --help
  shamir39 gen --help
  shamir39 split --help
  shamir39 recover --help
```

### Run the Application

```
  cd secret-shares-app
  python3 secret_share_app.py
```
