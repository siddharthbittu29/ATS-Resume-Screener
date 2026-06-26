---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- generated_from_trainer
- dataset_size:165
- loss:CosineSimilarityLoss
base_model: sentence-transformers/all-mpnet-base-v2
widget:
- source_sentence: Sales Manager with 8 years of experience. Skilled in CRM, Sales,
    Leadership, Negotiation, Forecasting. Delivered multiple successful projects and
    collaborated with teams. Strong problem solving and analytical skills.
  sentences:
  - Looking for a Sales Manager. Required skills include CRM, Sales, Leadership, Negotiation,
    Forecasting. Candidate should possess strong communication skills and relevant
    industry experience.
  - Looking for a Cybersecurity Analyst. Required skills include SIEM, Network Security,
    Linux. Candidate should possess strong communication skills and relevant industry
    experience.
  - Looking for a Full Stack Developer. Required skills include React, Node.js, MongoDB.
    Candidate should possess strong communication skills and relevant industry experience.
- source_sentence: AI Engineer with 7 years of experience. Skilled in LLMs, Python,
    NLP, Transformers, Vector DB. Delivered multiple successful projects and collaborated
    with teams. Strong problem solving and analytical skills.
  sentences:
  - Looking for a Marketing Manager. Required skills include SEO, Content Marketing,
    Analytics. Candidate should possess strong communication skills and relevant industry
    experience.
  - Looking for a Marketing Manager. Required skills include SEO, Content Marketing,
    Analytics. Candidate should possess strong communication skills and relevant industry
    experience.
  - Looking for a Backend Developer. Required skills include Java, Spring Boot, SQL.
    Candidate should possess strong communication skills and relevant industry experience.
- source_sentence: Backend Developer with 8 years of experience. Skilled in Java,
    Spring Boot, SQL, REST API, Docker. Delivered multiple successful projects and
    collaborated with teams. Strong problem solving and analytical skills.
  sentences:
  - Looking for a Marketing Manager. Required skills include SEO, Content Marketing,
    Analytics, Branding, Campaigns. Candidate should possess strong communication
    skills and relevant industry experience.
  - Looking for a DevOps Engineer. Required skills include Docker, Kubernetes, CI/CD,
    AWS, Linux. Candidate should possess strong communication skills and relevant
    industry experience.
  - Looking for a DevOps Engineer. Required skills include Docker, Kubernetes, CI/CD,
    AWS, Linux. Candidate should possess strong communication skills and relevant
    industry experience.
- source_sentence: Cloud Engineer with 2 years of experience. Skilled in AWS, Docker,
    Kubernetes, Terraform, Linux. Delivered multiple successful projects and collaborated
    with teams. Strong problem solving and analytical skills.
  sentences:
  - Looking for a DevOps Engineer. Required skills include Docker, Kubernetes, CI/CD,
    AWS, Linux. Candidate should possess strong communication skills and relevant
    industry experience.
  - Looking for a HR Specialist. Required skills include Recruitment, Onboarding,
    Communication, HRMS, Employee Relations. Candidate should possess strong communication
    skills and relevant industry experience.
  - Looking for a AI Engineer. Required skills include LLMs, Python, NLP. Candidate
    should possess strong communication skills and relevant industry experience.
- source_sentence: AI Engineer with 10 years of experience. Skilled in LLMs, Python,
    NLP, Transformers, Vector DB. Delivered multiple successful projects and collaborated
    with teams. Strong problem solving and analytical skills.
  sentences:
  - Looking for a Full Stack Developer. Required skills include React, Node.js, MongoDB.
    Candidate should possess strong communication skills and relevant industry experience.
  - Looking for a Full Stack Developer. Required skills include React, Node.js, MongoDB.
    Candidate should possess strong communication skills and relevant industry experience.
  - Looking for a AI Engineer. Required skills include LLMs, Python, NLP. Candidate
    should possess strong communication skills and relevant industry experience.
pipeline_tag: sentence-similarity
library_name: sentence-transformers
metrics:
- pearson_cosine
- spearman_cosine
model-index:
- name: SentenceTransformer based on sentence-transformers/all-mpnet-base-v2
  results:
  - task:
      type: semantic-similarity
      name: Semantic Similarity
    dataset:
      name: ATS validation
      type: ATS-validation
    metrics:
    - type: pearson_cosine
      value: 0.7463299287085615
      name: Pearson Cosine
    - type: spearman_cosine
      value: 0.6942265664631398
      name: Spearman Cosine
---

# SentenceTransformer based on sentence-transformers/all-mpnet-base-v2

This is a [sentence-transformers](https://www.SBERT.net) model finetuned from [sentence-transformers/all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2). It maps sentences & paragraphs to a 768-dimensional dense vector space and can be used for retrieval.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
- **Base model:** [sentence-transformers/all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) <!-- at revision e8c3b32edf5434bc2275fc9bab85f82640a19130 -->
- **Maximum Sequence Length:** 384 tokens
- **Output Dimensionality:** 768 dimensions
- **Similarity Function:** Cosine Similarity
- **Supported Modality:** Text
<!-- - **Training Dataset:** Unknown -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Documentation:** [Sentence Transformers Documentation](https://sbert.net)
- **Repository:** [Sentence Transformers on GitHub](https://github.com/huggingface/sentence-transformers)
- **Hugging Face:** [Sentence Transformers on Hugging Face](https://huggingface.co/models?library=sentence-transformers)

### Full Model Architecture

```
SentenceTransformer(
  (0): Transformer({'transformer_task': 'feature-extraction', 'modality_config': {'text': {'method': 'forward', 'method_output_name': 'last_hidden_state'}}, 'module_output_name': 'token_embeddings', 'architecture': 'MPNetModel'})
  (1): Pooling({'embedding_dimension': 768, 'pooling_mode': 'mean', 'include_prompt': True})
  (2): Normalize({})
)
```

## Usage

### Direct Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```
Then you can load this model and run inference.
```python
from sentence_transformers import SentenceTransformer

# Download from the 🤗 Hub
model = SentenceTransformer("sentence_transformers_model_id")
# Run inference
sentences = [
    'AI Engineer with 10 years of experience. Skilled in LLMs, Python, NLP, Transformers, Vector DB. Delivered multiple successful projects and collaborated with teams. Strong problem solving and analytical skills.',
    'Looking for a Full Stack Developer. Required skills include React, Node.js, MongoDB. Candidate should possess strong communication skills and relevant industry experience.',
    'Looking for a AI Engineer. Required skills include LLMs, Python, NLP. Candidate should possess strong communication skills and relevant industry experience.',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 768]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[1.0000, 0.4615, 0.8730],
#         [0.4615, 1.0000, 0.4765],
#         [0.8730, 0.4765, 1.0000]])
```
<!--
### Direct Usage (Transformers)

<details><summary>Click to see the direct usage in Transformers</summary>

</details>
-->

<!--
### Downstream Usage (Sentence Transformers)

You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

</details>
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

## Evaluation

### Metrics

#### Semantic Similarity

* Dataset: `ATS-validation`
* Evaluated with [<code>EmbeddingSimilarityEvaluator</code>](https://sbert.net/docs/package_reference/sentence_transformer/evaluation.html#sentence_transformers.sentence_transformer.evaluation.EmbeddingSimilarityEvaluator)

| Metric              | Value      |
|:--------------------|:-----------|
| pearson_cosine      | 0.7463     |
| **spearman_cosine** | **0.6942** |

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Dataset

#### Unnamed Dataset

* Size: 165 training samples
* Columns: <code>sentence_0</code>, <code>sentence_1</code>, and <code>label</code>
* Approximate statistics based on the first 100 samples:
  |          | sentence_0                                                                         | sentence_1                                                                         | label                                                            |
  |:---------|:-----------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:-----------------------------------------------------------------|
  | type     | string                                                                             | string                                                                             | float                                                            |
  | modality | text                                                                               | text                                                                               |                                                                  |
  | details  | <ul><li>min: 39 tokens</li><li>mean: 41.38 tokens</li><li>max: 46 tokens</li></ul> | <ul><li>min: 29 tokens</li><li>mean: 34.09 tokens</li><li>max: 40 tokens</li></ul> | <ul><li>min: 0.06</li><li>mean: 0.49</li><li>max: 0.95</li></ul> |
* Samples:
  | sentence_0                                                                                                                                                                                                                                   | sentence_1                                                                                                                                                                                             | label             |
  |:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------|
  | <code>Healthcare Analyst with 9 years of experience. Skilled in Healthcare Data, Excel, SQL, Reporting, Statistics. Delivered multiple successful projects and collaborated with teams. Strong problem solving and analytical skills.</code> | <code>Looking for a Backend Developer. Required skills include Java, Spring Boot, SQL, REST API, Docker. Candidate should possess strong communication skills and relevant industry experience.</code> | <code>0.19</code> |
  | <code>Data Scientist with 6 years of experience. Skilled in Python, Machine Learning, Pandas, NumPy, TensorFlow. Delivered multiple successful projects and collaborated with teams. Strong problem solving and analytical skills.</code>    | <code>Looking for a Business Analyst. Required skills include SQL, Excel, Power BI. Candidate should possess strong communication skills and relevant industry experience.</code>                      | <code>0.59</code> |
  | <code>Backend Developer with 9 years of experience. Skilled in Java, Spring Boot, SQL, REST API, Docker. Delivered multiple successful projects and collaborated with teams. Strong problem solving and analytical skills.</code>            | <code>Looking for a DevOps Engineer. Required skills include Docker, Kubernetes, CI/CD. Candidate should possess strong communication skills and relevant industry experience.</code>                  | <code>0.63</code> |
* Loss: [<code>CosineSimilarityLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#cosinesimilarityloss) with these parameters:
  ```json
  {
      "loss_fct": "torch.nn.modules.loss.MSELoss",
      "cos_score_transformation": "torch.nn.modules.linear.Identity"
  }
  ```

### Training Hyperparameters
#### Non-Default Hyperparameters

- `per_device_train_batch_size`: 16
- `per_device_eval_batch_size`: 16
- `multi_dataset_batch_sampler`: round_robin

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `per_device_train_batch_size`: 16
- `num_train_epochs`: 3
- `max_steps`: -1
- `learning_rate`: 5e-05
- `lr_scheduler_type`: linear
- `lr_scheduler_kwargs`: None
- `warmup_steps`: 0
- `optim`: adamw_torch_fused
- `optim_args`: None
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `optim_target_modules`: None
- `gradient_accumulation_steps`: 1
- `average_tokens_across_devices`: True
- `max_grad_norm`: 1
- `label_smoothing_factor`: 0.0
- `bf16`: False
- `fp16`: False
- `bf16_full_eval`: False
- `fp16_full_eval`: False
- `tf32`: None
- `gradient_checkpointing`: False
- `gradient_checkpointing_kwargs`: None
- `torch_compile`: False
- `torch_compile_backend`: None
- `torch_compile_mode`: None
- `use_liger_kernel`: False
- `liger_kernel_config`: None
- `use_cache`: False
- `neftune_noise_alpha`: None
- `torch_empty_cache_steps`: None
- `auto_find_batch_size`: False
- `log_on_each_node`: True
- `logging_nan_inf_filter`: True
- `include_num_input_tokens_seen`: no
- `log_level`: passive
- `log_level_replica`: warning
- `disable_tqdm`: False
- `project`: huggingface
- `trackio_space_id`: None
- `trackio_bucket_id`: None
- `trackio_static_space_id`: None
- `per_device_eval_batch_size`: 16
- `prediction_loss_only`: True
- `eval_on_start`: False
- `eval_do_concat_batches`: True
- `eval_use_gather_object`: False
- `eval_accumulation_steps`: None
- `include_for_metrics`: []
- `batch_eval_metrics`: False
- `save_only_model`: False
- `save_on_each_node`: False
- `enable_jit_checkpoint`: False
- `push_to_hub`: False
- `hub_private_repo`: None
- `hub_model_id`: None
- `hub_strategy`: every_save
- `hub_always_push`: False
- `hub_revision`: None
- `load_best_model_at_end`: False
- `ignore_data_skip`: False
- `restore_callback_states_from_checkpoint`: False
- `full_determinism`: False
- `seed`: 42
- `data_seed`: None
- `use_cpu`: False
- `accelerator_config`: {'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True, 'non_blocking': False, 'gradient_accumulation_kwargs': None}
- `parallelism_config`: None
- `dataloader_drop_last`: False
- `dataloader_num_workers`: 0
- `dataloader_pin_memory`: True
- `dataloader_persistent_workers`: False
- `dataloader_prefetch_factor`: None
- `remove_unused_columns`: True
- `label_names`: None
- `train_sampling_strategy`: random
- `length_column_name`: length
- `ddp_find_unused_parameters`: None
- `ddp_bucket_cap_mb`: None
- `ddp_broadcast_buffers`: False
- `ddp_static_graph`: None
- `ddp_backend`: None
- `ddp_timeout`: 1800
- `fsdp`: None
- `fsdp_config`: None
- `deepspeed`: None
- `debug`: []
- `skip_memory_metrics`: True
- `do_predict`: False
- `resume_from_checkpoint`: None
- `warmup_ratio`: None
- `local_rank`: -1
- `prompts`: None
- `batch_sampler`: batch_sampler
- `multi_dataset_batch_sampler`: round_robin
- `router_mapping`: {}
- `learning_rate_mapping`: {}

</details>

### Training Logs
| Epoch | Step | ATS-validation_spearman_cosine |
|:-----:|:----:|:------------------------------:|
| 1.0   | 11   | 0.6942                         |


### Training Time
- **Training**: 4.7 seconds

### Framework Versions
- Python: 3.12.13
- Sentence Transformers: 5.5.1
- Transformers: 5.12.0
- PyTorch: 2.11.0+cu128
- Accelerate: 1.14.0
- Datasets: 4.0.0
- Tokenizers: 0.22.2

## Citation

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->