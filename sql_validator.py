import re

def validate_sql(sql):
    """Ensures the SQL is a safe, read-only SELECT statement."""
    if not sql:
        return False, "Empty query"
        
    sql_upper = sql.upper().strip()
    
    if not sql_upper.startswith("SELECT"):
        return False, "Only SELECT queries are allowed."
        
    forbidden = [
        "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", 
        "CREATE", "REPLACE", "GRANT", "REVOKE", "EXEC", "CALL"
    ]
    
    for keyword in forbidden:
        if re.search(rf"\b{keyword}\b", sql_upper):
            return False, f"Unauthorized keyword found: {keyword}. Modifying queries are blocked."
            
    if "BUSINESS_DATA" not in sql_upper:
        return False, "Query must target the business_data table."
        
    return True, "Valid"