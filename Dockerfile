FROM debian:bullseye-slim

LABEL maintainer="mero.mero.guero@gmail.com"
LABEL org.opencontainers.image.authors='mero.mero.guero@gmail.com'
LABEL org.opencontainers.image.url='https://github.com/mmguero/montag'
LABEL org.opencontainers.image.source='https://github.com/mmguero/montag'
LABEL org.opencontainers.image.title='mmguero/montag'
LABEL org.opencontainers.image.description='Dockerized E-Book Profanity Scrubber'

ENV DEBIAN_FRONTEND noninteractive

RUN echo "deb http://deb.debian.org/debian bullseye-backports main" >> /etc/apt/sources.list && \
    apt-get -q update && \
    apt-get install -q -y --no-install-recommends -t bullseye-backports \
      ca-certificates \
      curl \
      xvfb \
      libmagic1 \
      imagemagick \
      python3-minimal \
      python3-magic \
      python3-ebooklib \
      xz-utils && \
    bash -c 'curl -sSL https://raw.githubusercontent.com/kovidgoyal/calibre/master/setup/linux-installer.py | python3 -c "import sys; main=lambda:sys.stderr.write(\"Download failed\n\"); exec(sys.stdin.read()); main()"' && \
    apt-get clean && \
      rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/cache/*/*

ADD montag.py /usr/local/bin
ADD swears.txt /usr/local/bin

ENTRYPOINT ["python3", "/usr/local/bin/montag.py"]
CMD []
