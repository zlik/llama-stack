---
orphan: true
---
# Qdrant

[Qdrant](https://qdrant.tech/documentation/) is an inline and remote vector database provider for Llama Stack. It
allows you to store and query vectors directly in memory.
That means you'll get fast and efficient vector retrieval.

> By default, Qdrant stores vectors in RAM, delivering incredibly fast access for datasets that fit comfortably in
> memory. But when your dataset exceeds RAM capacity, Qdrant offers Memmap as an alternative.
>
> \[[An Introduction to Vector Databases](https://qdrant.tech/articles/what-is-a-vector-database/)\]



## Features

- Lightweight and easy to use
- Fully integrated with Llama Stack
- Apache 2.0 license terms
- Store embeddings and their metadata
- Supports search by
  [Keyword](https://qdrant.tech/articles/qdrant-introduces-full-text-filters-and-indexes/)
  and [Hybrid](https://qdrant.tech/articles/hybrid-search/#building-a-hybrid-search-system-in-qdrant) search
- [Multilingual and Multimodal retrieval](https://qdrant.tech/documentation/multimodal-search/)
- [Medatata filtering](https://qdrant.tech/articles/vector-search-filtering/)
- [GPU support](https://qdrant.tech/documentation/guides/running-with-gpu/)

## Usage

To use Qdrant in your Llama Stack project, follow these steps:

1. Install the necessary dependencies.
2. Configure your Llama Stack project to use Qdrant.
3. Start storing and querying vectors.

## Installation

You can install Qdrant using docker:

```bash
docker pull qdrant/qdrant
```
## Documentation
See the [Qdrant documentation](https://qdrant.tech/documentation/) for more details about Qdrant in general.
