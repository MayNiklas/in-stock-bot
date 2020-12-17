ARG ARCH=
FROM ${ARCH}python:3.8

#  installing project dependencies // adding google-chrome to apt sources
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add && \
  echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
  apt-get update && apt-get -y upgrade && apt-get install -y && \
  install google-chrome-stable \
  python3-pip \
  unzip


# Installing ChromeDriver
RUN LATEST_VERSION=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
  wget -N https://chromedriver.storage.googleapis.com/$LATEST_VERSION/chromedriver_linux64.zip -P ~/ && \
  unzip ~/chromedriver_linux64.zip -d ~/ && \
  rm ~/chromedriver_linux64.zip && \
  mv -f ~/chromedriver /usr/local/bin/chromedriver && \
  chown root:root /usr/local/bin/chromedriver && \
  chmod 0755 /usr/local/bin/chromedriver

VOLUME /app/
VOLUME /app/data/
WORKDIR /app

# Installing requirements before copying the code -> this way, they don't get reinstalled with every build
COPY src/requirements.txt /app/
RUN python3 -m pip install -r /app/requirements.txt
COPY src/* /app/

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
