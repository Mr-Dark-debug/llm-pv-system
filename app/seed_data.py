"""Protocol seed data for models, prompts, and phrasal verbs."""

from datetime import date

from app.models import LLMModel, Prompt


PHAVE_MASTER_LIST: dict[str, str] = {
    "look_up": "literal",
    "give_up": "figurative",
    "pick_up": "semi_transparent",
    "turn_on": "literal",
    "turn_off": "literal",
    "find_out": "semi_transparent",
    "come_up": "semi_transparent",
    "go_on": "semi_transparent",
    "carry_out": "semi_transparent",
    "set_up": "semi_transparent",
    "take_off": "literal",
    "put_on": "literal",
    "bring_up": "figurative",
    "stand_out": "figurative",
    "break_down": "semi_transparent",
    "work_out": "semi_transparent",
    "run_into": "semi_transparent",
    "look_into": "semi_transparent",
    "hold_on": "semi_transparent",
    "keep_up": "semi_transparent",
    "cut_down": "semi_transparent",
    "make_up": "figurative",
    "point_out": "semi_transparent",
    "go_over": "semi_transparent",
    "get_along": "figurative",
    "get_over": "figurative",
    "put_off": "figurative",
    "call_off": "semi_transparent",
    "look_after": "semi_transparent",
    "come_across": "figurative",
}


def seed_models() -> list[LLMModel]:
    """Return default LLM registry rows.

    Args:
        None.

    Returns:
        list[LLMModel]: Sixteen active model records.

    Raises:
        None.
    """

    rows = [
        ("gemini-3.5-flash", "google", "Gemini 3.5 Flash", None, date(2025, 1, 1), True),
        ("gemini-3.1-flash-lite", "google", "Gemini 3.1 Flash-Lite", None, date(2025, 1, 1), True),
        ("gemini-2.5-flash", "google", "Gemini 2.5 Flash", None, date(2025, 1, 1), True),
        ("gemini-2.5-flash-lite", "google", "Gemini 2.5 Flash-Lite", None, date(2025, 1, 1), True),
        ("gemini-2.5-pro", "google", "Gemini 2.5 Pro", None, date(2025, 1, 1), True),
        ("llama-3.1-8b-instant", "groq", "Groq Llama 3.1 8B Instant", 8.0, date(2023, 12, 1), True),
        ("llama-3.3-70b-versatile", "groq", "Groq Llama 3.3 70B Versatile", 70.0, date(2023, 12, 1), True),
        ("openai/gpt-oss-20b", "groq", "Groq GPT-OSS 20B", 20.0, date(2024, 6, 1), True),
        ("openai/gpt-oss-120b", "groq", "Groq GPT-OSS 120B", 120.0, date(2024, 6, 1), True),
        ("qwen/qwen3-32b", "groq", "Groq Qwen3 32B", 32.0, date(2024, 12, 1), True),
        ("openrouter/free", "openrouter", "OpenRouter Free Models Router", None, date(2026, 1, 1), True),
        ("meta-llama/llama-3.3-70b-instruct:free", "openrouter", "OpenRouter Llama 3.3 70B Free", 70.0, date(2023, 12, 1), True),
        ("qwen/qwen3-coder:free", "openrouter", "OpenRouter Qwen3 Coder Free", None, date(2025, 1, 1), True),
        ("qwen/qwen3-next-80b-a3b-instruct:free", "openrouter", "OpenRouter Qwen3 Next 80B Free", 80.0, date(2025, 1, 1), True),
        ("openai/gpt-oss-20b:free", "openrouter", "OpenRouter GPT-OSS 20B Free", 20.0, date(2024, 6, 1), True),
        ("openai/gpt-oss-120b:free", "openrouter", "OpenRouter GPT-OSS 120B Free", 120.0, date(2024, 6, 1), True),
        ("google/gemma-4-31b-it:free", "openrouter", "OpenRouter Gemma 4 31B Free", 31.0, date(2025, 1, 1), True),
        ("google/gemma-4-26b-a4b-it:free", "openrouter", "OpenRouter Gemma 4 26B Free", 26.0, date(2025, 1, 1), True),
        ("nvidia/nemotron-3-super-120b-a12b:free", "openrouter", "OpenRouter Nemotron 3 Super Free", 120.0, date(2025, 1, 1), True),
        ("nvidia/nemotron-3-nano-30b-a3b:free", "openrouter", "OpenRouter Nemotron 3 Nano Free", 30.0, date(2025, 1, 1), True),
        ("gemma4", "ollama", "Ollama Gemma 4", None, date(2025, 1, 1), True),
        ("qwen3.5", "ollama", "Ollama Qwen 3.5", None, date(2025, 1, 1), True),
        ("llama3.3", "ollama", "Ollama Llama 3.3", 70.0, date(2023, 12, 1), True),
        ("gpt-4o", "openai", "GPT-4o Reference", None, date(2023, 10, 1), False),
        ("claude-3-5-sonnet", "anthropic", "Claude 3.5 Sonnet Reference", None, date(2024, 4, 1), False),
    ]
    return [
        LLMModel(
            model_id=model_id,
            provider=provider,
            display_name=display,
            parameter_count_billion=params,
            training_cutoff=cutoff,
            rlhf_tuned=rlhf,
            pvr_overall=0.0,
        )
        for model_id, provider, display, params, cutoff, rlhf in rows
    ]


def seed_prompts() -> list[Prompt]:
    """Return the 90-prompt benchmark seed set.

    Args:
        None.

    Returns:
        list[Prompt]: Prompt rows P001 through P090.

    Raises:
        None.
    """

    context_free = [
        "Write a short neutral paragraph about solving a common workplace problem.",
        "Describe a student learning a difficult English expression.",
        "Explain how someone handles a delayed train journey.",
        "Write advice for organizing a shared apartment.",
        "Describe a person repairing a bicycle before school.",
        "Write a short story about a missed phone call.",
        "Explain how to prepare for a group presentation.",
        "Describe a family planning a weekend trip.",
        "Write instructions for reducing screen time.",
        "Describe a friend helping with exam stress.",
    ]
    context_rich = [
        "A learner wants natural but clear English for an email to a professor. Write the email.",
        "Two flatmates disagree about cleaning duties. Write a realistic dialogue.",
        "A manager explains a postponed deadline to a team. Write the message.",
        "A student describes how they recovered from a failed test. Write their reflection.",
        "A tourist asks for help after losing a wallet. Write the interaction.",
        "A teacher explains a confusing grammar point with examples. Write the explanation.",
        "A volunteer coordinator assigns tasks before an event. Write the briefing.",
        "A job applicant explains a gap in their CV. Write the answer.",
        "A friend gives supportive advice after a breakup. Write the advice.",
        "A researcher summarizes unexpected survey findings. Write the summary.",
    ]
    target_pvs = list(PHAVE_MASTER_LIST.keys())
    prompts: list[Prompt] = []
    for index in range(30):
        template = context_free[index % len(context_free)]
        prompts.append(Prompt(prompt_id=f"P{index + 1:03d}", prompt_type="context_free", prompt_text=f"{template} Version {index + 1}.", expected_register="neutral"))
    for index in range(30):
        template = context_rich[index % len(context_rich)]
        prompts.append(Prompt(prompt_id=f"P{index + 31:03d}", prompt_type="context_rich", prompt_text=f"{template} Include concrete details. Version {index + 1}.", expected_register="neutral"))
    for index in range(30):
        target = target_pvs[index % len(target_pvs)]
        prompts.append(
            Prompt(
                prompt_id=f"P{index + 61:03d}",
                prompt_type="metalinguistic",
                prompt_text=f"Explain the phrasal verb '{target.replace('_', ' ')}' and use it in two learner-friendly sentences.",
                target_pv=target,
                expected_register="informal" if index % 2 else "neutral",
            )
        )
    return prompts
