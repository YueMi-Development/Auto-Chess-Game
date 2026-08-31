FROM rust:1.82-slim AS builder

WORKDIR /app

ARG CARGO_HOME=/usr/local/cargo
ENV CARGO_HOME=/usr/local/cargo

COPY Cargo.toml Cargo.lock* ./
COPY src ./src
COPY proto ./proto
COPY build.rs ./

RUN cargo build --release && \
    cp target/release/backend-matchmaking /app/

FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    libssl3 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/backend-matchmaking /usr/local/bin/

ENV RUST_LOG=info
EXPOSE 8083

CMD ["backend-matchmaking"]
