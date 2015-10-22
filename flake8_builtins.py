import ast
import tokenize

from sys import stdin

__version__ = '1.0'

BUILTINS_ERROR_CODE = 'T002'
BUILTINS_ERROR_MESSAGE = 'override of Python builtin found'
BUILTINS = ('ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BufferError', 'BytesWarning',
            'DeprecationWarning', 'EOFError', 'Ellipsis', 'EnvironmentError', 'Exception', 'False',
            'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning',
            'IndentationError', 'IndexError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError',
            'NameError', 'None', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError',
            'PendingDeprecationWarning', 'ReferenceError', 'RuntimeError', 'RuntimeWarning', 'StandardError',
            'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'True',
            'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError',
            'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'ZeroDivisionError',
            '__debug__', '__import__', '__name__', '__package__', 'abs', 'all', 'any', 'apply', 'basestring',
            'bin', 'bool', 'buffer', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'cmp', 'coerce', 'compile',
            'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'execfile',
            'exit', 'file', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash',
            'hex', 'id', 'input', 'int', 'intern', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list',
            'locals', 'long', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print',
            'property', 'quit', 'range', 'raw_input', 'reduce', 'reload', 'repr', 'reversed', 'round', 'set', 'setattr',
            'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'unichr', 'unicode', 'vars',
            'xrange', 'zip')


class BuiltinsOverrideChecker(object):
    name = 'flake8-builtins'
    version = __version__
    ignores = ()

    def __init__(self, tree, filename='(none)', builtins=None):
        self.tree = tree
        self.filename = (filename == 'stdin' and stdin) or filename

    @classmethod
    def add_options(cls, parser):
        parser.add_option('--builtins-exclude', default=None, action='store', type='str',
                          help='Comma-separated list of builtin overrides to exclude')
        parser.config_options.append('builtins-exclude')

    @classmethod
    def parse_options(cls, options):
        if options.builtins_exclude is not None:
            cls.ignores = options.builtins_exclude.split(',')

    def run(self):
        # Get lines to ignore
        if self.filename == stdin:
            noqa = _get_noqa_lines(self.filename)
        else:
            with open(self.filename, 'r') as file_to_check:
                noqa = _get_noqa_lines(file_to_check.readlines())

        # Run the actual check
        errors = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign) and hasattr(node, 'targets') and node.lineno not in noqa:
                for target in node.targets:
                    if hasattr(target, 'id') and target.id in BUILTINS and target.id not in self.ignores:
                        errors.append({
                            "message": '{0} {1}: {2}'.format(BUILTINS_ERROR_CODE, BUILTINS_ERROR_MESSAGE, target.id),
                            "line": node.lineno,
                            "col": node.col_offset
                        })

        # Yield the found errors
        for error in errors:
            yield (error.get("line"), error.get("col"), error.get("message"), type(self))


def _get_noqa_lines(code):
    tokens = tokenize.generate_tokens(lambda L=iter(code): next(L))
    return [token[2][0] for token in tokens if token[0] == tokenize.COMMENT and
            (token[1].endswith('noqa') or (isinstance(token[0], str) and token[0].endswith('noqa')))]
