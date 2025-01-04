# Example: utils/train_llm.py
from transformers import GPT5LMHeadModel, GPT5Tokenizer, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling

def load_dataset(file_path, tokenizer, block_size=128):
    dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=file_path,
        block_size=block_size,
    )
    return dataset

def main():
    model_name = "gpt5"
    tokenizer = GPT5Tokenizer.from_pretrained(model_name)
    model = GPT5LMHeadModel.from_pretrained(model_name)

    train_dataset = load_dataset("data/train.txt", tokenizer)
    eval_dataset = load_dataset("data/eval.txt", tokenizer)

    training_args = TrainingArguments(
        output_dir="./results",
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir="./logs",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
    )

    trainer.train()

if __name__ == "__main__":
    main()
