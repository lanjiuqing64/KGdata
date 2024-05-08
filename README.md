# ODA: Observation-Driven Agent for integrating LLMs and Knowledge Graphs

## Overview

This repository contains the code and dataset associated with the paper [ODA: Observation-Driven Agent for integrating LLMs and Knowledge Graphs](https://arxiv.org/abs/2404.07677)

## The overall framework of ODA
![The framework of ODA](framework.png)



## Description

- The code and subgraph datasets used in the paper are here.
- In the `subgraphs` folder: This directory contains the generated 2-hop and 3rd-hop subgraphs. We deployed the Wikidata dump across five AWS EC2 instances, each consisting of a 768GB machine with 48 cores. The specific code used for generating the subgraphs can be found in `subgraph.py`.
- In the `simple_wikidata_db` folder: This directory contains the deployed Wikidata dump.

## Usage

1. Clone this repository:

    ```bash
    git clone <repository_url>
    ```

2. Explore the contents of the repository, including the code and dataset.

3. For generating subgraphs, refer to the `subgraph.py` script in the `subgraphs` folder.

4. For accessing the Wikidata dump, navigate to the `simple_wikidata_db` folder.

## Citation

If you use the code or dataset provided in this repository, please consider citing the following paper:

```
@article{oda2024,
  title={ODA: Observation-Driven Agent for integrating LLMs and Knowledge Graphs},
  author={Author(s)},
  journal={arXiv preprint arXiv:2404.07677},
  year={2024}
}
```

