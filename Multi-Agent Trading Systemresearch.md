# **Autonomous Alpha: Architecting Multi-Agent Financial Systems with Google Antigravity, NautilusTrader, and OANDA**

## **Executive Summary**

The convergence of agentic software development, event-driven execution architectures, and high-performance quantitative research frameworks marks a definitive epoch in algorithmic trading. As we traverse the technology landscape of 2026, the query regarding the legitimacy of "Google Antigravity" serves as a bellwether for the industry's shift from human-centric coding to agent-orchestrated engineering. This report confirms that "Antigravity" is not a typographical error but the foundational "Agent-First" development platform introduced by Google in late 2025\.1 This platform fundamentally redefines the operational capability of quantitative developers, allowing for the deployment of autonomous software agents that plan, execute, and verify complex engineering tasks.

This document serves as an exhaustive technical architectural guide for constructing a sophisticated, multi-agent algorithmic trading system. The proposed architecture integrates three critical layers: the orchestration layer powered by **Google Antigravity**, the execution layer driven by **NautilusTrader**, and the market access layer provided by **OANDA**. Furthermore, the research capability is powered by a comparative analysis of **VectorBT Pro** and its open-source alternatives.

The central thesis of this report is that the unification of these technologies allows individual quantitative architects to operate with the capacity of institutional teams. By offloading the "heavy lifting" of code generation, adapter maintenance, and backtest verification to Antigravity agents, the human architect focuses on alpha generation and risk management. However, this integration is not without significant engineering challenges. Most notably, the absence of a native, production-grade OANDA adapter within the NautilusTrader ecosystem necessitates a rigorous custom development phase. This report details the specific Standard Operating Procedures (SOPs), architectural patterns, and code-level logic required to bridge these systems effectively, ensuring that the final deployed agent is robust, low-latency, and mathematically correct.2

## ---

**1\. The Paradigm Shift: Agentic Development in Quantitative Finance**

### **1.1 The Validity and Velocity of Google Antigravity**

The initial skepticism regarding "Antigravity"—whether it represents a legitimate framework or a misnomer for established tools like AutoGen—is understandable given the rapid cadence of AI releases. However, research definitively identifies Google Antigravity as a distinct, enterprise-grade platform released to public preview in late 2025\.1 It differs fundamentally from libraries like LangChain or AutoGen. While those are frameworks for *building* agents, Antigravity is a platform *for* developers to utilize agents as core members of the engineering workflow. It replaces the traditional Integrated Development Environment (IDE) with an "Agent-First" environment, shifting the developer's role from a writer of syntax to an architect of intent.4

The implications for algorithmic trading are profound. In traditional workflows, a quant trader must context-switch between analyzing charts, writing Python scripts, managing Docker containers, and debugging API connections. Antigravity acts as a "Mission Control," allowing the developer to delegate these distinct workstreams to specialized agents.4 For instance, a "Research Agent" can be tasked with optimizing parameters using VectorBT Pro, while an "Infrastructure Agent" simultaneously configures a Google Cloud Run deployment, and a "QA Agent" writes unit tests for the OANDA adapter. These agents operate asynchronously, utilizing tools across the editor, terminal, and browser, and report back with structured "Artifacts" rather than unstructured chat logs.1

#### **1.1.1 The "Mission Control" Interface vs. The Editor**

Antigravity introduces a bifurcated interface that separates high-level command from low-level implementation. The **Manager Surface** is the primary domain of the multi-agent process. Here, the user defines the "Mission"—for example, "Build a mean-reversion strategy on EUR/USD"—and the system spawns the necessary sub-agents to execute it. This surface abstracts the complexity of state management, allowing the user to observe multiple workstreams in parallel.1 Conversely, the **Editor View** remains available for "hands-on" intervention. This is crucial in financial engineering, where a single line of erroneous code can lead to significant capital loss. The ability to seamlessly transition from agent-led automation to human-led verification creates a "Human-in-the-Loop" architecture that is essential for risk management in trading systems.1

#### **1.1.2 Trust Through Artifacts**

A recurring challenge in AI-assisted development is the "black box" problem. Antigravity solves this via **Artifacts**—verifiable, structured outputs generated by agents. Instead of simply stating "I fixed the bug," an Antigravity agent produces a *Task List* outlining its plan, an *Implementation Plan* detailing the file changes, and a *Walkthrough* demonstrating the fix in a simulated environment.4 For the OANDA-Nautilus integration, this feature is invaluable. An agent can be tasked to "Verify the OANDA adapter's order reconciliation logic," and the resulting Artifact would be a log of the agent spinning up a test container, placing a dummy trade on OANDA's practice API, and confirming that the Nautilus engine correctly updated its internal state.1

### **1.2 The "Headless" Runtime and Continuous Operations**

For a trading system, the development environment is only half the equation; the runtime environment is critical. Antigravity supports a "Headless" mode, allowing agents to persist outside the graphical interface.6 This capability enables the deployment of "Guardian Agents" that run continuously on a server (e.g., via Docker or CLI). These headless agents can monitor the live trading system, analyze logs for anomalies (such as latency spikes or API disconnects), and even autonomously execute remediation scripts defined in their "Skills" library.7 This moves the system from "Automated Trading" (static rules) to "Autonomous Trading" (dynamic, self-healing infrastructure).

## ---

**2\. The Execution Layer: NautilusTrader Architecture**

### **2.1 The Case for Hybrid Rust/Python Architectures**

In the high-stakes domain of algorithmic trading, the execution engine is the bedrock of reliability. **NautilusTrader** has been selected as the execution core for this multi-agent process due to its uncompromising focus on performance and safety.2 Unlike purely Python-based frameworks (such as Backtrader), NautilusTrader utilizes a hybrid architecture. The core components—event loop, matching engine, and order management system—are written in Rust, a systems programming language known for memory safety and zero-cost abstractions. This Rust core is wrapped in Python, providing the developer with the ease of use of the Python ecosystem (including integration with data science libraries like Pandas/NumPy) while retaining the execution speed of a compiled language.8

This architecture addresses a critical vulnerability in Python-only systems: the Global Interpreter Lock (GIL). In a pure Python backtester, heavy calculation in a strategy can block the processing of incoming market data, leading to artificial latency in simulations that does not exist in reality (or vice versa). NautilusTrader's asynchronous, Rust-based networking stack (built on tokio) allows for non-blocking I/O, ensuring that market data ingestion and order transmission occur concurrently with strategy logic.2

### **2.2 Solving the Parity Problem**

One of the most pervasive failures in quantitative finance is the "Parity Gap"—the discrepancy between how a strategy performs in a backtest and how it performs live. NautilusTrader is designed specifically to eliminate this. It employs a unified event-driven engine that runs the *exact same* strategy code in both modes.9 In backtesting, the engine simulates the exchange matching logic (including latency and queue position); in live trading, it swaps the simulator for a live exchange adapter. This ensures that the "Engineer Agent" in our Antigravity workflow only needs to write the strategy logic once. The "QA Agent" can then verify parity by running the strategy against historical data and comparing the transaction logs with a "Paper Trading" session on OANDA, confident that the underlying engine mechanics are identical.8

### **2.3 The Integration Challenge: OANDA**

Despite its robust architecture, NautilusTrader's native support for OANDA is, as of early 2026, noticeably absent from the standard distribution.11 While adapters exist for crypto exchanges (Binance, Bybit) and institutional brokers (Interactive Brokers), the forex-centric OANDA integration remains a community or custom endeavor. This presents a specific engineering challenge for our multi-agent process: we cannot simply "plug and play." Instead, we must utilize the Antigravity agents to *construct* the integration. This involves building a bridge between NautilusTrader's strict, typed Rust/Python interface and OANDA's REST (v20) and Streaming APIs.13 The subsequent sections of this report will detail the precise architectural patterns required to build this adapter, transforming a potential weakness into a bespoke, high-performance asset.

## ---

**3\. The Research Layer: VectorBT Pro vs. Free Alternatives**

Before execution comes discovery. The "Research Layer" is where the "Quant Agent" operates, sifting through terabytes of data to find statistical anomalies. The choice of tool here dictates the velocity of innovation.

### **3.1 VectorBT Pro: The Industrial-Grade Engine**

**VectorBT Pro** (VBT Pro) is the proprietary successor to the open-source VectorBT library. It represents the pinnacle of "Vectorized Backtesting".14 Unlike event-driven systems (like Nautilus) that iterate through data row-by-row (simulating time), vectorized systems operate on the entire dataset simultaneously using linear algebra. VBT Pro extends this by treating trading strategies as hyper-dimensional arrays.

#### **3.1.1 Dimensionality and Speed**

In VBT Pro, a strategy is not a loop; it is a tensor. One dimension represents time, another represents assets, and a third represents parameter combinations. This allows the "Research Agent" to test 10,000 different Moving Average crossover combinations across 50 currency pairs in a matter of seconds.15 The library leverages Numba to compile Python code into machine code, bypassing the slowness of the Python interpreter for mathematical operations. For a multi-agent system, this speed is critical. It allows the "Research Agent" to perform continuous "Grid Search" or "Random Search" optimizations in near real-time, feeding only the most promising candidates to the slower, more accurate NautilusTrader engine for validation.16

#### **3.1.2 Memory Efficiency and Chunking**

A major limitation of vectorized backtesting is memory consumption—loading 10 years of tick data into RAM is often impossible. VBT Pro introduces "Chunking" mechanics (e.g., @vbt.chunked), which intelligently breaks operations into manageable pieces that fit in memory, processing them in parallel across all available CPU cores.14 This feature alone often justifies the subscription cost (\~$25/month) for serious practitioners, as it enables the analysis of high-frequency data (M1 or S5 bars) that would crash open-source alternatives.17

### **3.2 Free Alternatives: The Trade-Offs**

#### **3.2.1 Backtesting.py**

**Backtesting.py** is a popular free alternative that sits comfortably between vectorization and event-driven design. It is lightweight, easy to install, and produces high-quality interactive HTML plots out of the box.18 However, it lacks the raw scale of VBT Pro. It is primarily designed for testing a *single* strategy on a *single* asset. While it allows for parameter optimization, it uses standard multiprocessing which is less efficient than VBT's compiled arrays.

* *Suitability*: Ideal for the "Prototyping Phase" where the user wants to visually inspect a strategy's logic on a chart. It is less suitable for the "Mining Phase" of checking millions of combinations.

#### **3.2.2 The Open-Source VectorBT**

The original VectorBT library remains free and functional. It offers the core vectorized speed but lacks the advanced features of Pro, such as built-in portfolio optimization, signal generators, and the dedicated "Chunking" engine.19 It serves as an excellent entry point. A cost-effective SOP is to have the "Research Agent" start with the free version; if the strategy complexity grows or memory limits are hit, the architecture allows for a seamless upgrade to Pro codebases.20

#### **3.2.3 NautilusTrader (Backtest Mode)**

It is crucial to note that NautilusTrader itself is free and includes a backtester. However, it is an *event-driven* backtester. It is accurate but slow compared to vectorization.

* *Strategic Insight*: The optimal workflow utilizes **VectorBT Pro** for "Broad" research (filtering 1,000,000 ideas to 100\) and **NautilusTrader** for "Deep" research (filtering 100 ideas to 1, accounting for spread, latency, and slippage).

## ---

**4\. Architectural Design: The Custom OANDA Adapter**

The most technically demanding requirement of this user query is the integration of OANDA with NautilusTrader. Since no official adapter exists, this section provides the precise architectural specification that the "Integration Agent" in Antigravity must implement.

### **4.1 Integration Concept**

NautilusTrader uses a modular adapter system. To connect a new venue (OANDA), we must implement three primary components that interface with the nautilus\_trader.adapters base classes 13:

1. **InstrumentProvider**: Defines the physical properties of the assets (e.g., EUR/USD pip size).  
2. **DataClient**: Handles the ingestion of real-time prices and historical data.  
3. **ExecutionClient**: Handles the submission of orders and the reconciliation of account state.

The adapter must bridge the gap between OANDA's REST/Stream APIs (JSON-based) and NautilusTrader's internal Cython/Rust objects.

### **4.2 Component 1: The OandaInstrumentProvider**

Nautilus is strict about data types. It does not "guess" that EUR/USD has 5 decimal places; it must be told.

* **Mechanism**: The provider must query OANDA's v3/accounts/{ID}/instruments endpoint.  
* **Data Mapping**:  
  * OANDA name ("EUR\_USD") ![][image1] Nautilus Symbol("EUR/USD").  
  * OANDA pipLocation (e.g., \-4) ![][image1] Nautilus tick\_size (![][image2]).  
  * OANDA minimumTradeSize ![][image1] Nautilus lot\_size.  
* **Agent Directive**: The Antigravity agent must be instructed to fetch the raw JSON from OANDA's API documentation and generate a Pydantic model that parses this into the NautilusInstrument definition.

### **4.3 Component 2: The OandaDataClient (Streaming)**

OANDA provides a streaming API for prices (stream-fxtrade.oanda.com). This must be wrapped in an asynchronous Python client (using aiohttp or oandapyV20's async capabilities).

* **Architecture**:  
  * The client establishes a persistent HTTP chunked connection.  
  * It listens for JSON lines containing PRICE events.  
  * **Timestamp Normalization**: OANDA uses RFC3339 strings (e.g., "2026-01-28T12:00:01.123456Z"). Nautilus requires UNIX nanoseconds (int64). The adapter must implement a highly efficient parsing function (e.g., using ciso8601) to minimize latency during this conversion.11  
  * **Event Dispatch**: The converted object is wrapped in a Nautilus QuoteTick and pushed to the internal MessageBus.

### **4.4 Component 3: The OandaExecutionClient (Orders & State)**

This is the critical path for risk. The client must translate Nautilus Order objects into OANDA REST calls (POST /v3/accounts/{ID}/orders).

* **Identity Reconciliation**: Nautilus generates a unique client-side UUID for every order (client\_order\_id). OANDA supports a clientExtensions field in their API. It is *mandatory* to map the Nautilus ID to this OANDA field.  
  * *Why?* If the application crashes and restarts, Nautilus needs to know which OANDA orders belong to it. On startup, the reconcile() method queries open orders from OANDA, reads the clientExtensions ID, and re-hydrates the internal Nautilus state. Without this, the system would lose track of open positions.13  
* **Rate Limiting**: OANDA limits request rates. The adapter must implement a "Token Bucket" limiter to queue orders if the limit is reached, protecting the account from API bans.

## ---

**5\. Standard Operating Procedures (SOPs)**

The following SOPs are designed to be executed by the human "Architect" supervising the Antigravity "Agents." They represent the "Playbook" for the entire project.

### **SOP 1: Workspace Initialization and Agent Configuration**

**Objective**: Establish the "Mission Control" environment in Google Antigravity.

1. **Installation & Setup**:  
   * Download Google Antigravity from the official portal (antigravity.google).  
   * Authenticate and launch the **Agent Manager**.  
   * **Action**: Create a new Workspace named Titan-Oanda-Algo.  
2. **Defining the "Rules of Engagement"**:  
   * Create a root-level file .antigravity/rules.md. This file governs the behavior of all agents in the workspace.5  
   * *Content Requirement*:  
     * "All Python code must use uv for dependency management."  
     * "All financial data types must use decimal.Decimal or Nautilus native types, never standard floats."  
     * "Documentation must follow Google Style Guide."  
3. **Initializing the Agent Team**:  
   * In the Agent Manager, define three persistent agents:  
     * **Architect**: (Model: Gemini 3 Pro) \- Responsible for file structure and high-level design.  
     * **Engineer**: (Model: Gemini 3 Pro / Claude Sonnet) \- Responsible for writing Rust/Python code and API adapters.  
     * **Researcher**: (Model: Gemini 3 Pro) \- Responsible for VectorBT scripts and Jupyter notebooks.

### **SOP 2: The Adapter Construction Workflow**

**Objective**: Build the nautilus\_oanda adapter package.

1. **Context Loading**:  
   * Upload the OANDA v20 API specification (JSON/YAML) and the NautilusTrader adapter\_guide.md to the **Engineer** agent's context window.  
2. **Phase 1: Instrumentation**:  
   * *Prompt*: "Engineer Agent, create a Python module oanda\_instrument\_provider.py. It should query the OANDA Account Instruments endpoint and return a list of Nautilus Instrument objects. Ensure pipLocation is correctly converted to a float scalar."  
   * *Verification*: Request the agent to generate a test script tests/test\_instrument\_parsing.py that mocks the OANDA JSON response and asserts that the resulting Nautilus object has the correct tick\_size.  
3. **Phase 2: Streaming Data**:  
   * *Prompt*: "Engineer Agent, implement OandaDataClient. It must use aiohttp to listen to the OANDA pricing stream. Map the bids and asks to QuoteTick. Handle network disconnects with an exponential backoff retry logic."  
4. **Phase 3: Execution Logic**:  
   * *Prompt*: "Engineer Agent, implement OandaExecutionClient. Map MarketOrder and LimitOrder to OANDA's order body. **Crucial**: Map order.client\_order\_id to OANDA's clientExtensions.id tag."

### **SOP 3: The Alpha Research Loop (VectorBT Pro)**

**Objective**: Discover a viable trading strategy.

1. **Data Ingestion**:  
   * *Prompt*: "Researcher Agent, use the oandapyV20 library to download 1 year of M5 (5-minute) OHLC data for EUR/USD, GBP/USD, and AUD/USD. Save as Parquet files in data/raw."  
2. **Strategy Optimization**:  
   * *Prompt*: "Create a VectorBT Pro script. Define a strategy based on RSI (14) \< 30 for Long and RSI (14) \> 70 for Short. Use vbt.parameterized to test RSI periods from 10 to 20\. Use @vbt.chunked to manage memory. Output a heatmap of Sharpe Ratios."  
3. **Candidate Selection**:  
   * Review the generated Artifact (Heatmap). Identify parameters that show a "Plateau of Stability"—a region where neighbors are also profitable (avoiding overfitting).  
4. **Parity Transfer**:  
   * *Prompt*: "Architect Agent, take the optimal parameters from the VBT result (RSI=12, Window=5m) and generate a NautilusTrader configuration file config/strategy\_config.toml."

### **SOP 4: Free Alternative Research Loop (Backtesting.py)**

**Objective**: Validating strategy logic without VBT Pro.

1. **Setup**:  
   * *Prompt*: "Engineer Agent, install backtesting. Create a wrapper class that loads the OANDA Parquet data into the specific Pandas format required by backtesting.py."  
2. **Logic Implementation**:  
   * *Prompt*: "Implement the RSI strategy as a class inheriting from backtesting.Strategy. Note that backtesting.py processes bar-by-bar. Ensure the logic I(ta.rsi, self.data.Close) is calculated correctly."  
3. **Validation**:  
   * Since backtesting.py cannot easily do portfolio-wide optimization, use it to visually inspect the trade entries on the HTML plot it generates. Ensure the logic "makes sense" visually (e.g., buying at dips).

### **SOP 5: Live Deployment and Monitoring**

**Objective**: Deploy the nautilus\_oanda system to production.

1. **Containerization**:  
   * *Prompt*: "DevOps Agent, generate a Dockerfile. Base image: python:3.11-slim. Install nautilus\_trader from the wheel. Copy the custom oanda\_adapter package. Entrypoint: python main.py."  
2. **Infrastructure Provisioning**:  
   * Use Antigravity to deploy this container to a **Google Compute Engine** instance (e.g., e2-standard-2) located in us-east4 (Northern Virginia) or europe-west2 (London) depending on OANDA's server location for lowest latency.21  
3. **Headless Monitoring**:  
   * Run a local Antigravity agent in "Headless Mode" on your workstation or a separate lightweight server.  
   * *Command*: antigravity run \--agent "Guardian" \--task "Monitor Nautilus logs via SSH. If 'ERROR' appears, send Slack notification.".6

## ---

**6\. Technical Deep Dive: Data Structures and Latency**

### **6.1 The Data Normalization Imperative**

One of the most frequent causes of failure in OANDA integrations is unit confusion.

* **OANDA**: Often reports prices as string "1.08345" or uses pipLocation to indicate precision.  
* **Nautilus**: Uses rust\_decimal under the hood. It demands exact precision handling.  
* **Solution**: The adapter must strictly convert incoming strings to Decimal before passing them to Nautilus. Floating point math (e.g., 1.1 \+ 0.2) creates micro-errors (1.300000001) that can cause order rejection due to precision mismatch. The Antigravity "Engineer Agent" should be explicitly instructed to use decimal.Decimal for all price parsing logic.

### **6.2 Latency Considerations**

OANDA is a retail broker; it does not offer FIX API to everyone (typically requires high volume/deposit). The v20 REST API has network overhead.

* **Implication**: Your "Tick-to-Trade" latency will likely be in the 50ms \- 200ms range.  
* **Mitigation**: The Nautilus architecture handles this gracefully via its asynchronous event loop. While the strategy waits for the HTTP 200 OK from OANDA confirming the order, the engine continues to process incoming tick data, ensuring the internal view of the market remains fresh. This is superior to synchronous loops (like in simple Python scripts) which "freeze" while waiting for the network.

## ---

**7\. Comparative Analysis: VectorBT Pro vs. Alternatives**

The choice of research tool fundamentally shapes the workflow.

| Feature | VectorBT Pro (VBT Pro) | Backtesting.py | Nautilus (Backtest) |
| :---- | :---- | :---- | :---- |
| **Paradigm** | Vectorized (Hyper-Arrays) | Event-based (Iterative) | Event-Driven (Accurate) |
| **Speed (1M bars)** | \< 1 Second (Parallelized) | \~30 Seconds | \~2 Minutes |
| **Memory** | Efficient (Chunking) | High (Loads all into RAM) | Moderate |
| **Portfolio Logic** | Native (Matrix math) | Difficult (Single asset focus) | Native (Account object) |
| **Learning Curve** | High (Requires Linear Algebra mindset) | Low (Simple OOP) | High (Requires System mindset) |
| **Cost** | \~$25/mo \- $500 Lifetime | Free (Open Source) | Free (Open Core) |

**Strategic Recommendation**:

* Use **VectorBT Pro** if your strategy relies on "Market Wide" phenomena (e.g., "Buy the strongest 3 currencies against the weakest 3"). The array operations make this trivial.  
* Use **Backtesting.py** if you are trading a single pair with standard indicators and have zero budget.  
* Use **Nautilus Backtester** as the final "Gatekeeper" before live. It is the only one that simulates the specific quirks of the OANDA adapter you just built.

## ---

**8\. Conclusion**

The architecture detailed in this report represents a sophisticated, modern approach to algorithmic trading. By leveraging **Google Antigravity**, the user transcends the role of a mere coder and becomes a systems architect. The agents handle the tedious, error-prone work of mapping API fields and writing boilerplate adapter code, allowing the human to focus on strategy and risk.

While the lack of a native OANDA adapter for **NautilusTrader** is a hurdle, it is not a blockade. With the provided SOPs and the agentic capabilities of Antigravity, creating a custom, high-performance integration is a manageable task. When combined with the research velocity of **VectorBT Pro**, this stack constitutes a formidable "Individual Quantitative Hedge Fund" infrastructure, capable of competing in the 2026 marketplace with institutional-grade rigor.

### **Final Checklist for the User**

1. **Verify**: Ensure your OANDA account is v20 enabled.  
2. **Install**: Get the latest antigravity CLI and uv package manager.  
3. **Prompt**: Begin with the "Engineer Agent" to build the InstrumentProvider—this is the foundation upon which the Data and Execution clients rest.  
4. **Test**: Never deploy without a verified "Walkthrough" artifact from your Antigravity agent confirming correct order reconciliation in the OANDA sandbox.

#### **Works cited**

1. Build with Google Antigravity, our new agentic development platform, accessed on January 28, 2026, [https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/)  
2. Overview | NautilusTrader Documentation, accessed on January 28, 2026, [https://nautilustrader.io/docs/latest/concepts/overview/](https://nautilustrader.io/docs/latest/concepts/overview/)  
3. Introduction \- Oanda API, accessed on January 28, 2026, [https://developer.oanda.com/rest-live-v20/introduction/](https://developer.oanda.com/rest-live-v20/introduction/)  
4. Getting Started with Google Antigravity, accessed on January 28, 2026, [https://codelabs.developers.google.com/getting-started-google-antigravity](https://codelabs.developers.google.com/getting-started-google-antigravity)  
5. Tutorial : Getting Started with Google Antigravity | by Romin Irani \- Medium, accessed on January 28, 2026, [https://medium.com/google-cloud/tutorial-getting-started-with-google-antigravity-b5cc74c103c2](https://medium.com/google-cloud/tutorial-getting-started-with-google-antigravity-b5cc74c103c2)  
6. Antigravity subagents using Gemini-CLI : r/google\_antigravity \- Reddit, accessed on January 28, 2026, [https://www.reddit.com/r/google\_antigravity/comments/1px3nl2/antigravity\_subagents\_using\_geminicli/](https://www.reddit.com/r/google_antigravity/comments/1px3nl2/antigravity_subagents_using_geminicli/)  
7. Tutorial : Getting Started with Google Antigravity Skills, accessed on January 28, 2026, [https://medium.com/google-cloud/tutorial-getting-started-with-antigravity-skills-864041811e0d](https://medium.com/google-cloud/tutorial-getting-started-with-antigravity-skills-864041811e0d)  
8. nautechsystems/nautilus\_trader: A high-performance algorithmic trading platform and event-driven backtester \- GitHub, accessed on January 28, 2026, [https://github.com/nautechsystems/nautilus\_trader](https://github.com/nautechsystems/nautilus_trader)  
9. NautilusTrader, accessed on January 28, 2026, [https://nautilustrader.io/](https://nautilustrader.io/)  
10. Chapter 1: Introduction to NautilusTrader \- DEV Community, accessed on January 28, 2026, [https://dev.to/henry\_lin\_3ac6363747f45b4/chapter-1-introduction-to-nautilustrader-5552](https://dev.to/henry_lin_3ac6363747f45b4/chapter-1-introduction-to-nautilustrader-5552)  
11. Integrations | NautilusTrader Documentation, accessed on January 28, 2026, [https://nautilustrader.io/docs/latest/integrations/](https://nautilustrader.io/docs/latest/integrations/)  
12. zr7goat/nautilus\_trader\_Jerry: A high-performance algorithmic trading platform and event-driven backtester \- GitHub, accessed on January 28, 2026, [https://github.com/zr7goat/nautilus\_trader\_Jerry](https://github.com/zr7goat/nautilus_trader_Jerry)  
13. Adapters | NautilusTrader Documentation, accessed on January 28, 2026, [https://nautilustrader.io/docs/nightly/developer\_guide/adapters/](https://nautilustrader.io/docs/nightly/developer_guide/adapters/)  
14. VectorBT® PRO: Getting started, accessed on January 28, 2026, [https://vectorbt.pro/](https://vectorbt.pro/)  
15. Is free version of vectorbt a viable choice? Or I should choose another framework? \- Reddit, accessed on January 28, 2026, [https://www.reddit.com/r/algotrading/comments/yjkei4/is\_free\_version\_of\_vectorbt\_a\_viable\_choice\_or\_i/](https://www.reddit.com/r/algotrading/comments/yjkei4/is_free_version_of_vectorbt_a_viable_choice_or_i/)  
16. Battle-Tested Backtesters: Comparing VectorBT, Zipline, and Backtrader for Financial Strategy Development | by Trading Dude | Medium, accessed on January 28, 2026, [https://medium.com/@trading.dude/battle-tested-backtesters-comparing-vectorbt-zipline-and-backtrader-for-financial-strategy-dee33d33a9e0](https://medium.com/@trading.dude/battle-tested-backtesters-comparing-vectorbt-zipline-and-backtrader-for-financial-strategy-dee33d33a9e0)  
17. Become a member \- VectorBT® PRO, accessed on January 28, 2026, [https://vectorbt.pro/become-a-member/](https://vectorbt.pro/become-a-member/)  
18. Backtrader Alternatives for Strategies Backtesting \- Forex Tester Online, accessed on January 28, 2026, [https://forextester.com/blog/backtrader-alternatives/](https://forextester.com/blog/backtrader-alternatives/)  
19. VectorBT \- An Introductory Guide \- AlgoTrading101 Blog, accessed on January 28, 2026, [https://algotrading101.com/learn/vectorbt-guide/](https://algotrading101.com/learn/vectorbt-guide/)  
20. VectorBT – An Introductory Guide | IBKR Quant, accessed on January 28, 2026, [https://www.interactivebrokers.com/campus/ibkr-quant-news/vectorbt-an-introductory-guide/](https://www.interactivebrokers.com/campus/ibkr-quant-news/vectorbt-an-introductory-guide/)  
21. Cheapest Forex VPS in 2026 | Low-Latency Hosting for Traders \- QuantVPS, accessed on January 28, 2026, [https://www.quantvps.com/blog/cheapest-forex-vps](https://www.quantvps.com/blog/cheapest-forex-vps)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAXCAYAAADpwXTaAAAAiElEQVR4XmNgGAWjgGqAA4jTgJgHXYIcwAjErUBsjC5BLgAZ1AvELOgS5ACQ6wqAOA7KRgECQCxJIpYD4vlAPBmI+RiggBuIq4F4Fhl4BxB/BeJmIGZnoACYAPFqIJZBlyAVCAPxYiCWR5cgB2QBcQS6IDkAlGinArE0ugQ5AJQUeKH0KBhMAABVixNKp22j3QAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHUAAAAXCAYAAAA1OADtAAADjElEQVR4Xu2YTahOQRjHnxuKkLgiRe5FZCEKiZCFRPIRkq8oykKyQ2woWbCQj6JYyEIsbG0QVzbCQgoLSeQjihVCxP9/nzPuvGPm3Hk/zr3n1fzr13vOc2aec2b+c+adMyJJSQVoCDgFRrgXkppTLWAfeAlGOdeSmlQzwHHwUJKphaoNrHODliaBo+As2AAGVF6OFqfd3WCulMPUWtvF2WYWOAlOg6WgT0UJVUx+xniNZViWdULiPdaK+uXVZLAD3AS/wIXKy3+1GjwB08AgcAhcFzWoWm0Wve906X1Ta20XDd0DboN20AouiprSzyoXk5/HjPEay7As67CuEU1fBk6AN+CLaP95xc5dCeaA1+I3dQx4BjZasaHgPtiZnfcFu0Qb5eOA6ANPBVuzOr1taky7QuKzvxedbYzGia4RFmfnsfn3ZjFeM2Kdp2Bkdk5Tl4AFon2Za6oRO5YP5DOVN3CTcKRyZHaImhWrw+COaL1H4Ce4JvnTTVGqp11sh7vIGyzatvOieWLyG5Pdfp8JPoPlTpziIHDzepVnKv8zfElY9p3oCK1FnE7cjulJ1dqu/uCq/PvsNKlDut66mPycKT9mMVusw7ocPK4aYipjviSheIw4lfAN/Q7OSc6ffoEKPX8obmTMC5lq4qE8dtyY5/Z7KE7Vbap5UF+S0EMXofXgVRU8ABM6a/pVT7tMX+WZynvz2JfHzs/Z6ncWs1WoqQPBDfEn6a7xZVY97eLi5bnkmzpe4vJzxupxU6lQI0PxZlHo+UNxI3eaDcVDeex4yLxQnGqIqfyz9iVhWX4GjXbiRYiLEz5jLHyb7O9Fn2ptFz/frkjYVK6AuRKOyc/FEhdNbr8bU/c7caohpnJZzY2JhVbMrAAJj4vWWLCmClaAYZ01w4ptF3dw2qxzih3LVStXr0bDwWPRVS8Vk98MBLcfWedH9uuqalP5DdXiXGsF98BBK8aFAEdb3rZi2RXbrm2i/3uXRN9SylduHvgAZmfnsfk3iS7u2rNz9j93l+6Kf2eLpn4V/Zb1iiOBN+GI4oMTfvRyY2CKVY4b8C9Et8b4JvBb7Ih0P8WVXTHt4gr1W1bGHvCrROtuB1tEt/a45WqXicnP4zPglujuHg3lG8/tQiMu7C6DT9LlE3kLjlnlqhYTLxK9MbfA/hfV0y6+jTSd8NinmPwcCBNFjZ8vzf+yJCUlJSUlJSWVS38AmDwrjs08/iQAAAAASUVORK5CYII=>