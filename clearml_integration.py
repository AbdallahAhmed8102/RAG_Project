from clearml import Task
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def run_clearml_integration():
    task = Task.init(project_name="RAG_Project", 
                     task_name="distilGPT-2 Experiment", 
                     task_type=Task.TaskTypes.optimizer,  
                     reuse_last_task_id=False)
    
    hyperparameters = {
        'learning_rate': 0.001,
        'batch_size': 16,
        'max_length': 5000,
        'num_epochs': 5
    }
    
    
    task.connect(hyperparameters)

    
    model_name = 'distilgpt2'  
    model = AutoModelForCausalLM.from_pretrained(model_name).cuda()  
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    
    input_text = "What is robotics documentation?"
    inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
    
    
    for epoch in range(hyperparameters['num_epochs']):
        outputs = model(**inputs, labels=inputs["input_ids"])
        loss = outputs.loss
        
        
        task.get_logger().report_scalar("Loss", "train", iteration=epoch, value=loss.item())
        
        
        if epoch % 2 == 0:  
            checkpoint_path = f'./model_checkpoint_epoch_{epoch}'
            model.save_pretrained(checkpoint_path)
            task.upload_artifact(f"model_checkpoint_epoch_{epoch}", artifact_object=checkpoint_path)
    
    
    task.close()

if __name__ == "__main__":
    run_clearml_integration()
