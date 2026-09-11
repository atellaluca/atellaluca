---
title: "Technical Case Studies - Luca Atella"
description: "Technical case studies on cloud-portable backend architecture, runtime governance, AWS, IoT, Digital Twin systems and geospatial pipelines."
image: "assets/images/case-studies/cloud-portable-fleet-platform/cloud-portable-fleet-management-platform-aws-fastapi-architecture.png"
image_alt: "Backend architecture and AWS case studies by Luca Atella"
schema_type: "CollectionPage"
---

# Case Studies

This section collects selected projects and architecture case studies.

Each one explains the problem, the system shape, the main technical decisions, and why those decisions mattered in practice.

Use this hub as the evidence layer of the portfolio: each page connects a technical problem to architecture boundaries, runtime decisions, and implementation trade-offs.

---

<div class="portfolio-card-grid" markdown>

<div class="portfolio-card" markdown>

## Cloud-Portable Fleet Management Platform  
**Full-Stack Fleet Management System with AWS Production Deployment**

A Fleet Management System used by Studio Lambda to manage vehicle turnover for 50 employees. It is deployed on AWS and designed to separate application logic from persistence, cloud services, and the web runtime.

- Focus: Cloud portability, infrastructure abstraction, production deployment  
- Topics: AWS, FastAPI, React, DynamoDB, S3, Docker Compose, CloudFormation  

→ [View case study](cloud-portable-fleet-platform/index.md)

</div>

<div class="portfolio-card" markdown>

## ImportSpy  
**Runtime Contract Enforcement for Modular Python Systems**

ImportSpy is an open-source Python project that checks runtime contracts for modules.

It helps plugin-based and modular systems detect incompatible modules early, with structured diagnostics instead of hidden assumptions.

- Focus: Runtime contracts, modular safety, architectural invariants  
- Topics: Plugin governance, deterministic failure modes, validation models  

→ [View case study](importspy/index.md)

</div>

<div class="portfolio-card" markdown>

## B3DO  
**Geospatial Pipeline for 3D Terrain Model Generation**

B3DO is a geospatial processing pipeline for transforming public terrain and hydrographic datasets of Basilicata into textured 3D terrain models.

It demonstrates data pipeline architecture outside traditional web backends: DTM merging, boundary extraction, clipping, resampling, LOD mesh generation, hillshade/color relief textures, river overlays, and CLI-driven workflows.

- Focus: Geospatial data processing, 3D model generation, reproducible pipelines  
- Topics: GDAL, Rasterio, NumPy, PyVista, Fiona, Typer, terrain meshes  

→ [View case study](b3do/index.md)

</div>

<div class="portfolio-card" markdown>

## Unified Backend Architecture  
**Plugin-Based Backend Framework Behind delis.app**

The backend framework I developed at Vemar and on which delis.app is based, presented in SAFE form to show integration separation, contracts, and a unified API surface.

- Focus: Framework development, plugin systems, deployment architecture
- Topics: Device modeling, REST APIs, WebSockets, deployment workflows  

→ [View case study](unified-backend/index.md)

</div>

<div class="portfolio-card" markdown>

## Runtime Isolation for Italian Tax Applications
**Compatibility Work for Agenzia delle Entrate Desktop Tools**

A professional intervention in an accounting firm to keep tax applications from different years usable in the same Windows environment by isolating Java runtimes, JNLP/LaunchAnywhere startup modes, and Desktop Telematico/Entratel requirements.

- Focus: Legacy diagnosis, dependency isolation, operational continuity
- Topics: Windows, Java runtime, JNLP, LaunchAnywhere, Entratel, truststore

→ [View case study](agenzia-entrate-runtime-isolation/index.md)

</div>

<div class="portfolio-card" markdown>

## IoT Data Aggregation Architecture  
**Edge-to-Cloud Architecture for Digital Twin Systems**

An edge-to-cloud architecture for collecting heterogeneous IoT data and making it usable in Digital Twin systems. It covers edge acquisition, ingestion layers, GraphQL APIs, data-specific application layers, microfrontends, storage gateways, and AI-assisted processing.

- Focus: Edge/cloud architecture, data aggregation, Digital Twin systems  
- Topics: IoT, BLE/Zigbee mesh, GraphQL, microfrontends, AI agents, storage gateways  

→ [View case study](iot-data-aggregation-digital-twin/index.md)

</div>

<div class="portfolio-card" markdown>

## Fleet Tracking Platform  
**Real-Time Telemetry and Vehicle Management System**

A real-time telemetry backend distinct from the Studio Lambda fleet management platform: the infrastructure I personally designed and implemented at Vemar for 80 trackers, including socket communication, CAN bus data, persistence, and REST APIs.

- Focus: Real-time data pipelines, networking, API design  
- Topics: telemetry ingestion, socket communication, containerized deployment  

→ [View case study](fleet-tracking/index.md)

</div>

</div>
