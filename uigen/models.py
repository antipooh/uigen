from typing import ClassVar, List, Optional, TypeVar

from pydantic import BaseModel


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


class Section:

    def __init__(self, name: str, title: Optional[str] = None):
        self.name = name
        self.title = title or name.title()
        self.views: List[View] = []


class ModelSection(Section):

    def __init__(self, model: Model, **kwargs):
        self.model = model
        kwargs['name'] = kwargs.get('name') or model.name
        super().__init__(**kwargs)
