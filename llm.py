import os
import json
from dotenv import load_dotenv
from google import genai

from sql_generator import generate_sql
from sql_validator import validate_sql
from database import execute_query
from prompts import RESPONSE_PROMPT

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)


def process_user_query(user_message, current_context):

    try:

        # 1. Generate SQL and update context
        sql_generation_result = generate_sql(
            user_message,
            current_context
        )

        if "clarification_needed" in sql_generation_result:

            return (
                sql_generation_result["clarification_needed"],
                current_context,
                None
            )

        generated_sql = sql_generation_result.get("sql")

        new_context = sql_generation_result.get(
            "context",
            current_context
        )

        if not generated_sql:

            return (
                "I couldn't understand the question well enough.",
                new_context,
                None
            )

        # 2. Validate SQL
        is_valid, validation_msg = validate_sql(generated_sql)

        if not is_valid:

            return (
                f"Security Error: {validation_msg}",
                new_context,
                generated_sql
            )

        # 3. Execute SQL
        query_result = execute_query(generated_sql)

        if "error" in query_result:

            return (
                f"Database error: {query_result['error']}",
                new_context,
                generated_sql
            )

        # 4. Generate natural language response
        data_results = query_result["results"]

        prompt = RESPONSE_PROMPT.format(
            question=user_message,
            context=json.dumps(new_context),
            sql=generated_sql,
            results=json.dumps(
                data_results,
                default=str
            )
        )

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        return (
            response.text,
            new_context,
            generated_sql
        )

    except Exception as e:

        import traceback

        print("\n========== CHAT ERROR ==========")
        traceback.print_exc()
        print("================================\n")

        return (
            f"Error processing request: {str(e)}",
            current_context,
            None
        )