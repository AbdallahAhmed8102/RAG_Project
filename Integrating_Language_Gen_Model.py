from transformers import pipeline
from clearml import Task
import torch


task = Task.init(project_name="RAG_Project", 
                 task_name="distilGPT-2 Text Generation", 
                 task_type=Task.TaskTypes.optimizer,  
                 reuse_last_task_id=False)

hyperparameters = {
    'temperature': 1.0,
    'max_length': 1024,
    'no_repeat_ngram_size': 3
}
task.connect(hyperparameters)

generator = pipeline("text-generation", model="distilgpt2", device=0, temperature=hyperparameters['temperature'], no_repeat_ngram_size=hyperparameters['no_repeat_ngram_size'])

query = "What is robotics documentation?"
retrieved_docs = ["Document 1 content...", "Document 2 content...", "Document 3 content..."]
context = " ".join(retrieved_docs)

prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer: Provide a concise and informative answer."

response = generator(prompt, max_length=hyperparameters['max_length'])

generated_text = response[0]["generated_text"]
print("Generated Response:")
print(generated_text)

task.upload_artifact(name="Generated Response", artifact_object=generated_text)

task.get_logger().report_text("Generated Response", generated_text)


task.close()
