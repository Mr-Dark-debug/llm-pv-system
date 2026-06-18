# Free and Free-Tier Model Selection for LEI/PVA Benchmark

Date checked: 2026-06-18

This note lists current free or free-tier model candidates for the phrasal-verb benchmark. Catalogs and rate limits change frequently, so refresh this list before a production data collection run.

## Sources Checked

- Google Gemini API models: https://ai.google.dev/gemini-api/docs/models
- Google Gemini API pricing/free tier: https://ai.google.dev/gemini-api/docs/pricing
- Google Gemini API rate limits: https://ai.google.dev/gemini-api/docs/rate-limits
- Groq supported models: https://console.groq.com/docs/models
- Groq rate limits/free plan: https://console.groq.com/docs/rate-limits
- OpenRouter models API: https://openrouter.ai/api/v1/models
- OpenRouter models API docs: https://openrouter.ai/docs/api/api-reference/models/get-models
- Hugging Face Inference Providers: https://huggingface.co/docs/inference-providers/en/index
- Ollama model library: https://ollama.com/library
- Together AI pricing: https://www.together.ai/pricing
- Fireworks AI pricing: https://fireworks.ai/pricing

## Recommended Benchmark Matrix

Use these first because they give a good spread of providers, model families, model sizes, and instruction-tuning styles while keeping cost low.

| Provider | Model ID | Access class | Why include |
|---|---|---:|---|
| Google Gemini API | `gemini-3.5-flash` | Free tier | Current stable Gemini Flash family model for strong general language behavior. |
| Google Gemini API | `gemini-3.1-flash-lite` | Free tier | Cheap/fast current Gemini model; useful for high-volume benchmark runs. |
| Google Gemini API | `gemini-2.5-flash` | Free tier | Established Gemini baseline with reasoning and multimodal support. |
| Google Gemini API | `gemini-2.5-flash-lite` | Free tier | Budget/latency control condition. |
| Google Gemini API | `gemini-2.5-pro` | Free tier where available | Higher-capability reasoning model for comparison with smaller models. |
| Groq | `llama-3.1-8b-instant` | Free plan limits | Fast small Llama baseline. |
| Groq | `llama-3.3-70b-versatile` | Free plan limits | Strong open Llama baseline. |
| Groq | `openai/gpt-oss-20b` | Free plan limits | Smaller open-weight GPT-OSS baseline. |
| Groq | `openai/gpt-oss-120b` | Free plan limits | Larger open-weight GPT-OSS baseline. |
| Groq | `qwen/qwen3-32b` | Free plan limits | Qwen family comparison. |
| OpenRouter | `openrouter/free` | Zero-priced route | Router-level free fallback for exploratory smoke runs. |
| OpenRouter | `meta-llama/llama-3.3-70b-instruct:free` | Zero-priced | Free Llama 70B instruct endpoint. |
| OpenRouter | `qwen/qwen3-coder:free` | Zero-priced | Large Qwen coding/instruction model, useful contrast. |
| OpenRouter | `qwen/qwen3-next-80b-a3b-instruct:free` | Zero-priced | Recent Qwen MoE-style instruct candidate. |
| OpenRouter | `openai/gpt-oss-20b:free` | Zero-priced | Open GPT-OSS comparison through router. |
| OpenRouter | `openai/gpt-oss-120b:free` | Zero-priced | Larger GPT-OSS comparison through router. |
| OpenRouter | `google/gemma-4-31b-it:free` | Zero-priced | Google open-model family comparison. |
| OpenRouter | `google/gemma-4-26b-a4b-it:free` | Zero-priced | Smaller Gemma 4 comparison. |
| OpenRouter | `nvidia/nemotron-3-super-120b-a12b:free` | Zero-priced | Large NVIDIA instruct/reasoning family comparison. |
| OpenRouter | `nvidia/nemotron-3-nano-30b-a3b:free` | Zero-priced | Smaller NVIDIA comparison. |
| Ollama local | `gemma4` | Local/free hardware | Local Google open-model baseline if hardware allows. |
| Ollama local | `qwen3.5` | Local/free hardware | Local Qwen baseline if hardware allows. |
| Ollama local | `llama3.3` or current Llama tag | Local/free hardware | Local Meta baseline if hardware allows. |

## Full OpenRouter Zero-Priced Text Model Pull

These were pulled from `https://openrouter.ai/api/v1/models` where prompt and completion price were both `0`.

| Model ID | Name | Context |
|---|---|---:|
| `cohere/north-mini-code:free` | Cohere: North Mini Code (free) | 256000 |
| `nex-agi/nex-n2-pro:free` | Nex AGI: Nex-N2-Pro (free) | 262144 |
| `nvidia/nemotron-3.5-content-safety:free` | NVIDIA: Nemotron 3.5 Content Safety (free) | 128000 |
| `nvidia/nemotron-3-ultra-550b-a55b:free` | NVIDIA: Nemotron 3 Ultra (free) | 1000000 |
| `openrouter/owl-alpha` | Owl Alpha | 1048756 |
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | NVIDIA: Nemotron 3 Nano Omni (free) | 256000 |
| `poolside/laguna-xs.2:free` | Poolside: Laguna XS.2 (free) | 262144 |
| `poolside/laguna-m.1:free` | Poolside: Laguna M.1 (free) | 262144 |
| `google/gemma-4-26b-a4b-it:free` | Google: Gemma 4 26B A4B (free) | 262144 |
| `google/gemma-4-31b-it:free` | Google: Gemma 4 31B (free) | 262144 |
| `google/lyria-3-pro-preview` | Google: Lyria 3 Pro Preview | 1048576 |
| `google/lyria-3-clip-preview` | Google: Lyria 3 Clip Preview | 1048576 |
| `nvidia/nemotron-3-super-120b-a12b:free` | NVIDIA: Nemotron 3 Super (free) | 1000000 |
| `openrouter/free` | Free Models Router | 200000 |
| `liquid/lfm-2.5-1.2b-thinking:free` | LiquidAI: LFM2.5-1.2B-Thinking (free) | 32768 |
| `liquid/lfm-2.5-1.2b-instruct:free` | LiquidAI: LFM2.5-1.2B-Instruct (free) | 32768 |
| `nvidia/nemotron-3-nano-30b-a3b:free` | NVIDIA: Nemotron 3 Nano 30B A3B (free) | 256000 |
| `nvidia/nemotron-nano-12b-v2-vl:free` | NVIDIA: Nemotron Nano 12B 2 VL (free) | 128000 |
| `qwen/qwen3-next-80b-a3b-instruct:free` | Qwen: Qwen3 Next 80B A3B Instruct (free) | 262144 |
| `nvidia/nemotron-nano-9b-v2:free` | NVIDIA: Nemotron Nano 9B V2 (free) | 128000 |
| `openai/gpt-oss-120b:free` | OpenAI: gpt-oss-120b (free) | 131072 |
| `openai/gpt-oss-20b:free` | OpenAI: gpt-oss-20b (free) | 131072 |
| `qwen/qwen3-coder:free` | Qwen: Qwen3 Coder 480B A35B (free) | 1048576 |
| `cognitivecomputations/dolphin-mistral-24b-venice-edition:free` | Venice: Uncensored (free) | 32768 |
| `meta-llama/llama-3.3-70b-instruct:free` | Meta: Llama 3.3 70B Instruct (free) | 131072 |
| `meta-llama/llama-3.2-3b-instruct:free` | Meta: Llama 3.2 3B Instruct (free) | 131072 |
| `nousresearch/hermes-3-llama-3.1-405b:free` | Nous: Hermes 3 405B Instruct (free) | 131072 |

## Notes

- OpenRouter zero-priced models are excellent for exploratory runs, but availability and throughput can change. Store the exact model ID and response status for every benchmark run.
- Groq exposes a model list endpoint, but it requires `GROQ_API_KEY`. The public docs list production and preview models plus free-plan rate limits.
- Google Gemini free-tier usage may be used to improve Google products, while paid tier terms differ. Treat that as important if benchmark prompts or outputs become sensitive.
- Ollama is free in cash terms but limited by local hardware and model quantization. It is still valuable as a reproducible local baseline.
- Hugging Face Inference Providers, Together AI, and Fireworks are useful for extra open-model coverage, but they are better described as free-credit/free-tier rather than guaranteed zero-cost for a full 90-prompt x 3-run benchmark.
