FROM python:3-stretch

LABEL maintainer "Seth Grover <sethdgrover@gmail.com>"

ENV DEBIAN_FRONTEND noninteractive

ADD profanity_filter.patch /tmp/profanity_filter.patch

RUN apt-get update && \
    apt-get install -y libhunspell-dev curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install -r https://raw.githubusercontent.com/rominf/profanity-filter/master/requirements-deep-analysis.txt && \
    pip install profanity-filter && \
    pip install pyunpack entrypoint2 patool && \
    python -m spacy download en && \
    cd /usr/local/lib/python3.7/site-packages/profanity_filter && \
    bash -c "patch -p0 < /tmp/profanity_filter.patch" && \
    rm -f /tmp/profanity_filter.patch && \
    chmod +x /usr/local/lib/python3.7/site-packages/profanity_filter/console.py

ADD en_profane_words.txt /usr/local/lib/python3.7/site-packages/profanity_filter/data/
ADD https://cgit.freedesktop.org/libreoffice/dictionaries/plain/en/en_US.aff /usr/local/lib/python3.7/site-packages/profanity_filter/data/en.aff
ADD https://cgit.freedesktop.org/libreoffice/dictionaries/plain/en/en_US.dic /usr/local/lib/python3.7/site-packages/profanity_filter/data/en.dic

ENTRYPOINT ["/usr/local/lib/python3.7/site-packages/profanity_filter/console.py"]
CMD []