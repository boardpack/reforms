# Fields

## Built-in fields

Currently, reforms supports the next fields, which are expanded versions of 
well-known types.

#### `bool_field`
: 

* `field_id: str = ""`: a field `id` in the layout
* `field_class: str = ""`: a field `class` in the layout
* `label: str = ""`: a label content in the layout
* `render_kw: Dict = None`: a dictionary to pass all other data that be needed in the 
field template.
* `validators: Optional[List[BaseValidator]] = None`: a list of validators that will
 be described in one of the next parts.

#### `str_field`
: 

* `field_id: str = ""`: a field `id` in the layout
* `field_class: str = ""`: a field `class` in the layout
* `label: str = ""`: a label content in the layout
* `placeholder: str = ""`: a placeholder content in the layout
* `render_kw: Dict = None`: a dictionary to pass all other data that be needed in the 
field template.
* `validators: Optional[List[BaseValidator]] = None`: a list of validators that will
 be described in one of the next parts.

#### `email_field`
: implements the input string that must be a valid email address.

* `field_id: str = ""`: a field `id` in the layout
* `field_class: str = ""`: a field `class` in the layout
* `label: str = ""`: a label content in the layout
* `placeholder: str = ""`: a placeholder content in the layout
* `render_kw: Dict = None`: a dictionary to pass all other data that be needed in the 
field template.
* `validators: Optional[List[BaseValidator]] = None`: a list of validators that will
 be described in one of the next parts.

