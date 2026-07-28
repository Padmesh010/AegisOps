# AegisOps: Enterprise UI/UX Design System & Brand Identity
## Phase 3 — Visual Design & UX Blueprint
### Design System Version: v1.0.0-Core

---

## 1. Brand Identity Guide & Design Philosophy

The brand identity of AegisOps represents the marriage of human operational excellence and machine intelligence. The system is designed to convey security, trust, stability, and absolute control.

### 1.1. Logo Concept
The AegisOps logo consists of an abstract geometrical emblem combining the letter **A** (Aegis), a **Shield** (Security), and an **Infinite Loop** (Continuous Operations).
```text
           /\
          /  \
         / /\ \
        / /__\ \      <-- Outer shield silhouette
       / /    \ \
      / /  /\  \ \    <-- Inner node connection point
     / /  /  \  \ \
    ( (_  \__/  _) )  <-- Soft bottom curve representing infinity
     \__\______/__/
```
*   **Monochrome Variant**: Enforced on high-contrast print or terminal layouts.
*   **Glow Variant**: Active on dark digital surfaces using a soft radial drop-shadow matching the active theme's accent color.

### 1.2. Brand Personality & Voice
*   **Intelligent & Analytical**: AegisOps does not shout or spam alerts; it correlates, explains, and advises using clear metrics.
*   **Calm & Reassuring**: Operational incidents are stressful. The typography, spacing, and tone remain objective and structural.
*   **Futuristic yet Minimal**: Avoids cluttered "hacker" visual noise. Instead, it utilizes high-end, clean dashboard surfaces that prioritize situational awareness.

### 1.3. Icon & Illustration Style
*   **Icons**: Micro-line weights (1.5px stroke), geometric, non-filled icons from custom packages or Lucide-React. Action icons (e.g., Run, Restart, Clean) use theme functional colors.
*   **Illustrations**: Strict schematic wireframe layouts. No cartoon illustrations. Diagrams resemble technical blueprint line work.

---

## 2. Design System Foundations

The core design token mappings are organized into a strict hierarchy to establish unified layout grids and spatial relationships.

### 2.1. Spatial Scale (4px Base Grid)

| Token Name | Rem Value | Pixel Value | Typical Application |
| :--- | :--- | :--- | :--- |
| `--space-xs` | `0.25rem` | `4px` | Inner cell padding, button-icon spacing. |
| `--space-sm` | `0.5rem` | `8px` | Badge padding, list item gaps. |
| `--space-md` | `1.0rem` | `16px` | Standard card content padding, table column padding. |
| `--space-lg` | `1.5rem` | `24px` | Section spacing, container grid gutter sizes. |
| `--space-xl` | `2.0rem` | `32px` | Dashboard header layouts, splash screen margins. |

### 2.2. Typography (Inter & Outfit Monospace)
*   **Primary System Font**: **Inter** (sans-serif) for labels, headings, body text, and forms.
*   **Monospace Font**: **Outfit Mono** (or Fira Code) for code displays, metric tickers, Kubernetes resource YAMLs, and terminal outputs.

```text
Font Hierarchy Scale:
  Display 1: 2.25rem (36px) / 120% line-height / SemiBold (Outfit)
  Heading 1: 1.50rem (24px) / 130% line-height / Medium (Inter)
  Body Text: 0.875rem (14px) / 150% line-height / Regular (Inter)
  Mono Text: 0.75rem (12px) / 140% line-height / Regular (Outfit Mono)
```

### 2.3. Borders, Elevation & Shadows
*   **Border Radius**:
    *   Interactive controls (Buttons, inputs): `--radius-sm = 4px`.
    *   Containers (Cards, dialog panels): `--radius-md = 8px`.
    *   Command Palette & Alerts: `--radius-lg = 12px`.
*   **Elevation Layer Mapping**:
    ```text
    [Level 3] Overlay Panels (Drawers, Tooltips, Dialogs)    --> Z-Index: 1000
    [Level 2] Floating Components (Dropdowns, Toasts)        --> Z-Index: 500
    [Level 1] Core Content Cards                             --> Z-Index: 100
    [Level 0] Page Background Base Canvas                    --> Z-Index: 0
    ```

---

## 3. Theme Specifications (The Premium Seven)

AegisOps supports seven pre-configured visual theme profiles, enabling users to customize the system's aesthetic parameters immediately.

| Theme Token | Azure Command | Cyberpunk Neon | Matrix Terminal | Enterprise Dark | Arctic Ice | Sunset Orange | Midnight Purple |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Canvas BG** | `#0b111e` | `#0a0612` | `#000000` | `#121214` | `#f8f9fa` | `#110d0c` | `#0a0714` |
| **Surface** | `#141f32` | `#160a25` | `#080808` | `#1e1e24` | `#ffffff` | `#1e1512` | `#140f29` |
| **Card BG** | `#1c2b44` | `#231238` | `#101010` | `#25252d` | `#f1f3f5` | `#2d1f1b` | `#1c1538` |
| **Primary** | `#0078d4` | `#ff007f` | `#00ff33` | `#6366f1` | `#228be6` | `#f76707` | `#7048e8` |
| **Secondary** | `#2d89ef` | `#00ffff` | `#00aa22` | `#818cf8` | `#1c7ed6` | `#fd7e14` | `#845ef7` |
| **Accent** | `#00bcf2` | `#ffcc00` | `#ffffff` | `#a5b4fc` | `#15aabf` | `#ffd43b` | `#b197fc` |
| **Success** | `#107c41` | `#33ff33` | `#00ff44` | `#10b981` | `#2b8a3e` | `#37b24d` | `#2f9e44` |
| **Warning** | `#ff8c00` | `#ffff33` | `#ffff00` | `#f59e0b` | `#e67700` | `#f03e3e` | `#f08c00` |
| **Error** | `#e81123` | `#ff3333` | `#ff0000` | `#ef4444` | `#c92a2a` | `#d9480f` | `#e03131` |
| **Text Main** | `#f5f6f8` | `#00ffff` | `#00ff55` | `#f3f4f6` | `#212529` | `#f8f9fa` | `#f3f0ff` |
| **Text Muted**| `#8a9bb4` | `#9c27b0` | `#008822` | `#9ca3af` | `#868e96` | `#a68d87` | `#b197fc` |
| **Border** | `#2a3f60` | `#4a154b` | `#004411` | `#374151` | `#dee2e6` | `#4d3229` | `#3b2d6a` |
| **Chart 1** | `#0078d4` | `#ff007f` | `#00ff00` | `#6366f1` | `#228be6` | `#f76707` | `#7048e8` |
| **Chart 2** | `#00bcf2` | `#00ffff` | `#008800` | `#10b981` | `#12b886` | `#fd7e14` | `#ae3ec9` |

---

## 4. Component Layout Specifications

Components follow strict interface layouts to establish consistency across module teams.

### 4.1. The System Terminal Component
Designed to stream container logs or interactive sessions:
```text
+-----------------------------------------------------------------------------------+
|  [●] [●] [●] Terminal - auth-service-pod-99   [Filter Logs...] [Mode: Wrap]  [X]  |
+-----------------------------------------------------------------------------------+
| 2026-07-26T21:00:32.045Z [INFO] Initializing authentication controllers...        |
| 2026-07-26T21:00:32.182Z [INFO] Database pool successfully connected (PostgreSQL) |
| 2026-07-26T21:00:32.489Z [WARN] Redis pool connection timeout: Retrying...       |
| 2026-07-26T21:00:32.490Z [WARN] Connection retry #1 successful.                   |
| 2026-07-26T21:00:33.001Z [ERROR] Failed to decrypt token header metadata          |
|                                                                                   |
| > _                                                                               |
+-----------------------------------------------------------------------------------+
| [Suggested Action: Analyze with AI] [Suggested Action: Restart Pod]               |
+-----------------------------------------------------------------------------------+
```

### 4.2. Command Palette (HUD Dialog)
Triggered globally via `Ctrl+K`. It allows SREs to navigate the application or execute commands instantly:
```text
+-----------------------------------------------------------------------------------+
|  🔍 Type a command or search resource (e.g. restart auth-service)...              |
+-----------------------------------------------------------------------------------+
|  Navigate                                                                         |
|    Go to Kubernetes Pods Dashboard                                   [Go to K8s]  |
|    Go to AI Provider Settings Hub                                   [Go to Auth]  |
|  Actions                                                                          |
|    Restart Deployment...                                           [Cmd+Shift+R]  |
|    Drain Node...                                                   [Cmd+Shift+D]  |
|  AI Assistant                                                                     |
|    Ask AegisAI: "How is the memory budget on production cluster 1?"               |
+-----------------------------------------------------------------------------------+
```

---

## 5. Dashboard Wireframes

### 5.1. Global Home Dashboard Layout
```text
=====================================================================================
 AEGISOPS  [Home]  [K8s]  [Alerts]  [AI Assistant]            [Ctrl+K]  [Active Theme]
=====================================================================================
 SYSTEM HEALTH Status: HEALTHY DEGRADED  | Active Incidents: 1  | SLA State: 99.98%
-------------------------------------------------------------------------------------
 +-----------------------------------+   +------------------------------------------+
 | 📈 CPU & Memory Utilization       |   | ⚡ Self-Healing Logs (Live)               |
 |                                   |   |                                          |
 | CPU:    [========-----------] 42% |   | 21:00:32 - CrashLoopBackOff Detected     |
 | Memory: [==============-----] 73% |   | 21:00:35 - Executing PodRestart runbook  |
 |                                   |   | 21:00:48 - Post-Heal Checks PASSED [Ok]  |
 +-----------------------------------+   +------------------------------------------+
 +----------------------------------------------------------------------------------+
 | 🚨 Active Incidents                                                              |
 | [ID]     [Resource]       [Symptom]         [Trigger]     [Severity]   [AI Status]   |
 | inc-281  auth-pod-99      cAdvisor OOM      High Memory   CRITICAL     Analyzed   |
 +----------------------------------------------------------------------------------+
```

### 5.2. AI Provider Hub Interface Layout
```text
=====================================================================================
 AEGISOPS  [Home]  [AI Provider Hub]  [Kubernetes]  [Settings]                      
=====================================================================================
 ACTIVE PROVIDER: Anthropic Claude 3.5 Sonnet  | Routing Mode: Auto-Failover
-------------------------------------------------------------------------------------
 +----------------------------------------------------------------------------------+
 | AI PROVIDER REGISTRY                                                             |
 | [Provider]        [Type]       [Status]    [Latency]   [Installed Models]        |
 | Ollama            Offline      ● ACTIVE    14ms        llama3.1:8b, mistral      |
 | Anthropic Claude  Paid/API     ● ACTIVE    245ms       claude-3-5-sonnet-v2      |
 | OpenAI GPT-4o     Paid/API     ○ FALLBACK  --          gpt-4o, gpt-4-turbo       |
 | Google AI Studio  Free/API     ● ACTIVE    180ms       gemini-1.5-pro            |
 +----------------------------------------------------------------------------------+
 +-----------------------------------+   +------------------------------------------+
 | 💻 GPU & Host Memory Usage        |   | 📊 Benchmark & Token Cost Info           |
 |                                   |   |                                          |
 | GPU 0 (RTX 4090): 14GB/24GB (58%) |   | Average token cost (24h): $0.0042        |
 | VRAM Allocation:                  |   | Benchmark Score: Ollama (Excellent)      |
 | [============-------------]       |   | Google AI Studio: Standard Rate limits   |
 +-----------------------------------+   +------------------------------------------+
```

### 5.3. AI Incident Assistant / Chat Experience Layout
```text
=====================================================================================
 AEGISOPS  [Home]  [Incident Center]  [AI Assistant]                                 
=====================================================================================
 CONTEXT: incident-281 (auth-service-pod-99 CrashLoopBackOff)
-------------------------------------------------------------------------------------
 +------------------------------------+ +---------------------------------------------+
 | 💬 AegisAI Assistant Chat           | | ℹ️ Incident Context Dashboard               |
 |                                    | |                                           |
 | [AI]: I detected an out-of-memory  | | Target: auth-service-pod-99                |
 | (OOM) event on auth-service. Logs  | | Log Trace snippet:                        |
 | show the container JVM memory cap  | | "FATAL: java.lang.OutOfMemoryError"        |
 | exceeded.                          | |                                           |
 |                                    | | Recommended Runbook:                      |
 | Would you like to increase limits  | | [Increase Pod Limit & Restart]            |
 | or initiate a rollback?            | |                                           |
 |                                    | | Confidence Score: [ 92% ]                 |
 | [User]: What triggered the leak?   | |                                           |
 | [AI]: Analysis points to memory    | | Associated Metrics:                       |
 | drift in auth-service container.   | | Memory Usage (30m):                       |
 |                                    | |   / \                                     |
 | [ Message AegisAI...             ] | |  /   \____________                        |
 +------------------------------------+ +---------------------------------------------+
```

---

## 6. Data Visualization Standards

Data charts must adhere to strict visualization styling to ensure maximum screen efficiency.

### 6.1. Line Charts & Area Telemetry
*   **Axes**: Light grid lines conforming to `--border` token values.
*   **Active Metric Lines**: 2px width with a smooth curve interpolation (monotone spline). 
*   **Shading**: Radial gradient matching the metric stroke color with an opacity scale starting at 15% dropping to 0% at the baseline.

### 6.2. Cluster maps & Topology Graphs
*   **Nodes**: Hexagonal or circular icons representing Kubernetes resources (Namespace, Deployment, Pod, Service).
*   **Color Mapping**:
    *   Unhealthy Node: Pulsing outer shadow matching `--status-error` variable.
    *   Healthy Node: Static border matching `--status-success` variable.
    *   Cordoned Node: Muted outline matching `--text-muted` variable.

---

## 7. Motion & Transition System

Animations must enhance usability without adding visual latency. All transitions utilize hardware-accelerated layouts (CSS transforms and opacity).

### 7.1. Transition Scale

| Interaction | Animation Style | Duration | CSS Cubic-Bezier |
| :--- | :--- | :--- | :--- |
| **Page Navigation** | Fade and horizontal slide | `200ms` | `cubic-bezier(0.4, 0, 0.2, 1)` |
| **Command HUD Dialog** | Scale Up (95% -> 100%) & opacity | `150ms` | `cubic-bezier(0, 0, 0.2, 1)` |
| **Alert Pulser** | Radial outer scale (100% -> 115%) | `2000ms (Loop)` | `linear` |
| **Skeleton Loaders** | Linear background shine slide | `1500ms (Loop)` | `linear` |
| **Card Hover** | Border-color transition & 2px lift | `150ms` | `cubic-bezier(0.4, 0, 0.2, 1)` |

---

## 8. Accessibility (WCAG AA Compliance)

AegisOps is designed to be accessible to all operational engineers.

### 8.1. Color Contrast & Color Blindness
*   **Contrast Targets**: Body copy text maintains a minimum contrast ratio of 4.5:1 against surfaces (conforming to WCAG AA rules).
*   **Color Blindness Support**: Status indicators must not rely on color alone. Alerts utilize text labels (e.g., `[ERR]`, `[WARN]`, `[OK]`) and custom system icon shapes.

### 8.2. Screen Readers & Keyboard Control
*   **Aria Labels**: Interactive elements require explicit `aria-label` definitions detailing actions (e.g., `<button aria-label="Restart Pod auth-service-pod-99">`).
*   **Tab Routing**: All page structures are accessible using standard keyboard controls (`Tab` to navigate, `Enter` or `Space` to execute).

---

## 9. Responsive & Display Size Strategy

The user interface layouts adjust dynamically across high-end operational displays:

*   **Laptop Layout (13" - 15", 1440x900)**: Collapses secondary sidebars (e.g., the AI Assistant drawer) into tabbed side panels to maintain main screen real estate.
*   **Desktop & Ultra-wide Layouts (1080p, 2K, 4K)**: Displays persistent sidebars, multi-column metric widgets, and live log consoles concurrently.
*   **Grid Framework**: 12-column layout with fluid margins (24px padding on desktop, 16px padding on laptop viewports).
