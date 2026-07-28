# ADR-003: Selecting React, TypeScript, and Vite for the Frontend

## Status
Approved

## Context
AegisOps requires a premium, responsive dashboard user interface that streams real-time incident updates, visualizes complex cluster topologies, and handles multiple dynamic visual themes.
Traditional bundlers like Webpack create high latency during developer hot-reloading (HMR) and produce bloated build outputs.

## Decision
We select **React + TypeScript + Vite** for the frontend application stack.

### Key Details:
- **Build Tool**: **Vite** leverages native ES modules (ESM) in the browser to deliver near-instantaneous hot-module replacement (HMR) and optimized Rollup-based production builds.
- **Type Safety**: **TypeScript** is enforced throughout to eliminate runtime script errors and map API schemas to UI state models.
- **State Management**: **Zustand** is selected as the state manager instead of Redux due to its small footprint, hook-based APIs, and simplicity.
- **Layouts & Styling**: Styled using Custom CSS modules and native CSS custom properties (variables) to enable instant theme hot-swapping and smooth hardware-accelerated animations.

## Consequences
### Positive:
- **Fast Development Loops**: Sub-second component rebuilds during development.
- **Strong Typing**: Type validation from network payloads down to presentation components.
- **Performance**: Minimal framework overhead, preventing browser thread locking during heavy rendering sequences (e.g., metric canvas charts).

### Negative:
- **Client Processing**: A Single Page Application (SPA) shifts parsing overhead to user browsers. Mitigation includes lazy loading heavy features (e.g., IaC visual model editors) using code-splitting methods.
