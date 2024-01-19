import os


class Path:
    base = os.path.dirname(__file__)

    ui_prefix = os.path.join(base, "ui")
    # image_prefix = os.path.join(base, "image")
    icon_prefix = os.path.join(base, "icon")
    # data_prefix = os.path.join(base, "images")

    # File loaders.
    @classmethod
    def ui(cls, filename):
        return os.path.join(cls.ui_prefix, filename)

    @classmethod
    def icon(cls, filename):
        return os.path.join(cls.icon_prefix, filename)

    # @classmethod
    # def image(cls, filename):
    #     return os.path.join(cls.image_prefix, filename)

    # @classmethod
    # def data(cls, filename):
    #     return os.path.join(cls.data_prefix, filename)
