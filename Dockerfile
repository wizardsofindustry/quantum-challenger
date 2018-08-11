FROM wizardsofindustry/quantum:latest

RUN mkdir /var/lib/challenger
RUN mkdir /var/spool/aorta

COPY . /app
COPY etc/ /etc/challenger/

WORKDIR /app
RUN python3 setup.py install

ENV QUANTUM_DEPLOYMENT_ENV development
ENV AORTA_SPOOL_DIR /var/spool/aorta
ENV CHALLENGER_SECRET_KEY b9d3fc670302b2191fd341814ee98a13ec2070657f816cf2f93d2dc282277657
ENV CHALLENGER_HTTP_ADDR 0.0.0.0
ENV CHALLENGER_HTTP_PORT 8443
ENV CHALLENGER_RUNTIME service

ENTRYPOINT ["./bin/docker-entrypoint"]
