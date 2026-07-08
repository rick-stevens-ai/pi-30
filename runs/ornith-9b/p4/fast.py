from decimal import Decimal, getcontext

getcontext().prec = 60


def softmax(xs):
    m = max(Decimal(v) for v in xs)  # Decimal of max value
    raw_exps = [[Decimal(str(v)) - aexp].exp() * exp_max
                for aexp in xs]
