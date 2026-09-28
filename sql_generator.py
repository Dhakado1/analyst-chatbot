import os
import json
import re
import ast

from dotenv import load_dotenv
from google import genai

from prompts import SQL_GENERATION_PROMPT, DATABASE_SCHEMA

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)

MODELS = [
    "gemini-flash-lite-latest",
    "gemini-flash-latest",
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash"
]


def clean_response(text):
    """
    Convert Gemini response into a Python dictionary.
    Handles JSON, markdown JSON, Python dict and direct SQL.
    """

    text = text.strip()

    print("\n========== RAW GEMINI RESPONSE ==========")
    print(text)
    print("=========================================\n")

    # Remove markdown code blocks
    text = re.sub(r"```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```\s*", "", text)
    text = text.strip()

    # Try normal JSON
    try:
        return json.loads(text)
    except Exception:
        pass

    # Try extracting JSON object from surrounding text
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        json_text = match.group(0)

        try:
            return json.loads(json_text)
        except Exception:
            pass

        # Try Python dictionary format
        try:
            return ast.literal_eval(json_text)
        except Exception:
            pass

    # If Gemini directly returned SQL
    sql_match = re.search(
        r"(SELECT\s+.*?)(?:;|\Z)",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if sql_match:
        sql = sql_match.group(1).strip()

        if "business_data" in sql.lower():
            return {
                "sql": sql,
                "context": {}
            }

    return None


def generate_sql(user_message, current_context):

    prompt = SQL_GENERATION_PROMPT.format(
        schema=DATABASE_SCHEMA,
        question=user_message,
        context=json.dumps(current_context)
    )

    for model in MODELS:

        try:

            print("\n========================================")
            print("Trying model:", model)
            print("========================================")

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            if not response or not response.text:
                print("Empty Gemini response.")
                continue

            result = clean_response(response.text)

            if result:

                # Make sure SQL exists
                if result.get("sql"):

                    print("\n========== FINAL SQL ==========")
                    print(result["sql"])
                    print("===============================\n")

                    return {
                        "sql": result["sql"],
                        "context": result.get(
                            "context",
                            current_context
                        )
                    }

                # Clarification response
                if result.get("clarification_needed"):

                    return {
                        "clarification_needed":
                            result["clarification_needed"]
                    }

            print("Could not extract SQL from response.")

        except Exception as e:

            print("\nModel failed:", model)
            print("Error:", e)
            print("Trying next model...\n")

            continue

    print("\n========== SQL GENERATION FAILED ==========")
    print("No model produced usable SQL.")
    print("===========================================\n")

    return {
        "sql": None,
        "context": current_context
    }