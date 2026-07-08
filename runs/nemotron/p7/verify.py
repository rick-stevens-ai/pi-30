# P7 acceptance verifier — DO NOT let the agent edit this file.
from dispatch import dispatch

def main():
    assert dispatch("csv", "a,b,c") == {"fields": ["a", "b", "c"]}, "csv"
    assert dispatch("kv", "k1=v1;k2=v2") == {"k1": "v1", "k2": "v2"}, "kv"
    assert dispatch("json", '{"x": 1, "y": [2, 3]}') == {"x": 1, "y": [2, 3]}, "json"
    # round of edge cases
    assert dispatch("csv", "solo") == {"fields": ["solo"]}, "csv solo"
    assert dispatch("kv", "a=1") == {"a": "1"}, "kv single"
    print("OK P7")

if __name__ == "__main__":
    main()
