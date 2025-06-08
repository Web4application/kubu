# KubuVerse

## The AI-powered Multi-language Blockchain Webapp Dev Environment

KubuVerse unites the best of AI, blockchain, and multi-language development into a seamless, powerful platform. Build smarter, faster, and decentralized — no compromises.

---

### Features

- **AI-Assisted Development:** Code suggestions, auto-completion, and intelligent automation powered by cutting-edge AI.  
- **Multi-language Support:** Python, JavaScript, Rust, Dart, and more — all in one dev environment.  
- **Blockchain Integration:** Native support for smart contracts, decentralized apps, and blockchain transactions.  
- **Open Source & Community Driven:** Collaborate, contribute, and innovate alongside a growing ecosystem.

---


# 🌐 Kubuverse

**Kubuverse** is a scalable, AI-powered, multi-architecture application platform built with FastAPI, PostgreSQL, Docker, and GitHub Actions. It’s designed for modern deployments, secure supply chains, and extensible microservices.

> “Where ideas scale and compute becomes culture.”

---

## 🚀 Features

- ⚡️ **FastAPI backend** — blazing-fast Python web API framework
- 🗃 **PostgreSQL** — production-grade relational DB with Alembic migrations
- 🔁 **Redis** — caching and job queueing (optional)
- 🐋 **Multi-Arch Docker Support** — supports `linux/amd64` and `linux/arm64`
- 🔐 **Cosign signing** — secure container provenance using Sigstore
- 🌍 **i18n-ready** — FastAPI Accept-Language detection & content negotiation
- 🛠 **GitHub Actions CI/CD** — automated build, sign, and push to GHCR
- 🌐 **Kubernetes-native** — full deployment manifests and Helm-ready

---

## 🧰 Tech Stack

| Layer      | Tech           |
|------------|----------------|
| Backend    | FastAPI, Pydantic |
| Database   | PostgreSQL + Alembic |
| Cache/Queue| Redis (optional) |
| DevOps     | Docker, Buildx, Cosign |
| CI/CD      | GitHub Actions |
| Infra      | Kubernetes (with LoadBalancer) |

---

## 📦 Container Registry

Images are published to:

```

ghcr.io/web4application/kubuverse\:latest

````

Multi-arch support: ✅  
Signed with Cosign: ✅

---

## 🛠 Development Setup

```bash
git clone https://github.com/Web4application/kubuverse.git
cd kubuverse
docker-compose up --build
````

Local access: `http://localhost:8000`

---

## 🛡 Production Deployment

```bash
kubectl apply -f deploy/kubuverse-deployment.yaml
```

Image is automatically built, pushed, and signed by [`.github/workflows/ci-cd.yaml`](./.github/workflows/ci-cd.yaml).

---

## 🔐 Security & Signing

Kubuverse uses **Cosign** to sign and verify container images.
See: [`deploy/build_sign_push.sh`](./deploy/build_sign_push.sh)

```bash
cosign verify --key cosign.pub ghcr.io/web4application/kubuverse:latest
```

---

## 📚 Docs

* [API Reference](docs/api.md)
* [Database Models](docs/models.md)
* [I18N Routing Guide](docs/i18n.md)

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feat/my-feature`)
3. Commit your changes
4. Push and create a PR

All contributions must pass formatting and type checks.

---

## 📄 License

MIT License © Web4Application

---

## 🌌 Vision

Kubuverse is not just an app — it's an **AI-native compute culture**.
It’s what happens when DevOps, data, and distributed systems come together under one sovereign deployment.
