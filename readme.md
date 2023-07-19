# Result

This is a python implementation of the Result monad.

The result monad is a specific variant of the Either monad, in this case the
two sides of the either monad is being called Ok and Err, in this special case
the Err side will always return itself when any functor is called on itself.

Bind, Map, Return and Apply are implemented for these.

Return is simply the default constructor:
```python
a = Ok("a")
to_b = Ok(lambda _: "B")
a = Ok(a) # This will just be an Ok("a")
err_a = Err(a) # This will change Ok("a") to Err("a")
a = Ok(err_a) # This will raise an exception, an Err cannot be convert to an Ok
```

Bind will take a function that returns a Result and apply it to the value in the result:
```python
a = Ok("a")
add_b = lambda x: Ok(x+"b")
a = a.bind(add_b)
a.value == "ab" # True
```

Apply will take a function wrapped in a Result and apply it to the value in the result:
```python
a = Ok("a")
to_b = Ok(lambda _: "B")
a = a.apply(to_b)
a.value == "b" # True
```

Map will take a function and apply it to the value in the result:
```python
a = Ok("a")
to_b = lambda _: "B"
a = a.map(to_b)
a.value == "b" # True
```

# Corner cases

The type checker seems to not catch some corner cases even though they will cause an
error at runtime

```python
a = Ok("a")
add_b = Ok(lambda _: "b")
add_c = Ok(lambda _: "c")
add_b = add_b.apply(add_c)
a.apply(add_b) # Throws an error at runtime but the type checker wont show any error in your IDE
```