from expression import effect, Some

@effect.option[int]()
def fn():
    x = yield 42
    y = yield from Some(43)

    return x + y

xs = fn()
print(xs)