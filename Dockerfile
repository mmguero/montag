FROM python:3-slim-stretch

LABEL maintainer "mmguero <tlacuache@gmail.com>"

ENV DEBIAN_FRONTEND noninteractive

ADD requirements.txt /tmp/montag-requirements.txt

RUN apt-get update && \
    apt-get install --no-install-recommends -y curl xvfb libmagic1 imagemagick build-essential && \
    pip3 install -r /tmp/montag-requirements.txt && \
    rm -f /tmp/montag-requirements.txt && \
    bash -c 'curl https://raw.githubusercontent.com/kovidgoyal/calibre/master/setup/linux-installer.py | python -c "import sys; main=lambda:sys.stderr.write(\"Download failed\n\"); exec(sys.stdin.read()); main()"' && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/*

ADD montag.py /usr/local/bin/
ADD swears.txt /usr/local/bin

ENTRYPOINT ["python3", "/usr/local/bin/montag.py"]
CMD []
