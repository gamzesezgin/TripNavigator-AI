from __future__ import annotations

import json
import os
import re
from functools import lru_cache
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

try:  # Optional at import-time; installed via requirements
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline  # type: ignore
except Exception:  # pragma: no cover - allows importing module without transformers
    AutoModelForCausalLM = None  # type: ignore
    AutoTokenizer = None  # type: ignore
    pipeline = None  # type: ignore


DEFAULT_MODEL = "google/gemma-2-2b-it"


def _extract_json_block(text: str) -> Optional[Dict[str, Any]]:
    """Best-effort JSON extraction. Supports fenced code blocks and plain JSON."""
    if not text:
        return None
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", text, re.IGNORECASE)
    candidates: List[str] = []
    if fence:
        candidates.append(fence.group(1).strip())
    candidates.append(text)

    for cand in candidates:
        try:
            if cand.strip().startswith("{"):
                return json.loads(cand)
            match_obj = re.search(r"\{[\s\S]*\}", cand)
            if match_obj:
                return json.loads(match_obj.group(0))
        except Exception:
            continue
    return None


@lru_cache(maxsize=1)
def _get_text_generation_pipeline(model_name: str) -> Any:
    """Load and cache a local text-generation pipeline for Gemma. Returns None if unavailable."""
    if AutoModelForCausalLM is None or AutoTokenizer is None or pipeline is None:
        return None
    resolved_model = (os.getenv("HF_FOOD_MODEL", "").strip() or model_name).strip()
    hf_token = os.getenv("HUGGINGFACE_API_TOKEN", "").strip() or os.getenv("HF_TOKEN", "").strip() or None
    # Lazy import torch to avoid hard dependency at import time
    try:
        import torch  # type: ignore
    except Exception:
        torch = None  # type: ignore

    model_kwargs: Dict[str, Any] = {"trust_remote_code": True, "low_cpu_mem_usage": True}
    device_map: str | None = None
    if torch is not None:
        try:
            if torch.cuda.is_available():  # type: ignore[attr-defined]
                device_map = "auto"
                model_kwargs["torch_dtype"] = getattr(torch, "bfloat16", None) or getattr(torch, "float16", None)
            else:
                device_map = "cpu"
        except Exception:
            device_map = None

    tokenizer = AutoTokenizer.from_pretrained(
        resolved_model,
        token=hf_token,
        trust_remote_code=model_kwargs.get("trust_remote_code", False),
        use_fast=True,
    )
    model = AutoModelForCausalLM.from_pretrained(
        resolved_model,
        token=hf_token,
        **{k: v for k, v in model_kwargs.items() if k != "trust_remote_code"}
    )
    text_gen = pipeline(
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        device_map=device_map or None,
    )
    return text_gen


def get_popular_food_places(goal_or_city: str, top_k: int = 6, model: str = DEFAULT_MODEL) -> List[Dict[str, Any]]:
    """Generate popular restaurants using a local Transformers pipeline (Gemma-2 2B IT)."""
    try:
        load_dotenv()
    except Exception:
        pass

    text_gen = _get_text_generation_pipeline(model)
    if text_gen is None:
        return []

    system_hint = (
        "You are a concise travel food recommender. Always return STRICT JSON and nothing else."
    )

    user_task = (
        f"Task: From the following user goal text, infer the target city and list the top {top_k} "
        "popular food places (restaurants, food streets, bistros) in that city.\n"
        f"User goal: \"{goal_or_city}\"\n\n"
        "Output format (STRICT JSON, no extra text):\n"
        "{\n  \"restaurants\": [\n    {\"name\": \"...\", \"cuisine\": \"...\", \"neighborhood\": \"...\", \"short_reason\": \"...\"}\n  ]\n}\n\n"
        "Rules:\n- Prefer famous and crowd-pleasing places, avoid niche.\n"
        "- Keep reasons short (one sentence).\n- If unsure about neighborhood, omit that field or leave empty.\n\n"
        "Example (for the city of Paris):\n"
        "{\n  \"restaurants\": [\n"
        "    {\"name\": \"Le Comptoir du Relais\", \"cuisine\": \"French bistro\", \"neighborhood\": \"Saint-Germain\", \"short_reason\": \"Classic Parisian bistro with beloved dishes.\"},\n"
        "    {\"name\": \"L\u2019As du Fallafel\", \"cuisine\": \"Middle Eastern\", \"neighborhood\": \"Le Marais\", \"short_reason\": \"Iconic falafel spot with long lines and lively vibe.\"}\n"
        "  ]\n}\n"
    )

    # Prefer Gemma chat template if available
    def _gen_once(strict_user_task: str, max_tokens: int) -> str:
        if hasattr(text_gen, "tokenizer") and hasattr(text_gen.tokenizer, "apply_chat_template"):
            chat_formatted = text_gen.tokenizer.apply_chat_template(
                [
                    {"role": "system", "content": system_hint},
                    {"role": "user", "content": strict_user_task},
                ],
                tokenize=False,
                add_generation_prompt=True,
            )
            model_input = chat_formatted
        else:
            model_input = f"{system_hint}\n\n{strict_user_task}"

        eos_id = None
        try:
            eos_id = getattr(text_gen.tokenizer, "eos_token_id", None)
        except Exception:
            eos_id = None
        outputs = text_gen(
            model_input,
            max_new_tokens=max_tokens,
            do_sample=False,
            temperature=0.2,
            return_full_text=False,
            eos_token_id=eos_id,
        )
        return outputs[0]["generated_text"] if isinstance(outputs, list) else str(outputs)

    try:
        raw_text = _gen_once(user_task, 320)
    except Exception:
        raw_text = ""

    data = _extract_json_block(raw_text) or {}
    items = data.get("restaurants", [])
    if not items:
        # Retry with a stricter instruction and a minimal JSON stub to nudge formatting
        retry_task = (
            user_task
            + "\n\nReturn ONLY valid JSON. Do not include explanations or markdown. Do not repeat the prompt.\n"
            + "Begin JSON now and close it properly."
        )
        try:
            raw_text_retry = _gen_once(retry_task, 256)
        except Exception:
            raw_text_retry = ""
        data = _extract_json_block(raw_text_retry) or {}
        items = data.get("restaurants", [])

    results: List[Dict[str, Any]] = []
    for it in items[:top_k]:
        results.append(
            {
                "name": it.get("name", ""),
                "cuisine": it.get("cuisine", ""),
                "neighborhood": it.get("neighborhood", ""),
                "short_reason": it.get("short_reason", ""),
            }
        )

    # Optional debug: print first chars if empty
    if not results and (os.getenv("DEBUG_HF_AGENTS", "").strip()):
        try:
            print("[HF_FOOD_AGENT] First pass output:\n", raw_text[:800])
        except Exception:
            pass
    
    # Fallback to RAG if model output is empty
    if not results:
        try:
            from rag.retriever import retrieve_pois
            
            # Extract city from goal
            city_hint = None
            goal_lower = goal_or_city.lower()
            if "istanbul" in goal_lower or "istanbul'da" in goal_lower:
                city_hint = "Istanbul"
            elif "paris" in goal_lower or "pariş" in goal_lower:
                city_hint = "Paris"
            elif "rome" in goal_lower or "roma" in goal_lower:
                city_hint = "Rome"
            elif "tokyo" in goal_lower:
                city_hint = "Tokyo"
            elif "new york" in goal_lower or "nyc" in goal_lower:
                city_hint = "New York"
            
            # Get food-related POIs from RAG
            food_pois = retrieve_pois(
                goal=goal_or_city, 
                profile_card="food, gastronomi, yemek, restoran", 
                city_hint=city_hint, 
                top_k=top_k
            )
            
            # Filter for food-related categories and convert to expected format
            for poi in food_pois:
                if poi.get("category") in ["food-street", "restaurant"] or "food" in str(poi.get("tags", [])):
                    results.append({
                        "name": poi.get("name", ""),
                        "cuisine": poi.get("category", "").replace("food-street", "Street Food"),
                        "neighborhood": poi.get("neighborhood", ""),
                        "short_reason": poi.get("summary", "") or "Popüler yemek mekanı.",
                    })
                    if len(results) >= top_k:
                        break
            
            # If still no results, add any POI with food-related tags
            if not results:
                for poi in food_pois:
                    if any(tag in str(poi.get("tags", [])).lower() for tag in ["food", "yemek", "restoran"]):
                        results.append({
                            "name": poi.get("name", ""),
                            "cuisine": "Local Cuisine",
                            "neighborhood": poi.get("neighborhood", ""),
                            "short_reason": poi.get("summary", "") or "Yerel lezzetler.",
                        })
                        if len(results) >= top_k:
                            break
                            
        except Exception as e:
            if os.getenv("DEBUG_HF_AGENTS", "").strip():
                print(f"[HF_FOOD_AGENT] RAG fallback error: {e}")
    
    return results