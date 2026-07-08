from work.csv.backend import parse

def test():
    assert parse("a,b,c") == {"fields": ["a", "b", "c"]}
    assert parse("") == {"fields": []}
    assert parse("a") == {"fields": ["a"]}
    print("Tests passed!")

if __name__ == "__main__":
    test()
