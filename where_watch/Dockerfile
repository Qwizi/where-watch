FROM python:3.9.9
RUN wget -Oinit.sh https://sh.rustup.rs \
        && \
    sh init.sh -y \
        && \
    rm init.sh

ENV PATH="/root/.cargo/bin:${PATH}"

RUN rustup install nightly \
        && \
    rustup default nightly

ENV RUSTFLAGS="-C target-feature=-crt-static"
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/
