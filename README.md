# Deid


## Models
 
LLaMA系列建议本地加载模型

1. LLaMA
   
   Convert model weights to HF format (HuggingFace): convert_llama_weights_to_hf.py

   非专业版本：
   ```python
   # Load model directly
    from transformers import AutoTokenizer, AutoModelForCausalLM

    tokenizer = AutoTokenizer.from_pretrained("openlm-research/open_llama_7b_v2")
    model = AutoModelForCausalLM.from_pretrained("openlm-research/open_llama_7b_v2")
    ```

2. LLaMA2
   (**meta-llama/Llama-2-7b**)

    Convert model weights to HF format (HuggingFace): convert_llama_weights_to_hf.py

3. Falcon-7b
   (**tiiuae/falcon-7b**)

   ```python
   # Load model directly
    from transformers import AutoModelForCausalLM
    model = AutoModelForCausalLM.from_pretrained("tiiuae/falcon-7b", trust_remote_code=True)
    ```

4. Flan-t5
   (**google/flan-t5-base**) 
   
   **There are multiple versions for flan-t5 models.**
   **flan-t5是AutoModelForSeq2SeqLM**
   **falcon-7b是AutoModelForCausalLM**

   ```python
   # Load model directly
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
    ```



## Dataset

### Original Dataset
**testing-PHI-Gold-fixed ** folerr contains xml files

### Finetune
1. sentences_nornal.csv
2. sentences_random.csv

extracted from testing-PHI-Gold-fixed folder

Total number of occurrences of the word 'he' in sentences_he_she.csv: 3456

Total number of occurrences of the word 'she' in sentences_he_she.csv: 2237

- Diiference

replaced with some wired/rare names 

Replaced with 300 normal names

## Paramaters

### HuggingFace Models

```python
# Load falcon-7b model
#
input_directory = './testing-PHI-Gold-fixed'
# model = "tiiuae/falcon-7b"
model = "google/flan-t5-base"
model_name_part = model.split("/")[-1]
output_path = "./rewrite_{}_implicit".format(model_name_part)
# 修改以上model和input_directory
```
### Local Models
```python
# Load Local model
#
input_directory = './testing-PHI-Gold-fixed'
model = "LLaMA1_7B"
# model = "LLaMA2_7B"
model_name_part = model
output_path = "./rewrite_{}_implicit".format(model_name_part)

# 修改以上model和input_directory
```