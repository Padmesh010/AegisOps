# ADR-002: Transitioning Backend Core from Go to Python (FastAPI)

## Status
Approved

## Context
In early planning iterations (Chat 1/SRS draft), Go (Golang) was proposed for the backend core due to its low memory footprint and native integration with the Kubernetes Go SDK.
However, AegisOps is designed as an **AI-first platform** featuring log/metric parsing, context orchestration, and provider routing. The AI and Machine Learning ecosystem is overwhelmingly dominated by Python, which provides native, first-class SDKs and optimized libraries for client orchestration, token counting, semantic chunking, and local model inference (e.g., langchain, llama.cpp bindings, openai, anthropic). 

Writing deep integration code in Go would require maintaining complex HTTP clients manually or running subprocesses, significantly increasing architectural complexity.

## Decision
We will transition the backend core architecture to **Python (FastAPI)** while maintaining clean architecture layers and DDD patterns.

### Key Details:
- **Framework**: **FastAPI** is selected for its high runtime speed (running on ASGI/Uvicorn), automatic OpenAPI docs generation, built-in validation (Pydantic), and robust native Dependency Injection system.
- **Asynchronous Execution**: Fully utilizes `async/await` constructs to manage I/O bound operations (fetching external cloud metrics, streaming WebSocket container logs, and waiting for AI completions).
- **Core Decoupling**: Target Kubernetes interactions are resolved using the official Python Kubernetes SDK (`kubernetes` package). High-resolution collector agents can still be compiled in Go/Rust and deployed at the edge.

## Consequences
### Positive:
- **AI/LLM Velocity**: Direct import of standardized ML/LLM library bindings in the same execution memory space.
- **Developer Onboarding**: Python's readability speeds up service development cycles.
- **Contract Safety**: Standard Pydantic schemas enforce type validation at database entry paths and HTTP response structures.

### Negative:
- **Resource Footprint**: Higher baseline memory utilization than compiled Go binaries. This will be mitigated by using multi-stage alpine/slim Docker base layers and optimizing dependency sizes.
- **Concurrency Model**: Python is bound by the Global Interpreter Lock (GIL) for CPU-bound tasks. This is offset by FastAPI's asynchronous event loops, offloading heavy CPU operations to background task pools or external execution nodes.
