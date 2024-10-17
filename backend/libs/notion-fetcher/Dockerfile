FROM clux/muslrust:stable as builder
WORKDIR /app
COPY ./src/ /app/src
COPY ./Cargo.toml .
COPY ./Cargo.lock  .

RUN cargo build --target x86_64-unknown-linux-musl --release
RUN cp /app/target/x86_64-unknown-linux-musl/release/notion-fetcher /app

FROM alpine:latest
COPY --from=builder /app/notion-fetcher /usr/local/bin/notion-fetcher
RUN apk add ca-certificates fuse3 sqlite

# Get litefs
COPY --from=flyio/litefs:0.5 /usr/local/bin/litefs /usr/local/bin/litefs
WORKDIR /app

COPY litefs.yml /etc/litefs.yml

EXPOSE 3002

ENTRYPOINT litefs mount
