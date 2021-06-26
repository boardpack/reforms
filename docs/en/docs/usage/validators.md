# Validators

## Introduction

As Reforms expands Pydantic, then you can use all existed features including 
[validators](https://pydantic-docs.helpmanual.io/usage/validators/). Here you can 
see a simple example, for more information please go to the appropriate page of the
pydantic documentation.

```Python
{!../../../docs_src/validators/tutorial001.py!}
```
_(This script is complete, it should run "as is")_

## Built-in validators

If you used [wtforms](https://wtforms.readthedocs.io/en/2.3.x/validators/) before, 
you have definitely used their built-in validators and implemented yours owns in 
cases, when you needed some custom behavior. Reforms also contains a similar 
validators list. Here is a simple example.

```Python
{!../../../docs_src/validators/tutorial002.py!}
```
_(This script is complete, it should run "as is")_

All current built-in validators you can see below.

#### `Length`
: validates the length of a string.

* `min: int =- 1`: The minimum required length of the string. If not provided, minimum length 
will not be checked.
* `max: int =- 1`: The maximum length of the string. If not provided, maximum length will not 
be checked. 
* `message: str = ""`: Error message to raise in case of a validation error. Can be interpolated 
using {min} and {max} if desired. Useful defaults are provided depending on the 
existence of min and max.

#### `AnyOf`
: compares the incoming data to a sequence of valid inputs.

* `values: Sequence[Any]`: A sequence of valid inputs.
* `message: str = "Invalid value, must be one of: {values}."`: Error message to 
raise in case of a validation error. {values} contains the list of values.
* `values_formatter: Callable = None`: Function used to format the list of values in
 the error message.

#### `NoneOf`
: compares the incoming data to a sequence of invalid inputs.

* `values: Sequence[Any]`: A sequence of valid inputs.
* `message: str = "Invalid value, must be one of: {values}."`: Error message to 
raise in case of a validation error. {values} contains the list of values.
* `values_formatter: Callable = None`: Function used to format the list of values in
 the error message.

## Write your custom validator

To write custom validator, you need to create a callable object (function or class 
with implemented `__call__` method) with the parameters below.


!!! warning
    Validators should either return the parsed value or raise a `ValueError`, 
    `TypeError`, or `AssertionError` (`assert` statements may be used). It's the 
    same as with <a href="https://pydantic-docs.helpmanual.io/usage/validators/" class="external-link" target="_blank">default pydantic validators</a>.


| Parameter | Type                                                                                       | Description                                 |
|-----------|--------------------------------------------------------------------------------------------|---------------------------------------------|
| value     | Any                                                                                        | Current field value                               |
| field (Optional)     | [ModelField](https://github.com/samuelcolvin/pydantic/blob/master/pydantic/fields.py#L309){:target="_blank"} | Parameter to get access to the field itself |

```Python
{!../../../docs_src/validators/tutorial003.py!}
```
_(This script is complete, it should run "as is")_
