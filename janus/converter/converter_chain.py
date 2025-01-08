from janus.converter.converter import Converter


class ConverterChain(Converter):
    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            raise ValueError("Error: Converter chain must be passed at least 1 converter")
        for converter in args:
            if not isinstance(converter, Converter):
                raise ValueError(f"Error: unrecognized type: {type(converter)}")
        self._converters = args
        super().__init__(**kwargs)

    def get_chain(self, start: bool = False):
        chain = self._converters[0].get_chain(start)
        for converter in self._converters[1:]:
            chain = chain | converter.get_chain(False)
        return chain
