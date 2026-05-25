# Case Studies

This section collects selected technical case studies focused on backend platforms, cloud-portable systems, modular architectures, runtime governance, geospatial pipelines, and edge/cloud data architectures.

Each case study highlights architectural decisions, design trade-offs, and real-world constraints rather than just implementation details.

---

<div class="portfolio-card-grid" markdown>

<div class="portfolio-card" markdown>

## Cloud-Portable Fleet Management Platform  
**Full-Stack Fleet Management System with AWS Production Deployment**

A production-adopted fleet management platform designed with a cloud-portable architecture: FastAPI backend, React frontend, abstracted persistence and storage layers, local Docker Compose environment, and AWS deployment using Lambda, ECR, DynamoDB, S3, CloudFront, CloudFormation, and CloudWatch.

- Focus: Cloud portability, infrastructure abstraction, production deployment  
- Topics: AWS, FastAPI, React, DynamoDB, S3, Docker Compose, CloudFormation  

→ [View case study](cloud-portable-fleet-platform/overview.md)

</div>

<div class="portfolio-card" markdown>

## ImportSpy  
**Runtime Contract Enforcement for Modular Python Systems**

ImportSpy is a runtime governance layer for Python modules that introduces declarative contracts, deterministic validation, and structured diagnostics at import time.

It addresses architectural fragility in plugin-based, long-running, and integration-heavy systems by making implicit assumptions explicit and enforceable.

- Focus: Runtime contracts, modular safety, architectural invariants  
- Topics: Plugin governance, deterministic failure modes, validation models  

→ [View case study](importspy/overview.md)

</div>

<div class="portfolio-card" markdown>

## B3DO  
**Geospatial Pipeline for 3D Terrain Model Generation**

B3DO is an unpublished geospatial processing pipeline designed to transform public terrain and hydrographic datasets of Basilicata into textured 3D terrain models.

It demonstrates data pipeline architecture outside traditional web backends: DTM merging, boundary extraction, clipping, resampling, LOD mesh generation, hillshade/color relief textures, river overlays, and CLI-driven reproducible workflows.

- Focus: Geospatial data processing, 3D model generation, reproducible pipelines  
- Topics: GDAL, Rasterio, NumPy, PyVista, Fiona, Typer, terrain meshes  

→ [View case study](b3do/overview.md)

</div>

<div class="portfolio-card" markdown>

## Unified Backend Architecture  
**Plugin-Based IoT Backend Platform**

A scalable, plugin-driven backend architecture designed to manage heterogeneous IoT devices under a unified data model and API surface.

The platform focuses on repeatability, extensibility, and long-term maintainability across embedded, on-premise, and containerized deployments.

- Focus: Platform design, plugin systems, deployment architecture  
- Topics: Device modeling, REST APIs, WebSockets, deployment workflows  

→ [View case study](unified-backend/overview.md)

</div>

<div class="portfolio-card" markdown>

## IoT Data Aggregation Architecture  
**Edge-to-Cloud Architecture for Digital Twin Systems**

A conceptual architecture for heterogeneous IoT data acquisition and aggregation in Digital Twin scenarios, designed around edge pipelines, ingestion layers, GraphQL APIs, data-specific application layers, microfrontends, storage gateways, and AI-assisted processing.

- Focus: Edge/cloud architecture, data aggregation, Digital Twin systems  
- Topics: IoT, BLE/Zigbee mesh, GraphQL, microfrontends, AI agents, storage gateways  

→ [View case study](iot-data-aggregation-digital-twin/overview.md)

</div>

<div class="portfolio-card" markdown>

## Fleet Tracking Platform  
**Real-Time Telemetry and Vehicle Management System**

A backend system designed to ingest real-time telemetry from GPS and CAN bus-enabled tracking devices, providing fleet monitoring, driver analytics, and operational insights.

The architecture emphasizes reliability, scalability, and secure communication in mixed embedded and cloud environments.

- Focus: Real-time data pipelines, networking, API design  
- Topics: telemetry ingestion, socket communication, containerized deployment  

→ [View case study](fleet-tracking/overview.md)

</div>

</div>
