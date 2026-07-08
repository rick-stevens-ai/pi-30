# P13 SEED: only parses a bare integer. No recursion, no other types.
# DO NOT use the json module (the point is to write a parser).

import re

# Token types
TOKEN_EOF = 'EOF'
TOKEN_NULL = 'NULL'
TOKEN_TRUE = 'TRUE'
TOKEN_FALSE = 'FALSE'
TOKEN_NUMBER = 'NUMBER'
TOKEN_STRING = 'STRING'
TOKEN_LBRACKET = 'LBRACKET'
TOKEN_RBRACKET = 'RBRACKET'
TOKEN_LBRACE = 'LBRACE'
TOKEN_RBRACE = 'RBRACE'
TOKEN_COMMA = 'COMMA'
TOKEN_COLON = 'COLON'

# Token regex patterns
TOKEN_PATTERNS = [
    (TOKEN_NULL, r'null'),
    (TOKEN_TRUE, r'true'),
    (TOKEN_FALSE, r'false'),
    (TOKEN_NUMBER, r'-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?'),
    (TOKEN_STRING, r'"(?:[^"\\]|\\.)*"'),
    (TOKEN_LBRACKET, r'\['),
    (TOKEN_RBRACKET, r'\]'),
    (TOKEN_LBRACE, r'\{'),
    (TOKEN_RBRACE, r'\}'),
    (TOKEN_COMMA, r','),
    (TOKEN_COLON, r':'),
    (None, r'\s+'),  # whitespace - skip
]

# Compile master regex
MASTER_RE = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_PATTERNS if name))


class Token:
    __slots__ = ('type', 'value', 'pos')
    def __init__(self, type, value, pos):
        self.type = type
        self.value = value
        self.pos = pos
    def __repr__(self):
        return f'Token({self.type}, {self.value!r})'


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.tokens = []
        self.current = 0
        self._tokenize()
    
    def _tokenize(self):
        for match in MASTER_RE.finditer(self.text):
            type_name = match.lastgroup
            if type_name is not None:
                value = match.group(type_name)
                self.tokens.append(Token(type_name, value, match.start()))
        self.tokens.append(Token(TOKEN_EOF, None, len(self.text)))
    
    def peek(self):
        return self.tokens[self.current]
    
    def advance(self):
        token = self.tokens[self.current]
        self.current += 1
        return token
    
    def expect(self, token_type):
        token = self.peek()
        if token.type != token_type:
            raise ValueError(f'Expected {token_type}, got {token.type} at position {token.pos}')
        return self.advance()


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
    
    def parse(self):
        result = self.parse_value()
        self.lexer.expect(TOKEN_EOF)
        return result
    
    def parse_value(self):
        token = self.lexer.peek()
        
        if token.type == TOKEN_NULL:
            self.lexer.advance()
            return None
        elif token.type == TOKEN_TRUE:
            self.lexer.advance()
            return True
        elif token.type == TOKEN_FALSE:
            self.lexer.advance()
            return False
        elif token.type == TOKEN_NUMBER:
            return self.parse_number()
        elif token.type == TOKEN_STRING:
            return self.parse_string()
        elif token.type == TOKEN_LBRACKET:
            return self.parse_array()
        elif token.type == TOKEN_LBRACE:
            return self.parse_object()
        else:
            raise ValueError(f'Unexpected token {token.type} at position {token.pos}')
    
    def parse_number(self):
        token = self.lexer.advance()
        value = token.value
        # Try to parse as int first, then float
        if '.' in value or 'e' in value or 'E' in value:
            return float(value)
        return int(value)
    
    def parse_string(self):
        token = self.lexer.advance()
        # Remove surrounding quotes and process escape sequences
        s = token.value[1:-1]
        return self._unescape_string(s)
    
    def _unescape_string(self, s):
        # Handle JSON escape sequences
        result = []
        i = 0
        while i < len(s):
            if s[i] == '\\':
                i += 1
                if i >= len(s):
                    raise ValueError('Incomplete escape sequence')
                c = s[i]
                if c == '"':
                    result.append('"')
                elif c == '\\':
                    result.append('\\')
                elif c == '/':
                    result.append('/')
                elif c == 'b':
                    result.append('\b')
                elif c == 'f':
                    result.append('\f')
                elif c == 'n':
                    result.append('\n')
                elif c == 'r':
                    result.append('\r')
                elif c == 't':
                    result.append('\t')
                elif c == 'u':
                    # Unicode escape - simplified to just handle 4 hex digits
                    if i + 4 >= len(s):
                        raise ValueError('Incomplete unicode escape')
                    hex_digits = s[i+1:i+5]
                    result.append(chr(int(hex_digits, 16)))
                    i += 4
                else:
                    raise ValueError(f'Invalid escape sequence: \\{c}')
            else:
                result.append(s[i])
            i += 1
        return ''.join(result)
    
    def parse_array(self):
        self.lexer.expect(TOKEN_LBRACKET)
        elements = []
        
        if self.lexer.peek().type == TOKEN_RBRACKET:
            self.lexer.advance()
            return elements
        
        while True:
            elements.append(self.parse_value())
            token = self.lexer.peek()
            if token.type == TOKEN_COMMA:
                self.lexer.advance()
                continue
            elif token.type == TOKEN_RBRACKET:
                self.lexer.advance()
                break
            else:
                raise ValueError(f'Expected comma or ] at position {token.pos}')
        
        return elements
    
    def parse_object(self):
        self.lexer.expect(TOKEN_LBRACE)
        obj = {}
        
        if self.lexer.peek().type == TOKEN_RBRACE:
            self.lexer.advance()
            return obj
        
        while True:
            # Parse key (must be string)
            key_token = self.lexer.peek()
            if key_token.type != TOKEN_STRING:
                raise ValueError(f'Expected string key at position {key_token.pos}')
            key = self.parse_string()
            
            # Expect colon
            self.lexer.expect(TOKEN_COLON)
            
            # Parse value
            value = self.parse_value()
            obj[key] = value
            
            token = self.lexer.peek()
            if token.type == TOKEN_COMMA:
                self.lexer.advance()
                continue
            elif token.type == TOKEN_RBRACE:
                self.lexer.advance()
                break
            else:
                raise ValueError(f'Expected comma or }} at position {token.pos}')
        
        return obj


def parse(s):
    """Parse a JSON string and return the corresponding Python object."""
    lexer = Lexer(s.strip())
    parser = Parser(lexer)
    return parser.parse()
