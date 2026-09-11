---
title: "CV - Luca Atella"
description: "CV of Luca Atella, software architect and backend platform engineer focused on AWS, modular systems, cloud-portable architecture, IoT and runtime governance."
image: "assets/luca-atella-portrait.jpg"
image_alt: "Portrait of Luca Atella, Software Architect and Backend Engineer"
schema_type: "ProfilePage"
---

# Luca Atella — Curriculum Vitae

**Software Architect · Backend & Platform Engineering · AWS Certified**  
Basilicata, Italy · Email: [info@atellaluca.com](mailto:info@atellaluca.com) · GitHub: [github.com/atellaluca](https://github.com/atellaluca) · LinkedIn: [linkedin.com/in/luca-atella](https://www.linkedin.com/in/luca-atella/)

[Download PDF](assets/cv/Luca-Atella-CV.pdf){ .md-button .md-button--primary }

[Portfolio Home](index.md) · [Case Studies](case-studies/index.md) · [GitHub](https://github.com/atellaluca) · [Contact](contact.md)

---

## Profile

Software Architect, Tech Lead, and Backend/Platform Engineer. I design and directly build backends, APIs, and application infrastructure, with attention to architectural boundaries, integrations, deployment, and maintainability.

At Vemar, from April 2021 to October 2024, I worked as Tech Lead with continuous technical coordination responsibility for a 4-person team. I personally designed and implemented the infrastructure for 80 trackers and developed the framework on which delis.app is based.

I also work on geospatial processing and model-generation pipelines, applying the same architectural discipline to data transformation workflows outside traditional backend systems.

---

## Certifications

- AWS Certified Solutions Architect - Associate
- AWS Certified Cloud Practitioner
- AWS Certified AI Practitioner
- Cisco Networking Academy - CCNA path

---

## Core Competencies

### Backend & Platform Engineering

- Python, FastAPI, Flask, Pydantic
- REST API design and OpenAPI
- WebSocket and real-time communication
- Modular and plugin-based architectures
- Repository and storage abstraction
- Structured error handling
- MongoDB, PostgreSQL, DynamoDB

### Cloud & Infrastructure

- AWS Lambda, ECR, DynamoDB, S3, CloudFront, CloudFormation, CloudWatch
- Docker and Docker Compose
- Cloud-portable application design
- Infrastructure as Code
- Serverless deployment pipelines
- Linux server configuration
- Nginx reverse proxy
- VPN infrastructure
- DNS, firewalling, and networking

### Architecture

- Runtime governance
- Contract-driven design
- Long-lived backend systems
- Infrastructure abstraction
- Edge/cloud integration
- IoT data aggregation
- Digital Twin architecture concepts
- Geospatial data processing
- 3D terrain model generation
- Developer tooling and CLI workflows

---

## Professional Experience

### Tech Lead / Backend & Platform Engineer — Vemar S.A.S.
**April 2021 - October 2024**

Designed and developed backend architectures for distributed IoT systems and heterogeneous device integrations, working as Tech Lead.

Main responsibilities:

- continuously coordinated a 4-person technical team
- developed the plugin-based backend framework on which delis.app is based
- personally designed and implemented the infrastructure for 80 trackers
- worked on socket communication, CAN bus data, persistence, and REST API exposure
- centralized application logic, authentication, API exposure, and persistence concerns
- defined REST API contracts and backend structure
- designed plugin loading and execution boundaries
- introduced Docker-based development and deployment workflows
- coordinated backend/frontend architectural decisions in a small full-stack team
- supported infrastructure, provisioning, and deployment operations

The platform remained operational and structurally stable after delivery, demonstrating the long-term maintainability of the architecture.

---

## Selected Projects

### Cloud-Portable Fleet Management Platform  
**Full-stack AWS production deployment · 2026**

Fleet Management System used by Studio Lambda to manage vehicle turnover for 50 employees. The system is deployed on AWS and designed with separation between application logic, persistence, cloud services, and web runtime.

The system includes a FastAPI backend, React/TypeScript frontend, abstracted persistence and storage layers, local Docker Compose environment, and AWS deployment using Lambda, ECR, DynamoDB, S3, CloudFront, CloudFormation, and CloudWatch.

Key contributions:

- designed the application architecture and backend domain model
- implemented repository and storage abstraction layers
- built backend APIs for users, vehicles, trips, reservations, refueling, maintenance, reporting, and statistics
- configured local development with Docker Compose, DynamoDB Local, and MinIO
- implemented AWS deployment automation with CloudFormation and Bash scripts
- worked on frontend integration and production observability

### Real-Time Fleet Telemetry Backend
**Vemar · 80-tracker infrastructure**

Infrastructure distinct from the Studio Lambda platform, personally designed and implemented at Vemar for 80 trackers. The work included socket communication, CAN bus data, persistence, and REST API exposure.

### Unified Backend for Heterogeneous Data Sources
**Vemar · framework behind delis.app**

Plugin-based backend framework I developed at Vemar and on which delis.app is based. The case study presents integration separation, explicit contracts, and a unified API model in SAFE form; it does not attribute every architectural generalization to the product itself.

### ImportSpy — Runtime Contract Validation Engine  
**Open-source Python project**

Created and maintain ImportSpy, a runtime contract enforcement engine for Python modules.

ImportSpy validates structural, contextual, and execution constraints at import time, making architectural assumptions explicit in modular and long-lived Python systems.

Highlights:

- YAML-based declarative contracts
- runtime validation of module structure and execution context
- deterministic failure model
- 15,000+ downloads on PyPI
- presented at GDG Basilicata

### B3DO — Basilicata 3D Open  
**Geospatial processing pipeline · unpublished / in development**

Designed a Python-based pipeline for transforming public Basilicata terrain datasets into 3D terrain models.

The project uses GDAL, Rasterio, NumPy, PyVista, Fiona, and Typer to support DTM merging, boundary extraction, raster clipping, resampling, LOD mesh generation, hillshade/color relief texture generation, river overlays, and textured 3D previews.

Key contributions:

- designed the CLI-driven processing workflow
- separated raw data, processed datasets, build artifacts, and model outputs
- implemented terrain mesh generation from elevation rasters
- introduced diagnostics for system dependencies and source datasets
- modeled the project as a reproducible data-to-model pipeline rather than a manual GIS workflow

### IoT Data Aggregation Architecture for Digital Twin Systems  
**Architecture concept**

Designed a conceptual edge-to-cloud architecture for heterogeneous IoT data acquisition and aggregation in Digital Twin scenarios.

The architecture includes edge acquisition from devices and sensors, BLE/Zigbee mesh communication, gateways, ingestion layers, GraphQL API, data-specific application layers, microfrontends, storage gateway, object/database queues, and AI-assisted processing.

### Runtime Compatibility for Agenzia delle Entrate Applications
**Professional intervention · accounting firm**

Intervention in a Windows environment with IRAP 2019-2021, ISA, Desktop Telematico / Entratel, and other applications with different Java dependencies. I isolated Java runtimes per application, handled JNLP/LaunchAnywhere startup modes, treated Entratel TLS/truststore requirements separately, and verified coexistence without assuming tax consulting or regulatory certification responsibilities.

---

## Education

**BSc in Computer Science and Technology (L-31)** — University of Basilicata  
2018 - Present

**High School Diploma in Electronics, Electrical Engineering, and Automation** — I.I.S. Einstein-De Lorenzo, Potenza  
2013 - 2018

---

## Languages

Italian: native  
English: B1, actively improving through technical study and international collaboration

---

## Tech

Python · FastAPI · React · AWS · Lambda · DynamoDB · S3 · CloudFront · CloudFormation · Docker · Docker Compose · Kubernetes · Linux · Networking · Runtime Governance · GDAL · Rasterio · PyVista
