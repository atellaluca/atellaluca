# Declarative UI Schema (Widget DSL)
## Unified Backend for Heterogeneous Data Sources (SAFE)

## Why a Declarative UI Schema Exists

In heterogeneous device ecosystems, frontend complexity grows faster than backend complexity.

Each new device family introduces:

- new data fields
- new actions
- new UI interaction patterns
- new rendering requirements

Hardcoding UI behavior for every device type in the frontend leads to:

- duplicated UI logic
- brittle conditional rendering
- tight coupling between frontend and device specifics
- slow iteration cycles

To address this, the platform introduces a **declarative UI schema** (Widget DSL)
that allows plugins to describe how devices should be rendered and interacted with.

This shifts UI governance from the frontend into the platform layer,
without turning the backend into a UI framework.

---

## Design Goals

The Widget DSL was designed with the following goals:

- **Frontend decoupling**  
  Frontends should remain device-agnostic.

- **Declarative over imperative**  
  UI behavior should be described, not hardcoded.

- **Minimal surface area**  
  The schema should be small, predictable, and evolvable.

- **Runtime governance**  
  UI schemas must obey explicit contracts and invariants.

- **Composable rendering**  
  Complex UIs should be buildable from simple primitives.

---

## Conceptual Model

At a conceptual level, each device exposes:

- a **state model** (properties)
- a **capability model** (actions)
- a **presentation model** (widget schema)

The widget schema:

- binds UI components to device properties
- binds UI events to device actions
- defines layout structure
- encodes UI constraints declaratively

Frontends never interpret vendor-specific device logic.
They only interpret the widget schema.

---

## Core Schema Structure (Abstract)

A simplified, abstract schema structure looks like:

```json
{
  "layout": {
    "vertical": {
      "elements": [
        {
          "tag": "switch",
          "tracker": "power_state",
          "listener": {
            "on": "turn_on",
            "off": "turn_off"
          }
        },
        {
          "tag": "number",
          "tracker": "temperature",
          "listener": {
            "has_changed": "set_temperature"
          }
        }
      ]
    }
  }
}
```

This example is intentionally **toy-oriented** and non-identifying.

Key concepts:

- **tag**  
  Declares the UI component type.

- **tracker**  
  Binds the UI element to a device property.

- **listener**  
  Maps UI events to device actions.

- **layout**  
  Describes how UI components are composed.

---

## Binding Properties to UI

Each UI component can bind to a device property through a **tracker** field.

This creates a one-way or two-way data binding:

- property changes propagate to the UI
- UI interactions propagate back to the device via actions

This enables:

- real-time dashboards
- synchronized UI state
- consistent rendering across frontends

without requiring device-specific frontend logic.

---

## Binding Actions to UI Events

UI components can declare **listeners** that map UI events to device actions.

For example:

- a toggle switch may trigger `turn_on` or `turn_off`
- a slider may trigger `set_value`
- a button may trigger `execute_task`

The frontend does not need to know how an action is implemented.
It simply invokes the action identifier declared in the schema.

This creates a clean separation between:

- interaction semantics  
- device control logic  

---

## Runtime Governance and Validation

UI schemas are not free-form.

They are governed by runtime contracts that enforce:

- valid component types
- allowed layout structures
- mandatory fields
- valid property bindings
- valid action bindings

This prevents:

- malformed schemas
- broken UI rendering
- unsafe action exposure
- inconsistent device presentations

Schemas that violate contracts are rejected at runtime
before they can affect frontend behavior.

---

## Evolution and Backward Compatibility

The Widget DSL is versioned and designed for evolution.

Evolution strategies include:

- additive schema extensions
- backward-compatible defaults
- deprecation policies for components
- strict validation of breaking changes

This allows:

- frontends to upgrade independently
- plugins to evolve without breaking older UIs
- gradual introduction of new UI capabilities

without destabilizing the ecosystem.

---

## Why This Matters Architecturally

The Widget DSL provides architectural benefits beyond UI rendering.

It:

- centralizes UI governance in the platform
- enforces consistent UX across heterogeneous devices
- reduces frontend complexity
- enables rapid onboarding of new device families
- decouples UI evolution from device logic

This transforms the backend into a **presentation-aware platform**
without embedding frontend concerns into core services.

---

## Lessons Learned

Key lessons from introducing a declarative UI schema:

- Declarative models scale better than imperative UI logic.
- Frontend decoupling is critical in heterogeneous ecosystems.
- Runtime validation prevents long-term UI fragmentation.
- Unified schemas improve cross-device UX consistency.
- Small DSLs are more evolvable than feature-heavy ones.

---

## SAFE Disclosure

This case study intentionally omits:

- product identifiers and company references
- real schema formats and proprietary UI components
- implementation-specific rendering logic

The focus is exclusively on:

- declarative UI governance
- backend-driven presentation models
- transferable platform design principles
