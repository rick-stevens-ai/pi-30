class KVBackend:
    def dumps(self, obj: dict) -> str:
        """Dumps a flat dictionary {str: str} into the KV string format 'k1=v1;k2=v2'."""
        parts = []
        for k, v in obj.items():
            # Assuming keys and values are strings as per the requirement description
            parts.append(f"{k}={v}")
        return ";".join(parts)

    def loads(self, s: str) -> dict:
        """Loads a KV string 'k1=v1;k2=v2' back into a flat dictionary."""
        if not s:
            return {}
        
        result = {}
        pairs = s.split(';')
        for pair in pairs:
            if '=' in pair:
                try:
                    key, value = pair.split('=', 1)
                    result[key.strip()] = value.strip()
                except ValueError:
                    # Handle malformed pair if necessary, but for this exercise, we assume valid format
                    pass
        return result

# In a real setup, this class would likely be instantiated or used by the main backend system.
# For simplicity, we expose these methods directly as requested.