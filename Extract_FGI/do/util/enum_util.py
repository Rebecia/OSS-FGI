from enum import Enum


# Enumeration

class PackageManagerEnum(Enum):
    pypi = 'pypi'
    npmjs = 'npmjs'
    rubygems = 'rubygems'

    def __str__(self):
        return self.value


class LanguageEnum(Enum):
    python = 'python'
    javascript = 'javascript'
    ruby = 'ruby'
    java = 'java'
    csharp = 'csharp'
    php = 'php'
    docker = 'docker'
    vagrant = 'vagrant'

    def __str__(self):
        return self.value









