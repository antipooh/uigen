from datetime import datetime
from decimal import Decimal
from typing import Any, Optional, Type

from models import Attr, AttrType, Model, StrAttr, IntAttr, DecimalAttr, DateTimeAttr
from type_util import is_optional_type

_type_map = {
    str: StrAttr,
    int: IntAttr,
    float: DecimalAttr,
    Decimal: DecimalAttr,
    datetime: DateTimeAttr
}


def annotation_to_attr_type(annotation) -> AttrType:
    tp = _type_map.get(annotation)
    return tp and tp()


def attr_from_annotation(name: str, annotation) -> Optional[Attr]:
    optional = False
    if is_optional_type(annotation):
        optional = True
        attr_type = annotation_to_attr_type(annotation.__args__[0])  # FIXME: work only with Optional
    else:
        attr_type = annotation_to_attr_type(annotation)
    if attr_type:
        return Attr(name=name, type=attr_type, optional=optional)


def class_to_model(cls: Type[Any],
                   name: Optional[str] = None) -> Model:
    model = Model(name=name or cls.__name__)
    annotations = getattr(cls, '__annotations__', {})
    for attr_name, annotation in annotations.items():
        attr = attr_from_annotation(attr_name, annotation)
        if attr:
            model.attrs.append(attr)
    return model
