# ADR-004: Designing the AI Provider Hub Abstraction

## Status
Approved

## Context
AegisOps must interface with multiple AI vendors (OpenAI, Anthropic, Google Vertex AI, Amazon Bedrock, Ollama, local vLLM nodes). 
While frameworks like LangChain exist to abstract LLMs, they introduce heavy dependency footprints, frequent breaking API shifts, high performance overhead, and make writing raw asynchronous custom stream processors difficult.
To ensure the AegisOps core remains lightweight, robust, and maintainable, we need a simple, low-dependency abstraction layer.

## Decision
We will implement a custom interface-based **AI Provider Hub** directly in our core domain.

### Key Details:
- **Core Interface**: An `AIProvider` abstract base class defining `generate_completion` and `generate_stream` methods.
- **Provider Registry**: A factory pattern resolving string model targets (e.g., `openai/gpt-4o`, `ollama/llama3`) to specific vendor client implementations.
- **No Heavy Wrappers**: Backend implementations connect directly to official vendor clients (e.g., `openai` or `httpx` for Ollama/vLLM HTTP calls).
- **Graceful Degraded States**: Features fallback pipelines (if OpenAI fails with a 429 error code, the request automatically reroutes to Anthropic or a local Ollama instance).

## Consequences
### Positive:
- **Low Footprint**: Eliminates thousands of bloated dependencies from our environment.
- **API Stability**: Direct control over client HTTP headers, timeouts, and streaming structures.
- **Flexible Retries**: Custom logic for retry strategies, fallback routes, and token count logging.

### Negative:
- **Maintenance Cost**: The team must write custom mappings for new model features (e.g., tool-calling parameters) if the underlying vendor API schemas change. This is mitigated by focusing only on core operations: completions, streaming, and tool calls.
