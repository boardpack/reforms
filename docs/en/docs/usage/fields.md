# Fields

## Built-in fields

Currently, reforms supports the next fields, which are expanded versions of 
well-known types.

#### `bool_field`
: 

* `widget: Type[BaseWidget] = Checkbox`: a widget class, which is responsible for the
 field rendering;
* `field_id: str = ""`: a field `id` in the layout;
* `field_class: str = ""`: a field `class` in the layout;
* `label: str = ""`: a label content in the layout;
* `disabled: bool = False"`: a disabled field option;
* `render_kw: Dict = None`: a dictionary to pass all other data that be needed in the 
field template;
* `validators: Optional[List[BaseValidator]] = None`: a list of validators that will
 be described in one of the next parts.

#### `str_field`
: 

* `widget: Type[BaseWidget] = TextInput`: a widget class, which is responsible for the
 field rendering;
* `field_id: str = ""`: a field `id` in the layout;
* `field_class: str = ""`: a field `class` in the layout;
* `label: str = ""`: a label content in the layout;
* `placeholder: str = ""`: a placeholder content in the layout;
* `disabled: bool = False"`: a disabled field option;
* `render_kw: Dict = None`: a dictionary to pass all other data that be needed in the 
field template;
* `validators: Optional[List[BaseValidator]] = None`: a list of validators that will
 be described in one of the next parts.

#### `email_field`
: implements the input string that must be a valid email address.

* `widget: Type[BaseWidget] = EmailInput`: a widget class, which is responsible for 
the field rendering;
* `field_id: str = ""`: a field `id` in the layout;
* `field_class: str = ""`: a field `class` in the layout;
* `label: str = ""`: a label content in the layout;
* `placeholder: str = ""`: a placeholder content in the layout;
* `disabled: bool = False"`: a disabled field option;
* `render_kw: Dict = None`: a dictionary to pass all other data that be needed in the 
field template;
* `validators: Optional[List[BaseValidator]] = None`: a list of validators that will
 be described in one of the next parts.

