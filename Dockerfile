FROM python:3-slim-stretch

LABEL maintainer "Seth Grover <sethdgrover@gmail.com>"

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install --no-install-recommends -y curl xvfb libmagic1 imagemagick build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install filemagic ebooklib && \
    bash -c 'curl https://raw.githubusercontent.com/kovidgoyal/calibre/master/setup/linux-installer.py | python -c "import sys; main=lambda:sys.stderr.write(\"Download failed\n\"); exec(sys.stdin.read()); main()"'

ADD montag.py /usr/local/bin/
ADD swears.txt /usr/local/bin

ENTRYPOINT ["python3", "/usr/local/bin/montag.py"]
CMD []
