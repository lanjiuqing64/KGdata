# ODA: Observation-Driven Agent for integrating LLMs and Knowledge Graphs

## Overview

This repository contains the code and dataset associated with the paper [ODA: Observation-Driven Agent for integrating LLMs and Knowledge Graphs](https://arxiv.org/abs/2404.07677)

## Abstract

The integration of Large Language Models (LLMs) and knowledge graphs (KGs) has achieved remarkable success in various natural language processing tasks. However, existing methodologies that integrate LLMs and KGs often navigate the task-solving process solely based on the LLM's analysis of the question, overlooking the rich cognitive potential inherent in the vast knowledge encapsulated in KGs. To address this, we introduce Observation-Driven Agent (ODA), a novel AI agent framework tailored for tasks involving KGs. ODA incorporates KG reasoning abilities via global observation that enhances reasoning capabilities through a cyclical paradigm of observation, action, and reflection. Confronting the exponential explosion of knowledge during observation, we innovatively design a recursive observation mechanism. Subsequently, we integrate the observed knowledge into the action and reflection modules. Through extensive experiments, ODA demonstrates state-of-the-art performance on several datasets, notably achieving accuracy improvements of 12.87% and 8.9%.


## The overall framework of ODA
![The framework of ODA](framework.png)



## Description

- The code and subgraph datasets used in the paper are here.
- In the `subgraphs` folder: This directory contains the generated 2-hop and the 3rd-hop subgraphs. We deployed the Wikidata dump across five AWS EC2 instances, each consisting of a 768GB machine with 48 cores. The specific code used for generating the subgraphs can be found in `subgraph.py`.
- In the `simple_wikidata_db` folder: This directory contains the deployed Wikidata dump.


## Citation

If you use the code or dataset provided in this repository, please consider citing the following paper:

```
@misc{sun2024oda,
      title={ODA: Observation-Driven Agent for integrating LLMs and Knowledge Graphs}, 
      author={Lei Sun and Zhengwei Tao and Youdi Li and Hiroshi Arakawa},
      year={2024},
      eprint={2404.07677},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

