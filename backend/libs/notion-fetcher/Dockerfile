FROM rust:1.80.0 as builder
WORKDIR /app
COPY ./src/ /app/src
COPY ./Cargo.toml .
COPY ./Cargo.lock  .

RUN cargo install --path . --root /usr/local/cargo/

FROM debian:bookworm  AS final
COPY --from=builder /usr/local/cargo/bin/notion-fetcher /usr/local/bin/notion-fetcher
RUN apt-get update -y && apt-get install -y ca-certificates fuse3 sqlite3
# RUN apk add ca-certificates fuse3 sqlite

# Get litefs
COPY --from=flyio/litefs:0.5 /usr/local/bin/litefs /usr/local/bin/litefs
WORKDIR /app

COPY litefs.yml /etc/litefs.yml

EXPOSE 3002

ENTRYPOINT litefs mount
