## Elections Programs AI

### Run the app locally

Requirements:

- Python 3.12
- Poetry

1. Create a `.env` file copied from `.env.example` and fill the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` Aws credentials.


2. Run

    ```bash
    make run
    ```
    or if you prefer the most annoying way:

    ```bash
    poetry install
    AWS_ACCESS_KEY_ID=your_id  AWS_SECRET_ACCESS_KEY=your_secret API_USERNAME=elections-programs API_PASSWORD=an_api_password poetry run uvicorn src.webapp.main:app --reload
    ```

### Run the tests with

```bash
make test
```

### Do you want to switch to another generative model provider? 
Replace the env vars and the LangChain Chat class used by ai_assistant.py to (example with Huggingface):

`huggingface_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not huggingface_token:
   raise ValueError("HUGGINGFACEHUB_API_TOKEN environment variable is not set.")`

`llm_endpoint = HuggingFaceEndpoint(
     repo_id="mistralai/Mistral-7B-Instruct-v0.3",
     temperature=0.7,
     max_new_tokens=256,
     stop_sequences=["</s>", "Human:", "AI:"],
 )
 llm = ChatHuggingFace(llm=llm_endpoint)`