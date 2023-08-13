# Deid


# Models
 
1. LLaMA
   
   Convert model weights to HF format (HuggingFace): convert_llama_weights_to_hf.py

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

   ```python
   # Load model directly
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
    ```

