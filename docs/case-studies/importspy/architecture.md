---
title: "ImportSpy Architecture | Evidence, Policy and Python Admission"
description: "How Luca Atella’s ImportSpy separates source inspection, dependency identity, evidence collection, policy evaluation and explicit Python execution."
image: "assets/luca-atella-software-architect-backend-platform-engineer.png"
image_alt: "Luca Atella, author of ImportSpy’s Python admission architecture"
schema_type: "TechArticle"
---

# ImportSpy — Architecture

ImportSpy’s central design choice is to separate **learning about a module**, **deciding whether its facts satisfy policy**, and **executing it**. Each step has a different trust boundary. Keeping them explicit makes the admission result useful to a developer, a CI job or a plugin host without making execution an incidental part of validation.

The [case study](index.md) presents the project context; this page examines the architectural tradeoffs of **ImportSpy 0.5.0**.

## Source snapshots and the execution boundary

The inspector reads source bytes, hashes them, parses the AST and compiles it to validate syntax without running the resulting code. Its facts describe declarations and import references, not every object Python might eventually create. Decorators, metaclasses and computed values can leave required properties unknown; inspection does not execute them to resolve uncertainty.

`check` returns a decision even when admission succeeds. Execution requires an explicit `load`, which refreshes dependency metadata and performs a new admission check. Once admitted, it executes the captured source bytes rather than reopening the path. A test changes the source file during evidence collection and verifies that the inspected snapshot is what runs.

This limits the gap between checking and using the **selected source**. It does not freeze installed dependencies, import hooks, external files or the surrounding process. Runtime validators run after module initialization; removing a failed module from `sys.modules` cannot undo its effects. The loader is neither an import hook nor a sandbox.

The retained `Spy.importspy` and `SpyModel.from_module` compatibility APIs inspect modules that have already executed. They belong to the earlier runtime-contract design and do not acquire the admission pipeline's pre-execution boundary. See the [library workflow and migration guidance](https://github.com/atellaluca/ImportSpy/blob/main/docs/modes/embedded.md).

## Dependency identity without false certainty

An import name and a distribution name answer different questions. One import can map to several installed distributions, while one distribution can supply several imports. ImportSpy retains these mappings rather than choosing one contributor arbitrarily. Namespace imports therefore receive conservative treatment: policy evaluates all mapped contributors.

The resolver distinguishes standard-library, internal, external, namespace, direct-origin and unresolved dependencies. It reads source paths and installed metadata without importing candidate dependencies. Missing mappings stay unresolved, and required facts that cannot be established fail closed.

This conservatism can check namespace contributors unused by a particular child import. The inventory covers imports observed in the selected file, including conditional and function-body imports. It does not recursively establish the transitive dependency graph or intercept dynamic imports.

## Evidence is separate from policy

Normalized `Evidence` records carry a subject, observation, provider, phase and status. Four states preserve distinctions that a boolean would lose:

| Status | Meaning |
| --- | --- |
| `verified` | The producer established the particular stated fact. |
| `observed` | Data is available without a stronger verification claim. |
| `unknown` | The method cannot establish the fact. |
| `unavailable` | Collection failed or was disabled. |

Installed origin metadata is an observation, not cryptographic provenance. Likewise, verified syntax says nothing about whether arbitrary Python behavior is safe. Policy decides which facts and status are sufficient; required unknown or unavailable evidence cannot silently become approval.

Separating collection from evaluation keeps policy deterministic **for the same policy and facts**. Core checks work offline without an account or telemetry. Separate checks can still differ because source, installed metadata, host state and timestamps change. Dependency caches belong to an engine instance; explicit loading refreshes them.

## Extension points expose when code runs

| Extension | Responsibility and execution phase |
| --- | --- |
| `EvidenceProvider` | Collect selected local or external facts during admission. |
| `PolicyValidator` | Evaluate collected facts without I/O during policy evaluation. |
| `RuntimeValidator` | Inspect runtime objects after explicit target execution. |
| `Reporter` | Format an existing decision without rerunning admission. |

These are trusted Python extensions. Providers are selected explicitly; the engine does not load every installed plugin. Network-dependent collection requires opt-in, but that declaration is a cooperation boundary, not a firewall around plugin initialization or code.

The protocols are implemented; the [offline extension example](https://github.com/atellaluca/ImportSpy/blob/main/docs/extensions.md) demonstrates them without external verification. OSV/pip-audit, Sigstore, PyPI attestations, CycloneDX, SPDX and GitHub metadata adapters remain [proposed integrations](https://github.com/atellaluca/ImportSpy/blob/main/docs/community-roadmap.md) rather than native capabilities.

## One decision, several consumers

`AdmissionDecision` keeps source and policy identity and hashes, engine version, host facts, dependencies, evidence, violations and the admission result together. Its phases and `target_executed` flag distinguish host inspection from target execution. A `Violation` carries a stable code, severity, explanation and a source location when known.

Human, JSON and SARIF reporters consume that same decision. JSON preserves the inventory and evidence; SARIF presents violations for code-scanning workflows. Formatting does not repeat collection or execute the target. This gives automation structured diagnostics while preserving the evidence needed to explain a denial.

Version **0.5.0** implementation and limits: [official architecture](https://github.com/atellaluca/ImportSpy/blob/main/docs/architecture.md), [security model](https://github.com/atellaluca/ImportSpy/blob/main/docs/security-model.md) and [source code](https://github.com/atellaluca/ImportSpy).
