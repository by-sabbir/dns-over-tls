# DNS to DNS-over-TLS Proxy
---

## Features
- Accepts multiple client request
- Handles Both TCP and UDP requests using multithreading
- Logs for client query, answer from DNS server, and errors

## Requirements
- Python3
- Docker
- SSL certificate (included)

## Usage
---
#### 1. Makefile
- Build
```bash
  make build
```
- Run
```bash
  make run
```
- Test: UDP, TCP proxies, and multiple request
```bash
  make test-tcp
  make test-udp
  make multiple-client
```
- Inspect Logs
```bash
  make logs
```
- Cleanup Workspace
```bash
  make cleanup
```

> Makefile contains two variables- `SERVICE_NAME` and `SERVICE_PORT` to mitigate conflicts as port `53` is a common port and in most server, systemd resolver may already use the port by default.

#### 2. Docker
- Build
```bash
  docker build -t dns-over-tcp-proxy .
```
- Run
```bash
  docker run -itd -p 53:53/tcp -p 53:53/udp dns-over-tcp-proxy
```
- Test: UDP, TCP proxies
```bash
  dig @0.0.0.0 sabbir.dev        # for UDP
  dig @0.0.0.0 sabbir.dev +tcp   # for TCP
```

> I have also hosted this dns proxy in my server, so that we can try it in the wild,
```bash
  dig @13.251.211.39 sabbir.dev +tcp   # tcp test
  dig @13.251.211.39 sabbir.dev        # udp test
```

## Improvements
- Cache middlewire to decrease latency
- IP Block whitelist/blacklist
- Block malicious servers
- DDoS protection