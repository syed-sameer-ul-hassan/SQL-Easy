FROM python:3.11-slim

LABEL maintainer="syed-sameer-ul-hassan"
LABEL description="SQL Easy - Automated SQL Injection Framework"
LABEL version="1.2.0"

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget unzip curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir sqlmap arjun

WORKDIR /opt/sqleasy
COPY . .

ARG ARCH=amd64
RUN set -ex \
    && wget -q "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_${ARCH}.zip" -O /tmp/subfinder.zip \
    && unzip -q /tmp/subfinder.zip subfinder -d /usr/local/bin/ && chmod +x /usr/local/bin/subfinder \
    && wget -q "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_${ARCH}.zip" -O /tmp/httpx.zip \
    && unzip -q /tmp/httpx.zip httpx -d /usr/local/bin/ && chmod +x /usr/local/bin/httpx \
    && wget -q "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_${ARCH}.zip" -O /tmp/katana.zip \
    && unzip -q /tmp/katana.zip katana -d /usr/local/bin/ && chmod +x /usr/local/bin/katana \
    && wget -q "https://github.com/projectdiscovery/nuclei/releases/download/v3.3.9/nuclei_3.3.9_linux_${ARCH}.zip" -O /tmp/nuclei.zip \
    && unzip -q /tmp/nuclei.zip nuclei -d /usr/local/bin/ && chmod +x /usr/local/bin/nuclei \
    && wget -q "https://github.com/lc/gau/releases/download/v2.2.4/gau_2.2.4_linux_${ARCH}.tar.gz" -O /tmp/gau.tar.gz \
    && tar -xzf /tmp/gau.tar.gz -C /usr/local/bin/ gau && chmod +x /usr/local/bin/gau \
    && rm -rf /tmp/*.zip /tmp/*.tar.gz

RUN mkdir -p /root/.config/sqleasy \
    && echo "/opt/sqleasy" > /root/.config/sqleasy/path \
    && cp sqleasy /usr/local/bin/sqleasy \
    && chmod +x /usr/local/bin/sqleasy

VOLUME ["/data"]
WORKDIR /data

ENTRYPOINT ["sqleasy"]
CMD ["help"]
