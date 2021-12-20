from typing import ClassVar, List, TypeVar

from pydantic import BaseModel, root_validator


def ensure_title(_, values):
    if 'title' not in values:
        values['title'] = values['name'].title()
    return values


class Constraint(BaseModel):
    pass


class AttrClass(BaseModel):
    name: ClassVar[str]


AttrType = TypeVar('AttrType', bound=AttrClass)


class StrAttr(AttrClass):
    name = 'string'


class IntAttr(AttrClass):
    name = 'integer'


class DecimalAttr(AttrClass):
    name = 'decimal'


class DateTimeAttr(AttrClass):
    name = 'datetime'


class Attr(BaseModel):
    name: str
    type: AttrType
    constraints: List[Constraint] = []
    optional: bool


class Model(BaseModel):
    name: str
    attrs: List[Attr] = []
    constraints: List[Constraint] = []


class ModelForm(BaseModel):
    attrs: List[Attr] = []
    constraints: List[Constraint] = []


class View(BaseModel):
    name: ClassVar[str]


class ListModels(View):
    pass


class ViewModel(View):
    pass


class CreateModel(View):
    pass


class EditModel(View):
    pass


class DeleteModel(View):
    pass


class Section(BaseModel):
    name: str
    title: str
    views: List[View] = []

    _ensure_title = root_validator(pre=True, allow_reuse=True)(ensure_title)


class ModelSection(Section):
    model: Model
