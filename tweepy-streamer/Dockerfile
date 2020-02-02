FROM python:3.7-alpine

COPY streamers/config.py /bots/
COPY bots/favretweet.py /bots/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /streamers
CMD ["python3", "stream-tweets.py"]