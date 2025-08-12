from __future__ import annotations

import json
import os
import re
from functools import lru_cache
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline  # type: ignore
except Exception:  # pragma: no cover
    AutoModelForCausalLM = None  # type: ignore
    AutoTokenizer = None  # type: ignore
    pipeline = None  # type: ignore


DEFAULT_MODEL = "google/gemma-2-2b-it"


def _extract_json_block(text: str) -> Optional[Dict[str, Any]]:
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
    if AutoModelForCausalLM is None or AutoTokenizer is None or pipeline is None:
        return None
    resolved_model = (os.getenv("HF_PLACES_MODEL", "").strip() or model_name).strip()
    hf_token = os.getenv("HUGGINGFACE_API_TOKEN", "").strip() or os.getenv("HF_TOKEN", "").strip() or None
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


def get_popular_attractions(goal_or_place: str, top_k: int = 8, model: str = DEFAULT_MODEL) -> List[Dict[str, Any]]:
    """Generate popular attractions using a local Transformers pipeline (Gemma-2 2B IT)."""
    try:
        load_dotenv()
    except Exception:
        pass

    text_gen = _get_text_generation_pipeline(model)
    if text_gen is None:
        return []

    system_hint = (
        "You are a concise travel attractions recommender. Always return STRICT JSON and nothing else."
    )

    user_task = (
        f"Task: From the following user text, infer the target CITY or COUNTRY and list the top {top_k} "
        "popular attractions (landmarks, museums, historical places, parks). If the text is a country, distribute results across its most visited cities.\n"
        f"User text: \"{goal_or_place}\"\n\n"
        "Output format (STRICT JSON, no extra text):\n"
        "{\n  \"attractions\": [\n    {\"name\": \"...\", \"kind\": \"landmark|museum|park|neighborhood|gallery|other\", \"city\": \"...\", \"neighborhood\": \"...\", \"short_reason\": \"...\"}\n  ]\n}\n\n"
        "Rules:\n- Prefer globally recognized places.\n- Keep reasons short (one sentence).\n- If unsure about city/neighborhood, omit those fields or leave empty.\n\n"
        "Example (for the city of Rome):\n"
        "{\n  \"attractions\": [\n"
        "    {\"name\": \"Colosseum\", \"kind\": \"landmark\", \"city\": \"Rome\", \"neighborhood\": \"Centro Storico\", \"short_reason\": \"Iconic ancient amphitheater and must-see site.\"},\n"
        "    {\"name\": \"Vatican Museums\", \"kind\": \"museum\", \"city\": \"Vatican City\", \"neighborhood\": \"\", \"short_reason\": \"World-class art collections including the Sistine Chapel.\"}\n"
        "  ]\n}\n"
    )

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
        raw_text = _gen_once(user_task, 360)
    except Exception:
        raw_text = ""

    data = _extract_json_block(raw_text) or {}
    items = data.get("attractions", [])
    if not items:
        retry_task = (
            user_task
            + "\n\nReturn ONLY valid JSON. Do not include explanations or markdown. Do not repeat the prompt.\n"
            + "Begin JSON now and close it properly."
        )
        try:
            raw_text_retry = _gen_once(retry_task, 280)
        except Exception:
            raw_text_retry = ""
        data = _extract_json_block(raw_text_retry) or {}
        items = data.get("attractions", [])

    results: List[Dict[str, Any]] = []
    for it in items[:top_k]:
        results.append(
            {
                "name": it.get("name", ""),
                "kind": it.get("kind", ""),
                "city": it.get("city", ""),
                "neighborhood": it.get("neighborhood", ""),
                "short_reason": it.get("short_reason", ""),
            }
        )

    if not results and (os.getenv("DEBUG_HF_AGENTS", "").strip()):
        try:
            print("[HF_PLACES_AGENT] First pass output:\n", raw_text[:800])
        except Exception:
            pass

    # Enhanced RAG fallback with better city detection
    if not results:
        try:
            from rag.retriever import retrieve_pois, _detect_city_from_text
            
            # Use enhanced city detection
            city_hint = _detect_city_from_text(goal_or_place)
            
            # Get attractions from RAG
            attraction_pois = retrieve_pois(
                goal=goal_or_place, 
                profile_card="tarih, kültür, sanat, müze, landmark", 
                city_hint=city_hint, 
                top_k=top_k * 2  # Get more to filter
            )
            
            # Convert to expected format with better categorization
            for poi in attraction_pois:
                category = str(poi.get("category", "")).lower()
                kind = "other"
                
                # Better category mapping
                if category in {"museum", "gallery"}:
                    kind = "museum" if category == "museum" else "gallery"
                elif category in {"park", "garden"}:
                    kind = "park"
                elif category in {"landmark", "monument"}:
                    kind = "landmark"
                elif category in {"neighborhood", "district"}:
                    kind = "neighborhood"
                elif category in {"food-street", "restaurant"}:
                    kind = "neighborhood"  # Food streets as neighborhood attractions
                
                # Skip if it's clearly not an attraction
                if kind == "other" and category not in ["landmark", "museum", "park", "neighborhood"]:
                    continue
                
                results.append({
                    "name": poi.get("name", ""),
                    "kind": kind,
                    "city": poi.get("city", ""),
                    "neighborhood": poi.get("neighborhood", ""),
                    "short_reason": poi.get("summary", "") or "Popüler turistik nokta.",
                })
                
                if len(results) >= top_k:
                    break
            
            # If still no results, add any remaining POIs
            if not results:
                for poi in attraction_pois[:top_k]:
                    results.append({
                        "name": poi.get("name", ""),
                        "kind": "other",
                        "city": poi.get("city", ""),
                        "neighborhood": poi.get("neighborhood", ""),
                        "short_reason": poi.get("summary", "") or "Şehirde görülmeye değer yer.",
                    })
                    
        except Exception as e:
            if os.getenv("DEBUG_HF_AGENTS", "").strip():
                print(f"[HF_PLACES_AGENT] RAG fallback error: {e}")

    return results


