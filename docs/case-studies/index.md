---
title: "Case Studies | Backend Architecture, AWS, IoT and Runtime Validation"
description: "Selected Luca Atella case studies on cloud-portable backend architecture, AWS serverless deployment, FastAPI, runtime contract validation, IoT systems and geospatial pipelines."
image: "assets/images/case-studies/cloud-portable-fleet-platform/cloud-portable-fleet-management-platform-aws-fastapi-architecture.png"
image_alt: "Backend architecture and AWS case studies by Luca Atella"
schema_type: "CollectionPage"
---

# Case Studies

This section collects selected projects and architecture case studies.

Each one explains the problem, the system shape, the main technical decisions, and why those decisions mattered in practice.

---

<div class="portfolio-card-grid" markdown>

<div class="portfolio-card" markdown>

## Cloud-Portable Fleet Management Platform  
**Full-Stack Fleet Management System with AWS Production Deployment**

A fleet management platform for vehicles, reservations, trips, refueling, maintenance, documents, and reporting. It was adopted in a real business context and designed so the same application model could run locally with Docker or in production on AWS.

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
**Plugin-Based IoT Backend Platform**

A plugin-driven backend architecture for managing heterogeneous IoT devices behind a unified data model and API surface.

The platform focuses on repeatability, extensibility, and maintainability across embedded, on-premise, and containerized deployments.

- Focus: Platform design, plugin systems, deployment architecture  
- Topics: Device modeling, REST APIs, WebSockets, deployment workflows  

→ [View case study](unified-backend/index.md)

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

A backend system for ingesting real-time telemetry from GPS and CAN bus-enabled tracking devices, with fleet monitoring, driver analytics, and operational workflows.

The architecture emphasizes reliability, scalability, and secure communication in mixed embedded and cloud environments.

- Focus: Real-time data pipelines, networking, API design  
- Topics: telemetry ingestion, socket communication, containerized deployment  

→ [View case study](fleet-tracking/index.md)

</div>

</div>
