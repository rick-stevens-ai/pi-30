def parse(text):
    return {"fields": [field.strip() for field in text.split(",")]}
