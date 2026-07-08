class CSVBackend:
    """
    CSV backend implementation according to PLAN.md specification.
    obj: {'fields': [...]} <-> 'a,b,c'
    """
    def dumps(self, obj: dict) -> str:
        """
        Serializes an object with the structure {'fields': [...]}.
        Example: {'fields': ['a', 'b', 'c']} -> 'a,b,c'
        """
        if not isinstance(obj, dict) or 'fields' not in obj:
            raise TypeError("Input object must be a dictionary with a 'fields' key.")
        
        fields = obj['fields']
        return ",".join(map(str, fields))

    def loads(self, s: str) -> dict:
        """
        Deserializes a comma-separated string back into the object structure.
        Example: 'a,b,c' -> {'fields': ['a', 'b', 'c']}
        """
        if not isinstance(s, str):
            raise TypeError("Input must be a string.")
            
        fields = s.split(',')
        return {'fields': fields}

# In a real application, this class would likely be registered or used by the main backend logic.
# For demonstration purposes, we expose these methods directly if needed, 
# but typically a framework handles dispatching based on configuration.
# We assume the context requires defining this structure for the CSV backend implementation.