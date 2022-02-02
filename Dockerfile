FROM python:3.9

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt &&\
    curl -Lo kubent.tar.gz https://github.com/doitintl/kube-no-trouble/releases/download/nightly-0.5.1-15-g13702ac/kubent-nightly-0.5.1-15-g13702ac-linux-amd64.tar.gz && \
    tar -zxvf kubent.tar.gz && \
    mv kubent /usr/local/bin/ && \
    rm -rf kubent*

COPY ./src /app/src

CMD [ "python", "src" ]