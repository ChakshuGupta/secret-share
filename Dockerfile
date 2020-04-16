FROM ubuntu:18.04

RUN apt-get -y update && apt-get -y upgrade && apt-get -y install \
    git \
    mesa-common-dev \
    mesa-utils \
    libgl1-mesa-glx\
    python3.7 \
    python3.7-dev \
    python3-pip \
    python3-pyqt5 \
    pyqt5-dev \
    pyqt5-dev-tools

RUN git clone https://github.com/ChakshuGupta/secret-share.git
WORKDIR /secret-share

RUN pip3 install -r requirements.txt
RUN python3 setup.py develop
ENV QT_X11_NO_MITSHM=1

WORKDIR /secret-share/secret-shares-app/
CMD ["python3", "secret_share_app.py"]