# Violation System and Contract Diagnostics  
## ImportSpy — Violation System Deep Dive

---

## Why a Dedicated Violation System?

In most runtime validation frameworks, failures are reported through:

- generic exceptions  
- unstructured error messages  
- stack traces disconnected from domain semantics  

This approach conflates two fundamentally different concerns:

- detecting a contract violation  
- explaining why the contract was violated  

As a result:

- errors are hard to interpret  
- diagnostics are inconsistent  
- debugging becomes expensive  
- failure semantics are ambiguous  

ImportSpy introduces a dedicated Violation System  
to treat contract violations as first-class architectural events,  
rather than as incidental runtime errors.

---

## Contract Violations as First-Class Objects

In ImportSpy, a contract violation is not represented as a raw exception.

It is modeled as a first-class object implementing a formal  
ContractViolation abstraction.

This means that a violation:

- has a semantic type  
- carries structured contextual data  
- belongs to a specific validation domain  
- produces a deterministic diagnostic message  

This design separates:

- violation detection  
- from violation representation  
- from violation reporting  

and turns failures into structured domain artifacts.

---

## Violation Taxonomy

Contract violations are organized into a small, explicit taxonomy  
reflecting the semantics of failure.

The three primary violation categories are:

- MISSING  
  A required element is not present in the runtime model.

- MISMATCH  
  An element is present but does not satisfy the expected value  
  or structural constraint.

- INVALID  
  An element exists but has a value that is not allowed  
  under the contract.

This taxonomy provides:

- semantic clarity  
- consistent error classification  
- predictable failure modes  

across all validation domains.

---

## Domain-Specific Violation Types

Violations are further specialized by validation domain.

Each domain defines its own violation type, including:

- ModuleContractViolation  
- FunctionContractViolation  
- VariableContractViolation  
- RuntimeContractViolation  
- PythonContractViolation  
- SystemContractViolation  

Each specialized violation class is responsible for:

- interpreting domain-specific context  
- selecting appropriate message templates  
- producing semantically precise diagnostics  

This avoids a single monolithic error type  
and preserves semantic locality.

---

## Message Templates and Payload Injection

Violation messages in ImportSpy are not hard-coded.

Instead, they are generated from message templates  
associated with each violation category and domain.

At runtime, a mutable payload object is built,  
containing contextual metadata such as:

- expected values  
- actual values  
- module names  
- variable names  
- runtime properties  

This payload is then injected into the message template  
to produce a fully contextualized diagnostic.

This design enables:

- consistent phrasing across violations  
- localized message formatting  
- deterministic message output  
- future internationalization  

without coupling validation logic to presentation.

---

## Separation of Concerns

The Violation System enforces a strict separation between:

- validation rules  
- violation construction  
- message rendering  
- error propagation  

Validation rules never:

- format messages  
- raise raw exceptions  
- embed presentation logic  

They only:

- detect constraint failures  
- construct domain violations  
- attach contextual payloads  

This makes the validation engine:

- simpler  
- more testable  
- easier to extend  
- independent from UX concerns.

---

## Deterministic Failure Semantics

When a contract is violated:

- provider–consumer interaction is aborted  
- one or more ContractViolation objects are produced  
- a structured validation error is raised  

This guarantees that:

- invalid modules never enter the system  
- failures are deterministic  
- system state remains consistent  
- diagnostics are reproducible  

and eliminates entire classes of late runtime failures.

---

## Human-Readable and Machine-Readable Diagnostics

Violation diagnostics in ImportSpy are designed to be both:

- human-readable, for developers  
- machine-readable, for CI/CD and tooling  

A typical diagnostic includes:

- a semantic scope label (e.g., [MODULE], [VARIABLE])  
- the expected condition  
- the actual runtime condition  
- an optional remediation hint  

Example:

> [MODULE] Expected variable `timeout: int` not found in `my_module.py`  
> → Please add the variable or update your contract.

This dual nature makes violations usable in:

- local development  
- automated pipelines  
- static analysis tooling  
- observability systems  

---

## Integration with the Validation Pipeline

The Violation System is fully integrated  
into the rule-based validation pipeline.

Each rule:

- validates exactly one constraint  
- produces zero or more ContractViolation objects  
- never raises raw domain exceptions  

The pipeline then:

- aggregates all violations  
- determines overall contract satisfaction  
- decides whether to abort integration  

This ensures that:

- multiple independent violations  
  can be reported in a single run  
- diagnostics are complete  
- failures are not masked by early exits.

---

## Architectural Implications

Introducing a dedicated Violation System:

- formalizes the semantics of failure  
- decouples detection from reporting  
- stabilizes diagnostics across versions  
- enables tooling and automation  
- supports long-term contract evolution  

and elevates error handling  
from a technical afterthought  
to a first-class architectural concern.

---

## Lessons Learned

- Failure semantics are part of system architecture.  
- Structured diagnostics dramatically improve usability.  
- Separation of concerns simplifies extensibility.  
- Deterministic errors enable reliable automation.  
- Contracts are only useful if violations are intelligible.
