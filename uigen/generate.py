import os
import shutil
from collections import ChainMap
from os import PathLike
from pathlib import Path
from typing import Iterable, Optional, Union

from jinja2 import Environment, PackageLoader, TemplateNotFound, select_autoescape
from jinja2.loaders import split_template_path

from .models import Section

PathType = Union[str, PathLike[str]]


class PackageLoaderEx(PackageLoader):

    def copy_file(self, src: str, dest: Path) -> None:
        p = os.path.join(self._template_root, *split_template_path(src))
        if self._archive is None:
            if not os.path.isfile(p):
                raise TemplateNotFound(src)
            shutil.copy(p, dest)
            with open(p, "rb") as f:
                source = f.read()
        else:
            # Package is a zip file.
            try:
                with open(p, 'rb') as fd, dest.open('wb') as ofd:
                    buffer = fd.read()
                    while buffer:
                        ofd.write(buffer)
            except OSError as e:
                raise TemplateNotFound(src) from e


def rm_tree(path: Path, remove_top: bool = True):
    for child in path.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    if remove_top:
        path.rmdir()


class SourceGenerator:
    skeleton = ()

    def __init__(self, base_path: PathType, clear_dest: bool = False):
        self.base_path = Path(base_path)
        self.clear_dest = clear_dest
        self.loader = PackageLoaderEx("uigen")
        self.env = Environment(loader=self.loader, autoescape=select_autoescape())
        self.base_context: dict = {}

    def copy_file(self, source: str, dest: PathType):
        with self.ensure_path(dest) as dest_file:
            self.loader.copy_file(source, dest_file)

    def render_template(self, source: str, dest: PathType, context: Optional[dict] = None):
        template = self.env.get_template(source)
        with self.ensure_path(dest).open('w') as fd:
            fd.write(template.render(**ChainMap(context, self.base_context) if context else self.base_context))

    def ensure_path(self, dest: PathType) -> Path:
        path = (self.base_path / dest)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def read(self, items: Iterable[Section]):
        pass

    def generate(self):
        self.generate_skeleton()

    def __call__(self, items: Iterable[Section]):
        self.read(items)
        if self.clear_dest:
            rm_tree(self.base_path, False)
        self.generate()

    def generate_skeleton(self):
        for src, dest, *only_copy in self.skeleton:
            if only_copy:
                self.copy_file(src, dest)
            else:
                self.render_template(src, dest)


class FrontGenerator(SourceGenerator):
    skeleton = (
        ('vite.config.ts', 'vite.config.ts', True),
        ('public/favicon.ico', 'public/favicon.ico', True),
        ('index.html', 'index.html', True),
        ('tsconfig.json', 'tsconfig.json', True),
        ('package.json', 'package.json', True),
        ('src/components/HelloWorld.vue', 'src/components/HelloWorld.vue', True),
        ('src/env.d.ts', 'src/env.d.ts', True),
        ('src/App.vue', 'src/App.vue', True),
        ('src/main.ts', 'src/main.ts', True),
        ('src/assets/logo.png', 'src/assets/logo.png', True),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = []
        self.models = []
        self.routes = []
