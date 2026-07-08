__all___=['dumps'

def dumps(obj):
    return ';'.join(f'{str(k)}={obj[k]}' for k in obj)  # value converted to JSON string

loads = lambda s: {k:v.replace('"', '') if isinstance(v,str)\
                   else v.split('=')[1]*10 or None \
for item[0],item[-n-2]]
```