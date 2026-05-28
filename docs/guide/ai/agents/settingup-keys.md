# Setting up API Keys for AI Agent Evaluations

When you run the *full* evaluation suite (without the `--fast` flag), you may encounter an error like this:

```text
deepeval.errors.DeepEvalError: OpenAI API key is empty. Please configure a valid key.
```

This guide explains why this happens and how to fix it as a beginner.

## 1. Why do I need an API Key?

Our project uses **DeepEval** and **Ragas** to evaluate the quality of our AI agents. Instead of simply checking if the output has the right JSON fields (which is what `--fast` does), the full evaluation suite grades the *behavior* of the agents.

To calculate metrics like **Answer Relevancy** and **Faithfulness**, DeepEval and Ragas actually need to use an LLM "under the hood" as an impartial judge. This means the evaluation script needs to be able to make LLM API requests.

## 2. Where to put your keys

Your keys belong in your backend's environment variables. 

1. Navigate to the backend directory: `cd backend`
2. Create or open the file named `.env`
3. Add your keys using one of the approaches below.

---

### Option A: Using standard OpenAI (Easiest)

If you have an OpenAI account with available credits, you can simply provide your standard OpenAI API key. Both DeepEval and Ragas default to using OpenAI if configured.

Add this line to your `backend/.env` file:

```env
OPENAI_API_KEY="sk-your-openai-api-key-here"
```

---

### Option B: Using Local LLM / OpenRouter Proxy (Project Default)

Our project supports a Local LLM proxy using **LiteLLM** (see `infrastructure/LOCAL-LLM.md`). If you are running the `scripts/start-server-mac.sh` local server, you can tell the evaluation frameworks to route their requests through your local proxy instead of paying for OpenAI directly.

Add the following to your `backend/.env` file:

```env
# Tell the frameworks to use your local LiteLLM proxy instead of the real OpenAI servers
OPENAI_API_KEY="dummy-key-not-needed"
OPENAI_API_BASE="http://localhost:4000/v1" # Or whatever port your LiteLLM proxy is running on

# If your local proxy routes to OpenRouter for gpt-oss-120b, ensure that is set:
OPENROUTER_API_KEY="sk-or-v1-your-openrouter-key"
LITELLM_API_BASE="http://localhost:4000"
```

## 3. Running the Full Evaluation

Once your `.env` file is saved with the correct keys, you can run the full evaluation suite from the project root!

```bash
uv run --project backend python -m backend.admin.run_evals --all
```

*(Tip: Full evaluations make multiple LLM requests per test case. To save time or credits, try testing just one agent first using `--agent ranking` instead of `--all`)*
