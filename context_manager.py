def update_context(old_context, new_context):
    """Merges old context with new context intelligently."""
    updated = old_context.copy()
    for key, value in new_context.items():
        if value is not None:
            updated[key] = value
    return updated