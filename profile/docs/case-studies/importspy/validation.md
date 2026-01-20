# Designing a Runtime Validation Engine  
## ImportSpy — Validation System Deep Dive

---

## The Problem

In modular systems and plugin-based architectures, component validation is often:

- performed too late in the execution flow  
- fragmented across the codebase  
- implemented through ad-hoc procedural checks  

This typically leads to:

- failures surfacing only at advanced runtime stages  
- partially initialized states  
- unpredictable behavior  
- integration bugs that are difficult to diagnose  

In the *provider → consumer* model adopted by ImportSpy, these issues are amplified by the fact that:

- a provider module exposes functionality to external modules  
- consumer modules may have heterogeneous structures and assumptions  
- there is no formal boundary governing integration correctness  

As a result, integration correctness is often based on implicit assumptions rather than on enforceable, explicit contracts.

---

## Design Goals

The validation system of ImportSpy was designed around the following goals:

- generic applicability across domains  
- schema-driven validation  
- separation between model and execution logic  
- deterministic behavior  
- structured and diagnostic error reporting  
- long-term extensibility  

The objective was not to build a collection of checks,  
but a **generic runtime validation engine** reusable across different architectural contexts.

---

## Conceptual Architecture of the Validation System

At a conceptual level, the validation system is composed of three primary layers:

1. **Schema Layer (SpyModel)**  
   A declarative language for expressing runtime contracts.

2. **Rule Engine**  
   A collection of independent rules validating individual constraints.

3. **Execution Pipeline**  
   A deterministic flow orchestrating validation.

---

## The Declarative Contract Model (SpyModel)

To express runtime contracts in a formal, extensible, and implementation-independent way,  
ImportSpy introduces a declarative meta-model called **SpyModel**.

SpyModel is not a simple configuration structure, but a true conceptual model representing:

- the different types of expressible constraints  
- the semantic categories of requirements  
- the separation between structure, context, and environment  
- the hierarchical composition of contracts  

This model makes it possible to treat a contract as a first-class object:  
serializable, introspectable, and validatable independently from application code.

---

### Conceptual Architecture of SpyModel

The following diagram represents the conceptual structure of the SpyModel meta-model,  
which defines the declarative language used by ImportSpy to express runtime contracts.

![SpyModel conceptual architecture](https://raw.githubusercontent.com/atellaluca/ImportSpy/refs/heads/main/docs/assets/importspy-spy-model-architecture.png)

---

## Extending the Module Model and Baseline Contracts

SpyModel extends the conceptual model of a Python module (Module) by introducing  
a formal and typed representation of its structural, contextual, and environmental  
properties.

This extension makes it possible to model a module not only for what it **is**,  
but also for what it **must be** in order for integration to be considered valid.

In particular, SpyModel introduces the notion of a **baseline contract**,  
representing a lower bound of constraints that are always enforced,  
independently of the application domain.

This baseline includes, for example, constraints on:

- CPU architecture  
- operating system  
- Python version  
- interpreter implementation  
- minimal environment requirements  

The baseline contract acts as a first level of enforcement, ensuring that any runtime  
satisfies minimal compatibility requirements even before applying  
provider-defined, domain-specific contracts.

---

## Contract Satisfaction Semantics

Validation in ImportSpy is not based on simple structural equality checks,  
but on a **contract satisfaction semantics**.

In this model:

- the SpyModel derived from the contract represents the set of constraints  
  declared by the provider module  
- the SpyModel derived from the current runtime represents the effective properties  
  of the execution environment and of the consumer module  

Validation consists in verifying that:

> every constraint expressed in the contract SpyModel  
> is satisfied by the SpyModel representing the current runtime.

Formally, this is equivalent to checking that:

> **contract model ⊆ runtime model**  
> i.e., that the runtime **satisfies** the contract.

This approach makes it possible to:

- treat contracts and runtime as homogeneous models  
- apply a formal notion of conformance  
- avoid fragile, ad-hoc procedural checks  

---

## Projecting the Runtime into the Meta-Model

To make this satisfaction semantics possible, ImportSpy builds  
a SpyModel instance in the background that represents the current execution context.

This runtime model includes:

- Python interpreter metadata  
- platform information  
- environment variables  
- consumer module structure  
- relevant runtime properties  

In this way, both the contract and the runtime are represented  
within the same declarative meta-model.

Validation therefore reduces to a comparison between models,  
rather than to a collection of imperative checks scattered across the codebase.

---

## Rule Engine

The validation engine is designed as a **rule-based engine**, where:

- each rule validates exactly one constraint  
- rules are independent from each other  
- rules do not mutate shared state  
- each rule produces a structured result  

This design enables:

- deterministic execution  
- simplicity of testing  
- incremental extensibility  
- conceptual parallelization of rule evaluation  

---

## Validation Pipeline

At an abstract level, validation follows a deterministic pipeline:

1. Load the contract schema defined by the provider.  
2. Build the execution context.  
3. Resolve consumer module metadata.  
4. Project the runtime into a SpyModel instance.  
5. Execute all validation rules.  
6. Aggregate validation results.  
7. Produce the final validation outcome.

Each step is isolated and testable.

---

## Fail-Fast Semantics

The system adopts a **fail-fast** semantics:

- validation happens before provider–consumer interaction can occur  
- non-compliant modules never enter the system  
- no partially initialized states are allowed  

This dramatically reduces:

- the runtime error surface  
- recovery complexity  
- undefined behavior  

---

## Applications of the Validation System

This validation architecture is applicable to:

- plugin frameworks  
- modular backends  
- microservice bootstrapping  
- CI/CD policy enforcement  
- IoT and edge platforms  

---

## Design Trade-offs

Several trade-offs were considered during design:

- **Expressiveness vs complexity**  
  A more expressive contract language is more powerful,  
  but harder to use and maintain.

- **Performance vs validation depth**  
  Deeper introspection increases import-time latency.

- **Generality vs domain specificity**  
  Generic rules are less optimized than domain-specific rules.

---

## Lessons Learned

- Validation should be declarative and formal.  
- Contracts are architectural boundaries, not mere configurations.  
- Fail-fast semantics dramatically improve reliability.  
- Separating model and execution simplifies system evolution.  
- Treating runtime as a model enables formal reasoning about integration.
