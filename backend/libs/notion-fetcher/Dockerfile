# FROM rust:1.80.0 as builder
# WORKDIR /app
# COPY ./src/ /app/src
# COPY ./Cargo.toml .
# COPY ./Cargo.lock  .
# RUN cargo install --path . --root /usr/local/cargo/

# FROM rust:1.80.0
# WORKDIR /app
# COPY . .

FROM python:3.9-slim
RUN apt-get update -y && apt-get install -y ca-certificates fuse3 sqlite3
COPY --from=flyio/litefs:0.5 /usr/local/bin/litefs /usr/local/bin/litefs
WORKDIR /app

COPY litefs.yml /etc/litefs.yml

EXPOSE 2000

ENTRYPOINT litefs mount
CMD [ "python3", "-m", "http.server","2000" ]
