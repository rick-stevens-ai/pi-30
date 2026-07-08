from decimal import Decimal as Cd
print('Cd name', Cd.__name__)
print('Cd base class', Cd.__bases__)
print('has __sub__?', hasattr(Cd, '__sub__'))
print('method: ', Cd.__sub__.__code__.co_freevars if hasattr(Cd.__sub__, '__code__') else None)
