FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    socat \
    gcc \
    make \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m ctfuser

WORKDIR /challenge

# Copy source files first
COPY vulnerable_vm_service.c .
COPY flag.txt .
COPY run_service.sh .
COPY compile_service.sh .

# Compile inside the container to ensure GLIBC compatibility
RUN chmod +x compile_service.sh && ./compile_service.sh

RUN chmod +x vulnerable_service run_service.sh
RUN chown -R ctfuser:ctfuser /challenge

USER ctfuser

EXPOSE 4444

CMD ["./run_service.sh"]
