FROM python:3-slim-stretch

LABEL maintainer "Seth Grover <sethdgrover@gmail.com>"

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install --no-install-recommends -y libhunspell-dev curl xvfb libmagic1 imagemagick git build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install -r https://raw.githubusercontent.com/mmguero/profanity-filter/master/requirements-deep-analysis.txt && \
    pip install git+https://github.com/mmguero/profanity-filter && \
    pip install pyunpack entrypoint2 patool filemagic ebooklib && \
    python -m spacy download en && \
    cd /usr/local/lib/python3.7/site-packages/profanity_filter && \
    bash -c 'curl https://raw.githubusercontent.com/kovidgoyal/calibre/master/setup/linux-installer.py | python -c "import sys; main=lambda:sys.stderr.write(\"Download failed\n\"); exec(sys.stdin.read()); main()"'

ADD cleanbook.py /usr/local/bin/cleanbook.py
ADD en_profane_words.txt /usr/local/lib/python3.7/site-packages/profanity_filter/data/
ADD https://cgit.freedesktop.org/libreoffice/dictionaries/plain/en/en_US.aff /usr/local/lib/python3.7/site-packages/profanity_filter/data/en.aff
ADD https://cgit.freedesktop.org/libreoffice/dictionaries/plain/en/en_US.dic /usr/local/lib/python3.7/site-packages/profanity_filter/data/en.dic

ENTRYPOINT ["python3", "/usr/local/bin/cleanbook.py"]
CMD []