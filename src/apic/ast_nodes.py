from dataclasses import dataclass
from typing import Union
from .tokens import TokenType

# --- expressions ---
@dataclass
class Literal:
    value: Union[int, float, str, bool, None]
@dataclass
class Identifier:
    name: str
@dataclass
class Unary:
    operator:TokenType
    operand: object
@dataclass       
class Binary:
    left: object
    operator:TokenType
    right: object 
@dataclass       
class Call:
    callee: str
    arguments: list  
@dataclass       
class Index:
    target: object
    index_Ex: object 
@dataclass       
class ArrayLiteral:
     elements: list           
# --- statements ---
@dataclass
class VarDecl:
    name: str
    initializer: object
    is_const: bool
@dataclass
class Assign:
    target: object   # an Identifier or an Index node
    value: object 
@dataclass
class ExprStmt:
    expression: object
@dataclass
class Block:
    statements: list
@dataclass
class If:
    condition: object
    then_block: object
    elseifs: list          # list of (condition, block) tuples
    else_block: object     # a Block, or None
@dataclass
class Increment:
    target: object       # an Identifier
    operator: TokenType  # TokenType.PLUS_PLUS or TokenType.MINUS_MINUS
@dataclass
class Loop:
    initializer: object   # an Assign node (i = 0)
    condition: object     # an expression (i < 10)
    increment: object     # an Increment node (i++)
    body: object            # a Block
@dataclass
class Function:
    name: str
    params: list      # list of strings
    body: object       # a Block    
@dataclass
class Return:
    value: object   # an expression node, or None
@dataclass
class Program:
    statements: list                               