FROM python:3-slim-bullseye

LABEL maintainer="mero.mero.guero@gmail.com"
LABEL org.opencontainers.image.authors='mero.mero.guero@gmail.com'
LABEL org.opencontainers.image.url='https://github.com/mmguero/montag'
LABEL org.opencontainers.image.source='https://github.com/mmguero/montag'
LABEL org.opencontainers.image.title='mmguero/montag'
LABEL org.opencontainers.image.description='Dockerized E-Book Profanity Scrubber'

ENV DEBIAN_FRONTEND noninteractive
ENV TERM xterm
ENV PYTHONUNBUFFERED 1

ADD . /usr/local/src/montag-cleaner

RUN echo "deb http://deb.debian.org/debian bullseye-backports main" >> /etc/apt/sources.list && \
    apt-get update -q && \
    apt-get -y install -qq --no-install-recommends \
      ca-certificates \
      curl \
      xvfb \
      libmagic1 \
      imagemagick \
      python3-magic \
      python3-ebooklib \
      xz-utils && \
    python3 -m ensurepip && \
      python3 -m pip install --no-cache /usr/local/src/montag-cleaner && \
    bash -c 'curl -sSL https://raw.githubusercontent.com/kovidgoyal/calibre/master/setup/linux-installer.py | python3 -c "import sys; main=lambda:sys.stderr.write(\"Download failed\n\"); exec(sys.stdin.read()); main()"' && \
    apt-get clean && \
      rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/cache/*/* /usr/local/src/montag-cleaner

ENTRYPOINT ["montag"]
CMD []
