import sys
import ply.lex as lex

states = (
   ('formula','inclusive'),
   ('allowleftright','inclusive'),
   ('color', 'inclusive'),
)


reserved = {
        "theory": 'KWDTHEORY',
        "begin": 'KWDBEGIN',
        "end": 'KWDEND',
        "functions": 'KWDFUNCTIONS',
        "private": 'KWDPRIVATE',
        "destructor": 'KWDDESTRUCTOR',
        "equations": 'KWDEQUATIONS',
        "builtins": 'KWDBUILTINS',
        "diffie-hellman": 'KWDDIFFIEHELLMAN',
        "symmetric-encryption": 'KWDSYMMETRICENCRYPTION',
        "hashing": 'KWDHASHING',
        "asymmetric-encryption": 'KWDASYMMETRICENCRYPTION',
        "signing": 'KWDSIGNING',
        "bilinear-pairing": 'KWDBILINEARPAIRING',
        "xor": 'KWDXOR',
        "multiset": 'KWDMULTISET',
        "revealing-signing": 'KWDREVEALINGSIGNING',
        "heuristic": 'KWDHEURISTIC',
        "rule": 'KWDRULE',
        "variants": 'KWDVARIANTS',
        "modulo": 'KWDMODULO',
        "let": 'KWDLET',
        "in": 'KWDIN',
        "restriction": 'KWDRESTRICTION',
        "restrictions": 'KWDRESTRICTIONS',
        "lemma": 'KWDLEMMA',
        "diffLemma": 'KWDDIFFLEMMA',
        "sources": 'KWDSOURCES',
        "reuse": 'KWDREUSE',
        "use_induction": 'KWDUSEINDUCTION',
        "all-traces": 'KWDALLTRACES',
        "exists-trace": 'KWDEXISTSTRACE',
        "SOLVED": 'KWDSOLVED',
        "by": 'KWDBY',
        "case": 'KWDCASE',
        "qed": 'KWDQED',
        "sorry": 'KWDSORRY',
        "simplify": 'KWDSIMPLIFY',
        "solve": 'KWDSOLVE',
        "contradiction": 'KWDCONTRADICTION',
        "induction": 'KWDINDUCTION',
        "splitEqs": 'KWDSPLITEQS',
        "node": 'KWDNODE',
        "no_precomp": 'KWDNOPRECOMP',
        "not": 'KWDNOT',
        "last": 'KWDLAST',
        "Ex": 'KWDEXISTS',
        "All": 'KWDFORALL',
        "XOR": 'OPXOR',
        'next': 'KWDNEXT',
        'predicate': 'KWDPREDICATE',
        'tactic': 'KWDTACTIC',
        'presort': 'KWDPRESORT',
        'prio': 'KWDPRIO',
        'deprio': 'KWDDEPRIO',
        'axiom': 'KWDAXIOM',
        'diffLemma': 'KWDDIFFLEMMA',
        'rule-equivalence': 'KWDRULEEQ',
        'backward-search': 'KWDBACKWARDSEARCH',
        'step': 'KWDSTEP',
        'MIRRORED': 'KWDMIRRORED',
        'ATTACK': 'KWDATTACK',
        'UNFINISHABLEdiff': 'KWDUNFINISHABLEDIFF',
        'test': 'KWDTEST',
        'account': 'KWDACCOUNT',
        'accounts': 'KWDACCOUNTS',
        'for': 'KWDFOR'
}

tokens = [
    'HEURISTICORACLE',
    'COLON',
    'COMMA',
    'SLASH',
    'EQUAL',
    'DOUBLEQUOTE',
    'LBRACKET',
    'RBRACKET',
    'FORWARDARROW', # -->
    'LACTIONFACTARROW', # --[
    'RACTIONFACTARROW', # ]->
    'LPAREN',
    'RPAREN',
    'HEXCOLOR',
    'QUOTED_HEXCOLOR',
    'HASH_QUOTED_HEXCOLOR',
    'AROBA',
    'HASH',
    'DOT',
    'LFORMALCOMMENT',
    'RFORMALCOMMENT',
    'LOWER',
    'HIGHER',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'EXPONENTIAL',
    'LBRACE',
    'RBRACE',
    'QUOTE',
    'TILDE',
    'DOLLAR',
    'BANG',
    'EQUIVALENT',
    'UNIEQUIVALENT',
    'IMPLY',
    'UNIIMPLY',
    'DISJUNCTION',
    'UNIDISJUNCTION',
    'CONJUNCTION',
    'UNICONJUNCTION',
    'UNINOT',
    'UNIFALSE',
    'UNITRUE',
    'UNIEXISTS',
    'UNIFORALL',
    'GOALTRIANGLE',
    'GOALARROW',
    'FORMULASEP',
    'XORSYMBOL',
    'IDENTDOTNATURAL',
    'REGEX_STRING',
    'ISFACTNAME_STRING',
    'ISINFACTTERMS_STRING',
    'DHRENOISE_STRING',
    'DEFAULTNOISE_STRING',
    'REASONABLENONCESNOISE_STRING',
    'NONABSURDGOAL_STRING',
    'KWDHIDELEMMAEQUAL',
    'KWDHEURISTICEQUAL',
    'SECTION',
    'MACRO_INCLUDE',
    'MACRO_IFDEF',
    'MACRO_ELSE',
    'MACRO_ENDIF',
    'MACRO_DEFINE',
    'COLOREQUAL',
    'COLOUREQUAL',
    'DUMMY',
    'FORGOTTEN_COMMENT',
    'LITERAL',
    'KWDLEFT',
    'KWDRIGHT',

    'NATURAL',
    'IDENT',
    'LITTLE0',
    'LITTLE1',
    'LITTLE2',
    'LITTLE3',
    'LITTLE4',
    'LITTLE5',
    'LITTLE6',
    'LITTLE7',
    'LITTLE8',
    'LITTLE9',
] + list(reserved.values())

keywords = {v:k for (k,v) in reserved.items()}


def t_COMMENT_LINE(t):
    r'//.*'
    pass

def t_COMMENT_MULTILINE(t):
    r'/\*'
    start_comment = t.lexer.lexpos-2
    pushed_inner_comments = 1
    while pushed_inner_comments > 0 and t.lexer.lexpos < (len(t.lexer.lexdata)-2):
        c = t.lexer.lexdata[t.lexer.lexpos:t.lexer.lexpos+2]
        if c == "*/":
            pushed_inner_comments -= 1
            t.lexer.skip(2)
        elif c == "/*":
            pushed_inner_comments += 1
            t.lexer.skip(2)
        else:
            t.lexer.skip(1)
    pass

def t_FORMAL_COMMENT(t):
    r'.*{\*(.|\n)*?\*}'

t_FORGOTTEN_COMMENT = r'\*/'
t_MACRO_INCLUDE = r'\#include.*'
t_MACRO_IFDEF = r'\#ifdef.*'
t_MACRO_ELSE = r'\#else'
t_MACRO_ENDIF = r'\#endif'
t_MACRO_DEFINE = r'\#define.*'
t_LITERAL = r"'[^']+'" 
t_NATURAL = r'\d\d*'
t_COLON = r':'
t_COMMA = r','
t_SLASH = r'/'
t_EQUAL = r'='
t_DOUBLEQUOTE = r'"'
t_LBRACKET = r'\['
t_RBRACKET = r']'
t_FORWARDARROW = r'-->'
t_LACTIONFACTARROW = r'--\['
t_RACTIONFACTARROW = r']->'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_AROBA = r'@'
t_HASH = r'\#'
t_DOT = r'\.'
#t_LFORMALCOMMENT = r'{\*'
#t_RFORMALCOMMENT = r'}\*'
t_LOWER = r'<'
t_HIGHER = r'>'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_EXPONENTIAL = r'\^'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_QUOTE = r'\''
t_TILDE = r'~'
t_DOLLAR = r'\$'
t_BANG = r'!'
t_EQUIVALENT = r'<=>'
t_UNIEQUIVALENT = r'⇔'
t_IMPLY = r'==>'
t_UNIIMPLY = r'⇒'
t_DISJUNCTION = r'\|'
t_UNIDISJUNCTION = r'∨'
t_CONJUNCTION = r'&'
t_UNICONJUNCTION = r'∧'
t_UNINOT = r'¬'
t_UNIFALSE = r'⊥'
t_UNITRUE = r'⊤'
t_UNIEXISTS = r'∃'
t_UNIFORALL = r'∀'
t_GOALTRIANGLE = r'▶'
t_GOALARROW = r'~~>'
t_FORMULASEP = r'∥'
t_XORSYMBOL = r'⊕'

t_LITTLE0 = r'₀'
t_LITTLE1 = r'₁'
t_LITTLE2 = r'₂'
t_LITTLE3 = r'₃'
t_LITTLE4 = r'₄'
t_LITTLE5 = r'₅'
t_LITTLE6 = r'₆'
t_LITTLE7 = r'₇'
t_LITTLE8 = r'₈'
t_LITTLE9 = r'₉'

t_ignore = " \t \n"
t_formula_DUMMY = "DUMMY_6d158c5c9d43472f11cb3e2c1863a8da" # Will never be matched, purposefully
t_allowleftright_DUMMY = "DUMMY_6d158c5c9d43472f11cb3e2c1863a8da" # Will never be matched, purposefully

def t_error(t):
    print("Illegal character '{}'".format(t.value[0]))
    t.lexer.skip(1)

def t_SECTION(t):
    r'section{\*.*\*}'
    t.type = "SECTION"
    return t

def t_KWDHIDELEMMAEQUAL(t):
    r'hide_lemma='
    t.type = "KWDHIDELEMMAEQUAL"
    return t

def t_KWDHEURISTICEQUAL(t):
    r'heuristic='
    t.type = "KWDHEURISTICEQUAL"
    return t

def t_COLOREQUAL(t):
    r'color='
    t.type = "COLOREQUAL"
    t.lexer.begin("color")
    return t

def t_COLOUREQUAL(t):
    r'colour='
    t.type = "COLOUREQUAL"
    t.lexer.begin("color")
    return t

def t_color_HEXCOLOR(t):
    r'[0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F]'
    t.lexer.begin("INITIAL")
    return t

def t_color_QUOTED_HEXCOLOR(t):
    r"'[0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F]'"
    t.lexer.begin("INITIAL")
    return t

def t_color_HASH_QUOTED_HEXCOLOR(t):
    r"'\#[0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F]'"
    t.lexer.begin("INITIAL")
    return t

def t_HEURISTICORACLE(t):
    r'(o|O)[ \t]+"[^"]+"' 
    t.type = "HEURISTICORACLE"
    return t

def t_ISFACTNAME_STRING(t):
    r'isFactName(\s*"[^"]*")*'
    t.type = "ISFACTNAME_STRING"
    return t

def t_ISINFACTTERMS_STRING(t):
    r'isInFactTerms(\s*"[^"]*")*'
    t.type = "ISINFACTTERMS_STRING"
    return t

def t_DHRENOISE_STRING(t):
    r'dhreNoise(\s*"[^"]*")*'
    t.type = "DHRENOISE_STRING"
    return t

def t_DEFAULTNOISE_STRING(t):
    r'defaultNoise(\s*"[^"]*")*'
    t.type = "DEFAULTNOISE_STRING"
    return t

def t_REASONABLENONCESNOISE_STRING(t):
    r'reasonableNoncesNoise(\s*"[^"]*")*'
    t.type = "REASONABLENONCESNOISE_STRING"
    return t

def t_NONABSURDGOAL_STRING(t):
    r'nonAbsurdGoal(\s*"[^"]*")*'
    t.type = "NONABSURDGOAL_STRING"
    return t

def t_REGEX_STRING(t):
    r'regex(\s*"[^"]*")+'
    t.type = "REGEX_STRING"
    return t

def t_IDENTDOTNATURAL(t):
    r'[a-zA-Z0-9][a-zA-Z_0-9-]*\.\d+'
    t.type = "IDENTDOTNATURAL"
    return t

def t_IDENT(t):
    r'[a-zA-Z0-9][a-zA-Z_0-9-]*'
    if t.value.isnumeric():
        t.type = 'NATURAL'
    elif t.value == "end":
        # Stop Parsing
        t.type = "KWDEND"
        for _ in t.lexer:
            continue # Exhaust all tokens after the "end"
    elif t.value == "left" and t.lexer.lexstate != "allowleftright":
        t.type = "KWDLEFT"
    elif t.value == "right" and t.lexer.lexstate != "allowleftright":
        t.type = "KWDRIGHT"
    else:
        t.type = reserved.get(t.value, 'IDENT')    # Check for reserved words
    return t 

lexer = lex.lex()

if __name__ == "__main__":
    filename = sys.argv[1]
    lexer.input(open(filename, "r").read())

# Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)

