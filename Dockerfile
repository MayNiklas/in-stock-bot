ARG ARCH=
FROM ${ARCH}python:3.8

# make a full upgrade
RUN apt-get update && apt-get -y upgrade

# install project dependencies
RUN apt-get install -y python3-pip unzip

# install Google Chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get -y install google-chrome-stable

# Install ChromeDriver.
RUN LATEST_VERSION=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
 wget -N https://chromedriver.storage.googleapis.com/$LATEST_VERSION/chromedriver_linux64.zip -P ~/
RUN unzip ~/chromedriver_linux64.zip -d ~/
RUN rm ~/chromedriver_linux64.zip
RUN mv -f ~/chromedriver /usr/local/bin/chromedriver
RUN chown root:root /usr/local/bin/chromedriver
RUN chmod 0755 /usr/local/bin/chromedriver

VOLUME /app/
VOLUME /app/data/
WORKDIR /app

COPY src/requirements.txt /app/
RUN python3 -m pip install -r /app/requirements.txt
COPY src/* /app/

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
