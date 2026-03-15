# Uses the ESM-2 model to generate embeddings for sequences

from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
import wandb

# download model weights from huggingface
def load_model():
    model_name = "facebook/esm2_t12_35M_UR50D"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    model.eval()

def embed_sequence(sequence):
    # tokenize — converts amino acid string to token IDs
    inputs = tokenizer(sequence, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    # outputs.last_hidden_state shape: (1, seq_len, hidden_dim)
    # Mean pool over sequence length → (hidden_dim,) vector
    embedding = outputs.last_hidden_state[0, 1:-1, :].mean(dim=0)
    return embedding.numpy()

if __name__ == "__main__":
    load_model()
    # Use it
    sequence = "MAEPRQEFEVMEDHAGTYGLGDRK"  # Tau fragment
    embedding = embed_sequence(sequence)
    print(embedding.shape)  # (480,) for esm2_t12

