# Llama Stack

[![PyPI version](https://img.shields.io/pypi/v/llama_stack.svg)](https://pypi.org/project/llama_stack/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/llama-stack)](https://pypi.org/project/llama-stack/)
[![License](https://img.shields.io/pypi/l/llama_stack.svg)](https://github.com/meta-llama/llama-stack/blob/main/LICENSE)
[![Discord](https://img.shields.io/discord/1257833999603335178)](https://discord.gg/llama-stack)
[![Unit Tests](https://github.com/meta-llama/llama-stack/actions/workflows/unit-tests.yml/badge.svg?branch=main)](https://github.com/meta-llama/llama-stack/actions/workflows/unit-tests.yml?query=branch%3Amain)
[![Integration Tests](https://github.com/meta-llama/llama-stack/actions/workflows/integration-tests.yml/badge.svg?branch=main)](https://github.com/meta-llama/llama-stack/actions/workflows/integration-tests.yml?query=branch%3Amain)

[**Quick Start**](https://llama-stack.readthedocs.io/en/latest/getting_started/index.html) | [**Documentation**](https://llama-stack.readthedocs.io/en/latest/index.html) | [**Colab Notebook**](./docs/getting_started.ipynb)

Llama Stack standardizes the core building blocks that simplify AI application development. It codifies best practices across the Llama ecosystem. More specifically, it provides

- **Unified API layer** for Inference, RAG, Agents, Tools, Safety, Evals, and Telemetry.
- **Plugin architecture** to support the rich ecosystem of different API implementations in various environments, including local development, on-premises, cloud, and mobile.
- **Prepackaged verified distributions** which offer a one-stop solution for developers to get started quickly and reliably in any environment.
- **Multiple developer interfaces** like CLI and SDKs for Python, Typescript, iOS, and Android.
- **Standalone applications** as examples for how to build production-grade AI applications with Llama Stack.

<div style="text-align: center;">
  <img
    src="https://github.com/user-attachments/assets/33d9576d-95ea-468d-95e2-8fa233205a50"
    width="480"
    title="Llama Stack"
    alt="Llama Stack"
  />
</div>

### Llama Stack Benefits
- **Flexible Options**: Developers can choose their preferred infrastructure without changing APIs and enjoy flexible deployment choices.
- **Consistent Experience**: With its unified APIs, Llama Stack makes it easier to build, test, and deploy AI applications with consistent application behavior.
- **Robust Ecosystem**: Llama Stack is already integrated with distribution partners (cloud providers, hardware vendors, and AI-focused companies) that offer tailored infrastructure, software, and services for deploying Llama models.

By reducing friction and complexity, Llama Stack empowers developers to focus on what they do best: building transformative generative AI applications.

### API Providers
Here is a list of the various API providers and available distributions that can help developers get started easily with Llama Stack.

| **API Provider Builder** |    **Environments**    | **Agents** | **Inference** | **Memory** | **Safety** | **Telemetry** |
|:------------------------:|:----------------------:|:----------:|:-------------:|:----------:|:----------:|:-------------:|
|      Meta Reference      |      Single Node       |     ✅      |       ✅       |     ✅      |     ✅      |       ✅       |
|        SambaNova         |         Hosted         |            |       ✅       |            |            |               |
|         Cerebras         |         Hosted         |            |       ✅       |            |            |               |
|        Fireworks         |         Hosted         |     ✅      |       ✅       |     ✅      |            |               |
|       AWS Bedrock        |         Hosted         |            |       ✅       |            |     ✅      |               |
|         Together         |         Hosted         |     ✅      |       ✅       |            |     ✅      |               |
|           Groq           |         Hosted         |            |       ✅       |            |            |               |
|          Ollama          |      Single Node       |            |       ✅       |            |            |               |
|           TGI            | Hosted and Single Node |            |       ✅       |            |            |               |
|        NVIDIA NIM        | Hosted and Single Node |            |       ✅       |            |            |               |
|          Chroma          |      Single Node       |            |               |     ✅      |            |               |
|        PG Vector         |      Single Node       |            |               |     ✅      |            |               |
|    PyTorch ExecuTorch    |     On-device iOS      |     ✅      |       ✅       |            |            |               |
|           vLLM           | Hosted and Single Node |            |       ✅       |            |            |               |
|          OpenAI          |         Hosted         |            |       ✅       |            |            |               |
|        Anthropic         |         Hosted         |            |       ✅       |            |            |               |
|          Gemini          |         Hosted         |            |       ✅       |            |            |               |


### Distributions

A Llama Stack Distribution (or "distro") is a pre-configured bundle of provider implementations for each API component. Distributions make it easy to get started with a specific deployment scenario - you can begin with a local development setup (eg. ollama) and seamlessly transition to production (eg. Fireworks) without changing your application code. Here are some of the distributions we support:

|               **Distribution**                |                                                                    **Llama Stack Docker**                                                                     |                                                 Start This Distribution                                                  |
|:---------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------------------------------------------:|
|                Meta Reference                 |           [llamastack/distribution-meta-reference-gpu](https://hub.docker.com/repository/docker/llamastack/distribution-meta-reference-gpu/general)           |      [Guide](https://llama-stack.readthedocs.io/en/latest/distributions/self_hosted_distro/meta-reference-gpu.html)      |
|           Meta Reference Quantized            | [llamastack/distribution-meta-reference-quantized-gpu](https://hub.docker.com/repository/docker/llamastack/distribution-meta-reference-quantized-gpu/general) | [Guide](https://llama-stack.readthedocs.io/en/latest/distributions/self_hosted_distro/meta-reference-quantized-gpu.html) |
|                   SambaNova                   |                     [llamastack/distribution-sambanova](https://hub.docker.com/repository/docker/llamastack/distribution-sambanova/general)                     |   [Guide](https://llama-stack.readthedocs.io/en/latest/distributions/self_hosted_distro/sambanova.html)   |
|                   Cerebras                    |                     [llamastack/distribution-cerebras](https://hub.docker.com/repository/docker/llamastack/distribution-cerebras/general)                     |   [Guide](https://llama-stack.readthedocs.io/en/latest/distributions/self_hosted_distro/cerebras.html)   |
|                    Ollama                     |                       [llamastack/distribution-ollama](https://hub.docker.com/repository/docker/llamastack/distribution-ollama/general)                       |            [Guide](https://llama-stack.readthedocs.io/en/latest/distributions/self_hosted_distro/ollama.html)            |
|                      TGI                      |                          [llamastack/distribution-tgi](https://hub.docker.com/repository/docker/llamastack/distribution-tgi/general)                          |             [Guide](https://llama-stack.readthedocs.io/en/latest/distributions/self_hosted_distro/tgi.html)              |
|                   Together                    |                     [llamastack/distribution-together](https://hub.docker.com/repository/docker/llamastack/distribution-together/general)                     |           [Guide](https://llama-stack.readthedocs.io/en/latest/distributions/self_hosted_distro/together.html)           |
|                   Fireworks                   |                    [llamastack/distribution-fireworks](https://hub.docker.com/repository/docker/llamastack/distribution-fireworks/general)                    |          [Guide](https://llama-stack.readthedocs.io/en/latest/distributions/self_hosted_distro/fireworks.html)           |
| vLLM |                  [llamastack/distribution-remote-vllm](https://hub.docker.com/repository/docker/llamastack/distribution-remote-vllm/general)                  |         [Guide](https://llama-stack.readthedocs.io/en/latest/distributions/self_hosted_distro/remote-vllm.html)          |


### Documentation

Please checkout our [Documentation](https://llama-stack.readthedocs.io/en/latest/index.html) page for more details.

* CLI references
    * [llama (server-side) CLI Reference](https://llama-stack.readthedocs.io/en/latest/references/llama_cli_reference/index.html): Guide for using the `llama` CLI to work with Llama models (download, study prompts), and building/starting a Llama Stack distribution.
    * [llama (client-side) CLI Reference](https://llama-stack.readthedocs.io/en/latest/references/llama_stack_client_cli_reference.html): Guide for using the `llama-stack-client` CLI, which allows you to query information about the distribution.
* Getting Started
    * [Quick guide to start a Llama Stack server](https://llama-stack.readthedocs.io/en/latest/getting_started/index.html).
    * [Jupyter notebook](./docs/getting_started.ipynb) to walk-through how to use simple text and vision inference llama_stack_client APIs
    * The complete Llama Stack lesson [Colab notebook](https://colab.research.google.com/drive/1dtVmxotBsI4cGZQNsJRYPrLiDeT0Wnwt) of the new [Llama 3.2 course on Deeplearning.ai](https://learn.deeplearning.ai/courses/introducing-multimodal-llama-3-2/lesson/8/llama-stack).
    * A [Zero-to-Hero Guide](https://github.com/meta-llama/llama-stack/tree/main/docs/zero_to_hero_guide) that guide you through all the key components of llama stack with code samples.
* [Contributing](CONTRIBUTING.md)
    * [Adding a new API Provider](https://llama-stack.readthedocs.io/en/latest/contributing/new_api_provider.html) to walk-through how to add a new API provider.

### Llama Stack Client SDKs

|  **Language** |  **Client SDK** | **Package** |
| :----: | :----: | :----: |
| Python |  [llama-stack-client-python](https://github.com/meta-llama/llama-stack-client-python) | [![PyPI version](https://img.shields.io/pypi/v/llama_stack_client.svg)](https://pypi.org/project/llama_stack_client/)
| Swift  | [llama-stack-client-swift](https://github.com/meta-llama/llama-stack-client-swift) | [![Swift Package Index](https://img.shields.io/endpoint?url=https%3A%2F%2Fswiftpackageindex.com%2Fapi%2Fpackages%2Fmeta-llama%2Fllama-stack-client-swift%2Fbadge%3Ftype%3Dswift-versions)](https://swiftpackageindex.com/meta-llama/llama-stack-client-swift)
| Typescript   | [llama-stack-client-typescript](https://github.com/meta-llama/llama-stack-client-typescript) | [![NPM version](https://img.shields.io/npm/v/llama-stack-client.svg)](https://npmjs.org/package/llama-stack-client)
| Kotlin | [llama-stack-client-kotlin](https://github.com/meta-llama/llama-stack-client-kotlin) | [![Maven version](https://img.shields.io/maven-central/v/com.llama.llamastack/llama-stack-client-kotlin)](https://central.sonatype.com/artifact/com.llama.llamastack/llama-stack-client-kotlin)

Check out our client SDKs for connecting to a Llama Stack server in your preferred language, you can choose from [python](https://github.com/meta-llama/llama-stack-client-python), [typescript](https://github.com/meta-llama/llama-stack-client-typescript), [swift](https://github.com/meta-llama/llama-stack-client-swift), and [kotlin](https://github.com/meta-llama/llama-stack-client-kotlin) programming languages to quickly build your applications.

You can find more example scripts with client SDKs to talk with the Llama Stack server in our [llama-stack-apps](https://github.com/meta-llama/llama-stack-apps/tree/main/examples) repo.
