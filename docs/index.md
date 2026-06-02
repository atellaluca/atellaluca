---
title: "Luca Atella | Software Architect, Backend Platform Engineer"
description: "Portfolio of Luca Atella, software architect and backend platform engineer focused on AWS, FastAPI, cloud-portable backend architecture, runtime contract validation, IoT and Digital Twin systems."
image: "assets/luca-atella-software-architect-backend-platform-engineer.png"
image_alt: "Luca Atella software architect and backend platform engineer portfolio"
schema_type: "ProfilePage"
---

# Luca Atella
## Software Architect · Backend & Platform Engineering

**I design backend platforms that are clear to extend, reliable in production, and not locked to one runtime or cloud provider.**

My work sits between backend engineering, system design, cloud infrastructure, and developer tooling. I like projects where the system has to last: multiple environments, real users, integrations, operational constraints, and architecture that must remain understandable after the first release.

I am based in Basilicata, Italy, and I work well with teams that need calm technical ownership across backend architecture, cloud deployment, integration-heavy systems, and long-term platform evolution.

---

<div class="portfolio-proof-grid" markdown>

<div class="portfolio-proof" markdown>
**Production platform**
A fleet management platform adopted in a real business context and designed to run locally or on AWS.
</div>

<div class="portfolio-proof" markdown>
**Open-source architecture**
ImportSpy makes architectural assumptions explicit in modular Python systems.
</div>

<div class="portfolio-proof" markdown>
**Geospatial pipeline**
B3DO turns public terrain datasets into 3D models of Basilicata.
</div>

</div>

---

## Current Focus

Right now I am focused on:

- backend platforms that can evolve without constant rewrites
- AWS serverless deployments with clear infrastructure boundaries
- modular systems, plugins, and runtime validation
- local development environments that mirror production behavior
- geospatial and data-to-model processing pipelines
- IoT, edge/cloud integration, and Digital Twin architectures
- operational reliability: logs, deployment scripts, permissions, and production visibility

---

## Signature Work

<div class="portfolio-card-grid" markdown>

<div class="portfolio-card" markdown>

### Cloud-Portable Fleet Management Platform

A production-adopted fleet management platform for vehicles, users, reservations, trips, refueling, maintenance, documents, and reports.

What matters about it:

- FastAPI backend and React/TypeScript frontend
- same application structure for local development and AWS production
- repository and storage interfaces instead of cloud-specific business logic
- Docker Compose with DynamoDB Local and MinIO
- AWS deployment with Lambda, ECR, DynamoDB, S3, CloudFront, CloudFormation, and CloudWatch

→ [Explore cloud-portable case study](case-studies/cloud-portable-fleet-platform/index.md)

</div>

<div class="portfolio-card" markdown>

### ImportSpy — Runtime Contract Engine

An open-source Python project for checking module contracts at runtime.

It helps modular systems fail early when a plugin, module, or integration does not respect the expected structure or execution context.

Useful for plugin ecosystems, modular backends, embedded runtimes, and CI/CD validation.

→ [Explore ImportSpy case study](case-studies/importspy/index.md)

</div>

<div class="portfolio-card" markdown>

### B3DO — Basilicata 3D Open

A geospatial pipeline that converts public Basilicata terrain datasets into textured 3D terrain models.

The project covers:

- DTM tile merge, regional boundary extraction, and raster clipping
- multi-resolution LOD generation for 3D terrain meshes
- hillshade, hypsometric color relief, texture generation, and river overlay
- CLI-driven workflow using GDAL, Rasterio, NumPy, PyVista, Fiona, and Typer
- unpublished pipeline, designed as an open geospatial/model-generation project

→ [Explore B3DO case study](case-studies/b3do/index.md)

</div>

<div class="portfolio-card" markdown>

### IoT Data Aggregation Architecture

An edge-to-cloud reference architecture for collecting heterogeneous IoT data and making it usable in Digital Twin systems.

It covers:

- edge acquisition from cameras, sensors, and devices
- BLE/Zigbee mesh and gateway communication
- ingestion layer for real-time, GeoJSON, and domain-specific data
- GraphQL API, data-specific layers, microfrontends, storage gateway, and AI-assisted processing

→ [Explore Digital Twin architecture case study](case-studies/iot-data-aggregation-digital-twin/index.md)

</div>

</div>

---

## Methodology Snapshot

I usually work from a few simple principles:

- make assumptions visible
- keep domain logic separate from infrastructure choices
- validate important boundaries early
- make failures understandable
- design local, staging, and production environments as part of the same system
- prefer maintainability and operational clarity over clever shortcuts

---

## Typical Application Domains

This portfolio is most relevant to:

- cloud-portable backend platforms
- AWS and serverless application architectures
- plugin-based and modular systems
- geospatial processing pipelines
- industrial and embedded systems
- integration orchestrators
- Digital Twin and edge/cloud data platforms
- real-time telemetry systems
- long-lived software systems

---

## Work Conversations

The best fit is usually a project where backend architecture, deployment, integrations, or maintainability are starting to matter as much as feature delivery.

I am especially interested in conversations around:

- backend and platform architecture
- AWS and cloud-portable deployments
- modular systems and runtime validation
- IoT, telemetry, and integration backends
- geospatial and data-processing pipelines
- technical direction for long-lived software products

→ [Contact me](contact.md) · [LinkedIn](https://www.linkedin.com/in/luca-atella/)

---

## Explore Further

- [Technical Profile](profile.md)
- [Case Studies](case-studies/index.md)
- [Curriculum Vitae](cv.md)
- [Methodology](methodology.md)
- [Contact](contact.md)
- [LinkedIn](https://www.linkedin.com/in/luca-atella/)

---

*This site collects selected projects, architectural notes, and case studies from my backend and platform engineering work.*
