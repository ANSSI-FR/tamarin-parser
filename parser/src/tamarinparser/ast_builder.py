from tamarinparser.tok import *

class ASTNode(object):
    def __init__(self, node_type, *args, **kwargs):
        self.type = node_type
        self.children = []
        for c in args:
            self.children.append(c)

    def build(self):
        return ""

class ASTNodeList(ASTNode):
    def __init__(self, node_type, *args, **kwargs):
        super().__init__(node_type, *args, **kwargs)

    def add_list(self, other):
        for c in other.children:
            self.children.append(c)

    def add_elt(self, elt):
        self.children.append(elt)

    def build(self):
        return ""

# p_security_protocol_theory
class SecurityProtocolTheory(ASTNode):
    def __init__(self, theory_name, body):
        super().__init__("SecurityProtocolTheory", theory_name, body)
        self.theory_name = theory_name
        self.body = body

    def build(self):
        return f"{keywords['KWDTHEORY']} {self.theory_name}\n{keywords['KWDBEGIN']}\n\n{self.body.build()}\n{keywords['KWDEND']}\n"

class Body(ASTNode):
    def __init__(self):
        super().__init__("Body")
    
    def add_item(self, item):
        self.children.append(item)

    def add_body(self, other):
        for c in other.children:
            self.children.append(c)

    def build(self):
        res = ""
        for c in self.children:
            res += c.build() + "\n"

        return res

class BodyItem(ASTNode):
    def __init__(self, item):
        super().__init__("BodyItem")
        self.item = item

    def build(self):
        return self.item.build()

class Test(ASTNode):
    def __init__(self, test_name, formula_start, formula, formula_end):
        super().__init__("Test")
        self.test_name = test_name
        self.formula_start = formula_start
        self.formula = formula
        self.formula_end = formula_end

    def build(self):
        ret = f"{keywords['KWDTEST']} {self.test_name}:\n{self.formula_start.build()} {self.formula.build()} {self.formula_end.build()}"
        return ret
# TODO: verify later that this is correct

class ForgottenComment(ASTNode):
    def __init__(self):
        pass
    def build(self):
        return ""

class Macro(ASTNode):
    def __init__(self, macro):
        super().__init__("Macro")
        self.macro = macro

    def build(self):
        return self.macro

class Section(ASTNode):
    def __init__(self, section):
        super().__init__("Section")
        self.section = macro

    def build(self):
        return self.section.build()

class SignatureSpec(ASTNode):
    def __init__(self, elt):
        super().__init__("SignatureSpec")
        self.elt = elt

    def build(self):
        return self.elt.build()

class Functions(ASTNode):
    def __init__(self, function_list):
        super().__init__("Functions")
        self.function_list = function_list

    def build(self):
        return f"{keywords['KWDFUNCTIONS']}: {self.function_list.build()}\n"

class FunctionList(ASTNode):
    def __init__(self):
        super().__init__("FunctionList")

    def add_function(self, function):
        self.children.append(function)

    def add_function_list(self, function_list):
        for f in function_list.children:
            self.children.append(f)

    def build(self):
        ret = ""
        for f in self.children[:-1]:
            ret += f.build()
            ret += ",\n\t\t"
        ret += self.children[-1].build()

        return ret

class FunctionSym(ASTNode):
    def __init__(self, name, arity, private=False, destructor=False):
        super().__init__("FunctionSym")
        self.name = name
        self.arity = arity
        self.private = private
        self.destructor = destructor

    def build(self):
        ret = f"{self.name}/{self.arity.build()}"
        if self.private:
            ret += f"[{keywords['KWDPRIVATE']}]"
        elif self.destructor:
            ret += f"[{keywords['KWDDESTRUCTOR']}]"
        return ret

class Arity(ASTNode):
    def __init__(self, arity):
        super().__init__("Arity")
        self.arity = arity

    def build(self):
        return self.arity

class Equations(ASTNode):
    def __init__(self, equation_list):
        super().__init__("Equations")
        self.equation_list = equation_list

    def build(self):
        return f"{keywords['KWDEQUATIONS']}: {self.equation_list.build()}\n"

class EquationList(ASTNode):
    def __init__(self):
        super().__init__("EquationList")

    def add_equation(self, equation):
        self.children.append(equation)

    def add_equation_list(self, equation_list):
        for f in equation_list.children:
            self.children.append(f)

    def build(self):
        ret = ""
        for f in self.children[:-1]:
            ret += f.build()
            ret += ",\n\t\t"
        ret += self.children[-1].build()

        return ret

class Equation(ASTNode):
    def __init__(self, lterm, rterm):
        super().__init__("Equation")
        self.lterm = lterm
        self.rterm = rterm
        
    def build(self):
        return f"{self.lterm.build()} = {self.rterm.build()}"

class Builtins(ASTNode):
    def __init__(self, builtins_list):
        super().__init__("Builtins")
        self.builtins_list = builtins_list

    def build(self):
        return f"{keywords['KWDBUILTINS']}: {self.builtins_list.build()}\n"

class BuiltinList(ASTNode):
    def __init__(self):
        super().__init__("BuiltinList")

    def add_builtin(self, builtin):
        self.children.append(builtin)

    def add_builtin_list(self, builtin_list):
        for f in builtin_list.children:
            self.children.append(f)

    def build(self):
        ret = ""
        for f in self.children[:-1]:
            ret += f.build()
            ret += ", "
        ret += self.children[-1].build()

        return ret

class Builtin(ASTNode):
    def __init__(self, builtin):
        super().__init__("Builtin")
        self.builtin = builtin

    def build(self):
        return self.builtin

class GlobalHeuristic(ASTNode):
    def __init__(self, goal_ranking_list):
        self.goal_ranking_list = goal_ranking_list

    def build(self):
        return f"{keywords['KWDHEURISTIC']}: {self.goal_ranking_list.build()}"

class GoalRankingList(ASTNode):

    def __init__(self):
        super().__init__("GoalRankingList")

    def add_goal_ranking(self, goal):
        self.children.append(goal)

    def add_goal_ranking_list(self, goal_ranking_list):
        for c in goal_ranking_list:
            self.children.append(c)

    def build(self):
        ret = ""
        for c in self.children:
            ret += c.build() + " "
        return ret

class StandardGoalRanking(ASTNode):

    def __init__(self, goal):
        super().__init__("StandardGoalRanking")
        self.goal = goal

    def build(self):
        return self.goal

class OracleGoalRanking(ASTNode):

    def __init__(self, goal):
        super().__init__("OracleGoalRanking")
        self.goal = goal

    def build(self):
        return self.goal

class Rule(ASTNode):
    def __init__(self, rule):
        super().__init__("Rule")
        self.rule = rule

    def build(self):
        return self.rule.build()

class SimpleRuleVariant(ASTNode):
    def __init__(self, rule, variants):
        super().__init__("SimpleRuleVariant")
        self.rule = rule
        self.variants = variants

    def build(self):
        return self.rule.build() + "\n" + self.variants.build()

class DiffRule(ASTNode):
    def __init__(self, simple_rule, rule_left, rule_right):
        super().__init__("DiffRule")
        self.simple_rule = simple_rule
        self.rule_left = rule_left
        self.rule_right = rule_right

    def build(self):
        return f"{self.simple_rule.build()}\n{keywords['KWDLEFT']}\n{self.rule_left.build()}\n{keywords['KWDRIGHT']}\n{self.rule_right.build()}" 


class SimpleRule(ASTNode):
    def __init__(self, header, body):
        super().__init__("SimpleRule")
        self.header = header
        self.body = body

    def build(self):
        return f"{self.header.build()}\n{self.body.build()}"

class SimpleRuleHeader(ASTNode):

    def __init__(self, rule_name):
        super().__init__("SimpleRuleHeader")
        self.rule_name = rule_name
        self.rule_attrs = None
        self.modulo = None

    def add_modulo(self, modulo):
        self.modulo = modulo

    def add_rule_attrs(self, rule_attrs):
        self.rule_attrs = rule_attrs

    def build(self):
        ret = f"{keywords['KWDRULE']} "
        if self.modulo is not None:
            ret += f"{self.modulo.build()} "
        ret += f"{self.rule_name}"
        if self.rule_attrs is not None:
            ret += f"{self.rule_attrs.build()} "
        ret += ":"
        return ret

class SimpleRuleBody(ASTNode):

    def __init__(self):
        super().__init__("SimpleRuleBody")
        self.let_block = None
        self.pre_facts = None
        self.post_facts = None
        self.action_facts = None

    def set_action_facts(self, action_facts):
        self.action_facts = action_facts

    def set_let_block(self, let_block):
        self.let_block = let_block

    def set_pre_facts(self, pre_facts):
        self.pre_facts = pre_facts

    def set_post_facts(self, post_facts):
        self.post_facts = post_facts

    def build(self):
        ret = ""
        if self.let_block is not None:
            ret += f"{self.let_block.build()}\n"
        ret += "\t[\n"
        ret += self.pre_facts.build()
        ret += "\n\t]\n"
        if self.action_facts is not None:
            ret += f"\t--[\n{self.action_facts.build()}\n\t]->\n"
        else:
            ret += "\t-->\n"
        ret += "\t[\n"
        ret += self.post_facts.build()
        ret += "\n\t]\n"
        return ret

class Variants(ASTNode):

    def __init__(self, simple_rule_list):
        super().__init__("Variants")
        self.simple_rule_list = simple_rule_list

    def build(self):
        return f"{keywords['KWDVARIANTS']}\n{self.simple_rule_list.build()}"

class SimpleRuleList(ASTNode):

    def __init__(self):
        super().__init__("SimpleRuleList")

    def add_simple_rule(self, simple_rule):
        self.children.append(simple_rule)

    def add_simple_rule_list(self, simple_rule_list):
        for c in simple_rule_list.children:
            self.children.append(c)

    def build(self):
        ret = ""
        for c in self.children[:-1]:
            ret += "\t" + c.build() + "\t,\n" 
        ret += "\t" + self.children[-1].build()
        return ret

class Modulo(ASTNode):

    def __init__(self, name):
        super().__init__("Modulo")
        self.name = name

    def build(self):
        return f"( {keywords['KWDMODULO']} {self.name} )"

class RuleAttrs(ASTNode):

    def __init__(self, rule_attr_list):
        super().__init__("RuleAttrs")
        self.rule_attr_list = rule_attr_list

    def build(self):
        return f"[ {self.rule_attr_list.build()} ]"

class RuleAttrList(ASTNode):

    def __init__(self):
        super().__init__("RuleAttrList")

    def add_rule_attr(self, rule_attr):
        self.children.append(rule_attr)

    def add_rule_attr_list(self, rule_attr_list):
        for c in rule_attr_list:
            self.children.append(c)

    def build(self):
        ret = ""
        for c in self.children[:-1]:
            ret += c.build() + "," 
        ret += self.children[-1].build()

class RuleAttr(ASTNode):

    def __init__(self, coloreq, hexcolor):
        super().__init__("RuleAttr")
        self.coloreq = coloreq
        self.hexcolor = hexcolor

    def build(self):
        return f"{self.coloreq.build()} {self.hexcolor.build()}"

class ColorEqual(ASTNode):

    def __init__(self, coloreq):
        super().__init__("ColorEqual")
        self.coloreq = coloreq

    def build(self):
        return self.coloreq

class Hexcolor(ASTNode):

    def __init__(self, hexcolor):
        super().__init__("Hexcolor")
        self.hexcolor = hexcolor

    def build(self):
        return self.hexcolor

class LetBlock(ASTNode):

    def __init__(self, stmt_list):
        super().__init__("LetBlock")
        self.stmt_list = stmt_list

    def build(self):
        return f"\t{keywords['KWDLET']}\n{self.stmt_list.build()}\t{keywords['KWDIN']}"

class LetBlockStmtList(ASTNode):

    def __init__(self):
        super().__init__("LetBlockStmtList")

    def add_stmt(self, stmt):
        self.children.append(stmt)

    def add_stmt_list(self, stmt_list):
        for stmt in stmt_list.children:
            self.children.append(stmt)

    def build(self):
        ret = ""
        for c in self.children:
            ret += f"\t\t{c.build()}\n"
        return ret

class LetBlockStmt(ASTNode):

    def __init__(self, msg_var, msetterm):
        super().__init__("LetBlockStmt")
        self.msg_var = msg_var
        self.msetterm = msetterm

    def build(self):
        return f"{self.msg_var.build()} = {self.msetterm.build()}"

class MsgVar(ASTNode):

    def __init__(self, name, post=None):
        super().__init__("MsgVar")
        self.name = name
        self.post = post

    def build(self):
        ret = f"{self.name}"
        if self.post is not None:
            ret += f":{self.post}"
        return ret

class Restriction(ASTNode):

    def __init__(self, restrictions=False):
        super().__init__("Restriction")
        self.restrictions = restrictions
        self.restriction_attrs = None

    def set_formula(self, formula_start, formula, formula_end):
        self.formula_start = formula_start
        self.formula = formula
        self.formula_end = formula_end

    def set_name(self, name):
        self.name = name

    def set_restriction_attrs(self, restriction_attrs):
        self.restriction_attrs = restriction_attrs

    def set_restriction_list(self, restriction_list):
        self.restriction_list = restriction_list

    def build(self):
        ret = ""
        if self.restrictions:
            ret = f"{keywords['KWDRESTRICTIONS']}:\n{self.restriction_list.build()}"
        else:
            ret = f"{keywords['KWDRESTRICTION']} {self.name}"
            if self.restriction_attrs is not None:
                ret += " " + self.restriction_attrs.build()
            ret += f":\n\t{self.formula_start.build()}{self.formula.build()}{self.formula_end.build()}\n"
        return ret

class RestrictionList(ASTNode):

    def __init__(self):
        super().__init__("RestrictionList")

    def add_restriction_list(self, restriction_list):
        for c in restriction_list:
            self.children.append(c)

    def add_restriction_elt(self, elt):
        self.children.append(elt)

    def build(self):
        ret = ""
        for c in self.children:
            ret += c.build() + "\n"
        return ret

class RestrictionElt(ASTNode):

    def __init__(self, formula_start, formula, formula_end):
        super().__init__("RestrictionElt")
        self.formula = formula
        self.formula_start = formula_start
        self.formula_end = formula_end

    def build(self):
        return f"{self.formula_start.build()} {self.formula.build()} {self.formula_end.build()}"

class RestrictionAttrs(ASTNode):

    def __init__(self, direction):
        super().__init__("RestrictionAttrs")
        self.direction = direction

    def build(self):
        return f"[{direction}]"

class Axiom(ASTNode):

    def __init__(self, name):
        super().__init__("Axiom")
        self.name = name
        self.direction = None

    def set_formula(self, formula_start, formula, formula_end):
        self.formula_start = formula_start
        self.formula = formula
        self.formula_end = formula_end

    def set_direction(self, direction):
        self.direction = direction

    def build(self):
        ret = f"{keywords['KWDAXIOM']} {self.name}"
        if self.direction is not None:
            ret += f"[{self.direction}]"
        ret += f": {self.formula_start.build()} {self.formula.build()} {self.formula_end.build()}"
        return ret

class Predicate(ASTNode):

    def __init__(self, formula):
        super().__init__("Predicate")
        self.formula = formula

    def build(self):
        return f"{keywords['KWDPREDICATE']}: {self.formula.build()}"

class Lemma(ASTNode):

    def __init__(self, lemma_hdr, lemma_body):
        super().__init__("Lemma")
        self.lemma_hdr = lemma_hdr
        self.lemma_body = lemma_body
        self.lemma_acc = None

    def set_lemma_acc(self, lemma_acc):
        self.lemma_acc = lemma_acc

    def build(self):
        ret = f"{self.lemma_hdr.build()}"
        if self.lemma_acc is not None:
            ret += f"{self.lemma_acc.build()}"
        ret += f"{self.lemma_body.build()}"
        return ret

class LemmaHeader(ASTNode):

    def __init__(self, name):
        super().__init__("LemmaHeader")
        self.modulo = None
        self.lemma_attrs = None
        self.quantifier = None
        self.name = name

    def set_modulo(self, modulo):
        self.modulo = modulo

    def set_lemma_attrs(self, lemma_attrs):
        self.lemma_attrs = lemma_attrs

    def set_quantifier(self, quantifier):
        self.quantifier = quantifier

    def build(self):
        ret = f"{keywords['KWDLEMMA']} "

        if self.modulo is not None:
            ret += f"{self.modulo.build()} "
        ret += f"{self.name}"

        if self.lemma_attrs is not None:
            ret += f" {self.lemma_attrs.build()}"

        ret += f":"

        if self.quantifier is not None:
            ret += f" {self.quantifier.build()}"
        ret += "\n"
        return ret

class LemmaAcc(ASTNode):

    def __init__(self, lemma_list, account):
        super().__init__("LemmaAcc")
        self.account = account
        self.lemma_list = lemma_list

    def build(self):
        return f"{self.lemma_list.build()} {self.account.build()} {keywords['KWDFOR']}"

class LemmaList(ASTNode):

    def __init__(self):
        super().__init__("LemmaList")

    def add_elt(self, elt):
        self.children.append(elt)

    def add_lemma_list(self, lemma_list):
        for c in lemma_list:
            self.children.append(c)

    def build(self):
        ret = ""
        for c in self.children[:-1]:
            ret += c.build()
            ret += ", "
        ret += self.children[-1].build()
        return ret

class LemmaBody(ASTNode):

    def __init__(self, formula_start, formula, formula_end):
        super().__init__("LemmaBody")
        self.formula_start = formula_start
        self.formula = formula
        self.formula_end = formula_end
        self.proof_skeleton = None

    def set_proof_skeleton(self, proof_skeleton):
        self.proof_skeleton = proof_skeleton

    def build(self):
        ret = f"{self.formula_start.build()} {self.formula.build()} {self.formula_end.build()}\n"
        if self.proof_skeleton is not None:
            ret += self.proof_skeleton.build() + "\n"
        return ret
        
class TraceQuantifier(ASTNode):

    def __init__(self, quant):
        super().__init__("TraceQuantifier")
        self.quant = quant

    def build(self):
        return self.quant

class LemmaAttrs(ASTNode):

    def __init__(self, lemma_attrs_list):
        super().__init__("LemmaAttrs")
        self.lemma_attrs_list = lemma_attrs_list

    def build(self):
        return f"[{self.lemma_attrs_list.build()}]"

class LemmaAttrList(ASTNode):

    def __init__(self):
        super().__init__("LemmaAttrList")

    def add_lemma_attr_list(self, lemma_attr_list):
        for c in lemma_attr_list.children:
            self.children.append(c)

    def add_lemma_attr(self, lemma_attr):
        self.children.append(lemma_attr)

    def build(self):
        ret = ""
        for c in self.children[:-1]:
            ret += c.build()
            ret += ", "
        ret += self.children[-1].build()
        return ret

class LemmaAttr(ASTNode):

    def __init__(self, content):
        super().__init__("LemmaAttr")
        self.content = content

    def build(self):
        return self.content.build()

class LemmaAttrContent(ASTNode):

    def __init__(self, keyword):
        super().__init__("LemmaAttrContent")
        self.keyword = keyword
        self.other = None

    def set_ident(self, other):
        self.other = other

    def set_goal_rankings(self, goal_rankings):
        self.other = goal_rankings.build()

    def build(self):
        ret = self.keyword
        if self.other is not None:
            ret += " " + self.other
        return ret

class LemmaGoalRankings(ASTNode):

    def __init__(self):
        super().__init__("LemmaGoalRankings")
        self.oracle_goal_ranking = None
        self.goal_ranking_list = []

    def set_oracle_goal_ranking(self, oracle_goal_ranking):
        self.oracle_goal_ranking = oracle_goal_ranking

    def set_lemma_goal_ranking_list(self, goal_ranking_list):
        self.goal_ranking_list = goal_ranking_list

    def build(self):
        if self.oracle_goal_ranking is not None:
            return self.oracle_goal_ranking.build()
        return f"{{{self.goal_ranking_list.build()}}}"

class LemmaGoalRankingList(ASTNode):

    def __init__(self):
        super().__init__("LemmaGoalRankingList")

    def add_lemma_goal_ranking_list(self, goal_ranking):
        for c in goal_ranking.children:
            self.children.append(c)

    def add_lemma_goal_ranking(self, goal_ranking):
        self.children.append(goal_ranking)

    def build(self):
        ret = ""
        for c in self.children[:-1]:
            ret += c.build()
            ret += ", "
        ret += self.children[-1].build()
        return ret

class LemmaGoalRanking(ASTNode):

    def __init__(self, goal):
        super().__init__("LemmaGoalRanking")
        self.goal = goal

    def build(self):
        return self.goal

class ProofSkeleton(ASTNode):

    def __init__(self, solved=False, by=None):
        super().__init__("ProofSkeleton")
        self.solved = solved
        self.by = by
        self.method = None
        self.skeleton = None
        self.case = None
        self.inner_list = None
        self.qed = False

    def set_method(self, method):
        self.method = method

    def set_skeleton(self, skeleton):
        self.skeleton = skeleton

    def set_case(self, case):
        self.case = case

    def set_qed(self, qed):
        self.qed = qed

    def set_proof_inner_list(self, lst):
        self.inner_list = lst

    def build(self):
        if self.solved:
            return f"{keywords['KWDSOLVED']}"
        if self.by is not None:
            return f"{keywords['KWDBY']} {self.by.build()}"

        res = "{self.method.build()}\n"
        if self.case is not None:
            res += "{keywords['KWDCASE']} {self.case}\n"
        res += self.skeleton.build()

        if self.inner_list is not None:
            res += self.skeleton.build()

        if self.qed is not None:
            res += f"{keywords['KWDQED']}"

        return res

class ProofSkeletonInnerList(ASTNode):

    def __init__(self):
        super().__init__("ProofSkeletonInnerList")

    def add_inner_list(self, other):
        for c in other.children:
            self.children.append(c)

    def add_inner_elt(self, elt):
        self.children.append(elt)

    def build(self):
        ret = ""
        for c in self.children[:-1]:
            ret += c.build()
            ret += "\n"
        ret += self.children[-1].build()
        return ret

class ProofSkeletonInnerElt(ASTNode):

    def __init__(self, case, skeleton):
        super().__init__("ProofSkeletonInnerElt")
        self.case = case
        self.skeleton = skeleton
        self.qed = False

    def set_qed(self, qed):
        self.qed = qed

    def build(self):
        res = f"{keywords['KWDNEXT']} {keywords['KWDCASE']} {self.case}\n"
        res += self.skeleton.build()
        if self.qed:
            res += f"{keywords['KWDQED']}"
        return res

class ProofMethod(ASTNode):

    def __init__(self, method):
        super().__init__("ProofMethod")
        self.method = method
        self.goal = None

    def set_goal(self, goal):
        self.goal = goal

    def build(self):
        res = self.method
        if self.goal is not None:
            res += f"({self.goal.build()})"
        return res

class DiffLemma(ASTNode):

    def __init__(self, name, skeleton):
        super().__init__("DiffLemma")
        self.name = name
        self.skeleton = skeleton
        self.attrs = None

    def set_attrs(self, attrs):
        self.attrs = attrs

    def build(self):
        res = f"{keywords['KWDDIFFLEMMA']} {self.name}"
        if self.attrs is not None:
            res += " " + self.attrs.build() 

        res += f":\n{self.skeleton.build()}"
        return res

class DiffProofMethod(ASTNode):

    def __init__(self, method):
        super().__init__("DiffProofMethod")
        self.method = method
        self.goal = None

    def build(self):
        res = self.method
        if self.goal is not None:
            res += f"({self.goal.build()})"
        return res
        

class DiffProofSkeleton(ASTNode):

    def __init__(self, mirrored=False, by=None):
        super().__init__("DiffProofSkeleton")
        self.solved = solved
        self.by = by
        self.method = None
        self.skeleton = None
        self.case = None
        self.inner_list = None
        self.qed = False

    def set_method(self, method):
        self.method = method

    def set_skeleton(self, skeleton):
        self.skeleton = skeleton

    def set_case(self, case):
        self.case = case

    def set_qed(self, qed):
        self.qed = qed

    def set_proof_inner_list(self, lst):
        self.inner_list = lst

    def build(self):
        if self.mirrored:
            return f"{keywords['KWDMIRRORED']}"
        if self.by is not None:
            return f"{keyword['KWDBY']} {self.by.build()}"

        res = "{self.method.build()}\n"
        if self.case is not None:
            res += "{keywords['KWDCASE']} {self.case}\n"
        res += self.skeleton.build()

        if self.inner_list is not None:
            res += self.skeleton.build()

        if self.qed is not None:
            res += f"{keywords['KWDQED']}"

        return res


class DiffProofSkeletonInnerList(ASTNode):

    def __init__(self):
        super().__init__("DiffProofSkeletonInnerList")

    def add_inner_list(self, other):
        for c in other.children:
            self.children.append(c)

    def add_elt(self):
        self.children.append(c)

    def build(self):
        ret = ""
        for c in self.children[:-1]:
            ret += c.build()
            ret += "\n"
        ret += self.children[-1].build()
        return ret

class DiffProofSkeletonInnerElt(ASTNode):

    def __init__(self, case, skeleton):
        super().__init__("DiffProofSkeletonInnerElt")
        self.case = case
        self.skeleton = skeleton
        self.qed = False

    def set_qed(self, qed):
        self.qed = qed

    def build(self):
        res = f"{keywords['KWDNEXT']} {keywords['KWDCASE']} {self.case}\n"
        res += self.skeleton.build()
        if self.qed:
            res += f"{keywords['KWDQED']}"
        return res

class Goal1(ASTNode):

    def __init__(self, fact, natural_sub, node_var):
        super().__init__("Goal1")
        self.fact = fact
        self.natural_sub = natural_sub
        self.node_var = node_var

    def build(self):
        return f"{self.fact.build()} ▶ {self.natural_sub.build()} {self.node_var.build()}"

class Goal2(ASTNode):

    def __init__(self, fact, node_var):
        super().__init__("Goal2")
        self.fact = fact
        self.node_var = node_var

    def build(self):
        return f"{self.fact.build()}@{self.node_var.build()}"

class Goal3(ASTNode):

    def __init__(self, node_var1, natural1, node_var2, natural2):
        super().__init__("Goal3")
        self.node_var1 = node_var1
        self.natural1 = natural1
        self.node_var2 = node_var2
        self.natural2 = natural2

    def build(self):
        return f"({self.node_var1.build()},{self.natural1.build()}) ~~> ({self.node_var2.build()},{self.natural2.build()})"

class Goal4(ASTNode):

    def __init__(self, lst):
        super().__init__("Goal4")
        self.lst = lst

    def build(self):
        return self.lst.build()

class Goal5(ASTNode):

    def __init__(self, natural):
        super().__init__("Goal5")
        self.natural = natural

    def build(self):
        return f"{keywords['KWDSPLITEQS']} ({self.natural.build()})"

class GoalFormulaList(ASTNode):

    def __init__(self):
        super().__init__("GoalFormulaList")

    def add_list(self, other):
        for c in other.children:
            self.children.append(c)

    def add_elt(self, elt):
        self.children.append(elt)

    def build(self):
        ret = ""
        for c in self.children[:-1]:
            ret += c.build()
            ret += " ∥ "
        ret += self.children[-1].build()
        return ret

class NodeVar(ASTNode):

    def __init__(self, node):
        super().__init__("NodeVar")
        self.node = node

    def build(self):
        return self.node

class Natural(ASTNode):

    def __init__(self, nat):
        super().__init__("Natural")
        self.nat = nat

    def build(self):
        return self.nat

class NaturalSub(ASTNodeList):

    def __init__(self):
        super().__init__("NaturalSub")

    def build(self):
        ret = ""
        for c in self.children:
            ret += c.build()

        return ret

class LittleDigit(ASTNode):

    def __init__(self, digit):
        super().__init__("LittleDigit")
        self.digit = digit

    def build(self):
        return self.digit

class Tupleterm(ASTNode):

    def __init__(self, term):
        super().__init__("Tupleterm")
        self.term = term

    def build(self):
        return "< " + self.term.build() + " >"

class MsettermList(ASTNodeList):

    def __init__(self):
        super().__init__("MsettermList")

    def build(self):
        ret = ""
        for c in self.children[:-1]:
            ret += c.build()
            ret += ", "
        ret += self.children[-1].build()
        return ret

class Msetterm(ASTNode):

    def __init__(self, term):
        super().__init__("Msetterm")
        self.term = term

    def build(self):
        return self.term.build()

class XortermList(ASTNodeList):

    def __init__(self):
        super().__init__("XortermList")

    def build(self):
        ret = ""
        for c in self.children[:-1]:
            ret += c.build()
            ret += " + "
        ret += self.children[-1].build()
        return ret

class Xorterm(ASTNode):

    def __init__(self, term):
        super().__init__("Xorterm")
        self.term = term

    def build(self):
        return self.term.build()

class MulttermList(ASTNodeList):

    def __init__(self):
        super().__init__("MulttermList")

    def build(self):
        ret = ""
        for c in self.children[:-1]:
            ret += c.build()
            ret += " XOR "
        ret += self.children[-1].build()
        return ret

class Multterm(ASTNode):

    def __init__(self, term):
        super().__init__("Multterm")
        self.term = term

    def build(self):
        return self.term.build()

class ExptermList(ASTNodeList):

    def __init__(self):
        super().__init__("ExptermList")

    def build(self):
        ret = ""
        for c in self.children[:-1]:
            ret += c.build()
            ret += " * "
        ret += self.children[-1].build()
        return ret

class Expterm(ASTNode):

    def __init__(self, term):
        super().__init__("Expterm")
        self.term = term

    def build(self):
        return self.term.build()

class TermList(ASTNodeList):

    def __init__(self):
        super().__init__("TermList")

    def build(self):
        ret = ""
        for c in self.children[:-1]:
            ret += c.build()
            ret += "^"
        ret += self.children[-1].build()
        return ret

class Term(ASTNode):

    def __init__(self, term, lst=False):
        super().__init__("Term")
        self.term = term
        self.lst = lst

    def build(self):
        if self.lst is not None:
            return self.term.build()
        return f"({self.term.build()})"

class NullaryFun(ASTNode):

    def __init__(self, fun):
        super().__init__("NullaryFun")
        self.fun = fun

    def build(self):
        return self.fun

class BinaryApp(ASTNode):

    def __init__(self, fun, term1, term2):
        super().__init__("BinaryApp")
        self.fun = fun
        self.term1 = term1
        self.term2 = term2

    def build(self):
        return f"{self.fun.build()}{{ {self.term1.build()} }}{self.term2.build()}"

class BinaryFun(ASTNode):

    def __init__(self, fun):
        super().__init__("BinaryFun")
        self.fun = fun

    def build(self):
        return self.fun

class NaryApp(ASTNode):

    def __init__(self, fun, termlist=None):
        super().__init__("NaryApp")
        self.fun = fun
        self.termlist = termlist

    def build(self):
        if self.termlist is not None:
            return f"{self.fun.build()}({self.termlist.build()})"
        else:
            return f"{self.fun.build()}"

class NaryFun(ASTNode):

    def __init__(self, fun):
        super().__init__("NaryFun")
        self.fun = fun

    def build(self):
        return self.fun

class Literal(ASTNode):

    def __init__(self, elt, b=False):
        super().__init__("Literal")
        self.elt = elt
        self.b = b

    def build(self):
        if self.b:
            return self.elt.build()
        return self.elt

class NonnodeVar(ASTNode):

    def __init__(self, elt, b=False):
        super().__init__("NonnodeVar")
        self.elt = elt
        self.b = b

    def build(self):
        if self.b:
            return self.elt.build()
        else:
            return self.elt

class Facts(ASTNodeList):

    def __init__(self):
        super().__init__("Facts")

    def build(self):
        ret = ""
        for c in self.children[:-1]:
            if type(c) != Empty:
                ret += f"\t\t{c.build()},\n"
        if len(self.children) > 0:
            ret += f"\t\t{self.children[-1].build()}"
        return ret

class Empty(ASTNode):

    def __init__(self):
        super().__init__("Empty")

    def build(self):
        return ""

class Fact1(ASTNode):

    def __init__(self, elt):
        super().__init__("Fact")
        self.name = elt.strip("()")
        self.elt = self.name + "()"

    def build(self):
        return self.name + "()"

class Fact2(ASTNode):

    def __init__(self, name, args):
        super().__init__("Fact")
        self.name = name
        self.args = args

    def build(self):
        return f"{self.name}({self.args.build()})"

class Fact3(ASTNode):

    def __init__(self, name, args):
        super().__init__("Fact")
        self.name = name
        self.args = args

    def build(self):
        return f"!{self.name}({self.args.build()})"

class Fact4(ASTNode):

    def __init__(self, name, annotes):
        super().__init__("Fact")
        self.name = name
        self.annotes = annotes

    def build(self):
        return f"{self.name}(){self.annotes.build()}"

class Fact5(ASTNode):

    def __init__(self, name, annotes):
        super().__init__("Fact")
        self.name = name
        self.annotes = annotes

    def build(self):
        return f"!{self.name}(){self.annotes.build()}"

class Fact6(ASTNode):

    def __init__(self, name, args, annotes):
        super().__init__("Fact")
        self.name = name
        self.args = args
        self.annotes = annotes

    def build(self):
        return f"{self.name}({self.args.build()}){self.annotes.build()}"

class Fact7(ASTNode):

    def __init__(self, name, args, annotes):
        super().__init__("Fact")
        self.name = name
        self.args = args
        self.annotes = annotes

    def build(self):
        return f"!{self.name}({self.args.build()}){self.annotes.build()}"

class FactAnnotes(ASTNode):

    def __init__(self, annotes):
        super().__init__("FactAnnotes")
        self.annotes = annotes

    def build(self):
        return "[" + self.annotes.build() + "]"

class FactAnnoteList(ASTNodeList):

    def __init__(self):
        super().__init__("FactAnnoteList")

    def build(self):
        ret = ""
        for c in self.children[:-1]:
            ret += c.build()
            ret += ", "
        ret += self.children[-1].build()
        return ret

class FactAnnote(ASTNode):

    def __init__(self, elt):
        super().__init__("FactAnnote")
        self.elt = elt

    def build(self):
        return self.elt

class FormulaStart(ASTNode):

    def __init__(self):
        super().__init__("FormulaStart")

    def build(self):
        return '"'

class FormulaEnd(ASTNode):

    def __init__(self):
        super().__init__("FormulaEnd")

    def build(self):
        return '"'

class Formula1(ASTNode):

    def __init__(self, imp):
        super().__init__("Formula")
        self.imp = imp

    def build(self):
        return self.imp.build()

class Formula2(ASTNode):

    def __init__(self, imp1, symbol, imp2):
        super().__init__("Formula")
        self.imp1 = imp1
        self.symbol = symbol
        self.imp2 = imp2

    def build(self):
        return self.imp1.build() +  self.symbol + "\n" + self.imp2.build()

class Imp1(ASTNode):

    def __init__(self, elt):
        super().__init__("Imp")
        self.elt = elt

    def build(self):
        return self.elt.build()

class Imp2(ASTNode):

    def __init__(self, imp1, symbol, imp2):
        super().__init__("Imp")
        self.imp1 = imp1
        self.symbol = symbol
        self.imp2 = imp2

    def build(self):
        return f"{self.imp1.build()} {self.symbol} {self.imp2.build()}"

class Imp3(ASTNode):

    def __init__(self, imp1, symbol, imp2):
        super().__init__("Imp")
        self.imp1 = imp1
        self.symbol = symbol
        self.imp2 = imp2

    def build(self):
        return f"{self.imp1.build()} {self.symbol} {self.imp2}"

class Disjunction(ASTNode):

    def __init__(self, elt1):
        super().__init__("Disjunction")
        self.elt1 = elt1
        self.symbol = None
        self.elt2 = None

    def set_symbol(self, symbol):
        self.symbol = symbol

    def set_elt2(self, elt2):
        self.elt2 = elt2

    def build(self):
        if self.symbol is not None:
            return f"{self.elt1.build()} {self.symbol} {self.elt2.build()}"
        else:
            return self.elt1.build()

class Conjunction(ASTNode):

    def __init__(self, elt1):
        super().__init__("Conjunction")
        self.elt1 = elt1
        self.symbol = None
        self.elt2 = None

    def set_symbol(self, symbol):
        self.symbol = symbol

    def set_elt2(self, elt2):
        self.elt2 = elt2

    def build(self):
        if self.symbol is not None:
            return f"{self.elt1.build()} {self.symbol} {self.elt2.build()}"
        else:
            return self.elt1.build()

class Negation1(ASTNode):

    def __init__(self, atom):
        super().__init__("Negation")
        self.atom = atom

    def build(self):
        return self.atom.build()

class Negation2(ASTNode):

    def __init__(self, atom, symbol):
        super().__init__("Negation")
        self.atom = atom
        self.symbol = symbol

    def build(self):
        return self.symbol + " " + self.atom.build()

class Negation3(ASTNode):

    def __init__(self, atom, symbol):
        super().__init__("Negation")
        self.atom = atom
        self.symbol = symbol

    def build(self):
        return self.symbol + " " + self.atom

class Negation4(ASTNode):

    def __init__(self, atom, symbol):
        super().__init__("Negation")
        self.atom = atom
        self.symbol = symbol

    def build(self):
        return self.symbol + "(" + self.atom + ")"

class Atom1(ASTNode):

    def __init__(self, elt):
        super().__init__("Atom")
        self.elt = elt

    def build(self):
        return self.elt

class Atom2(ASTNode):

    def __init__(self, elt):
        super().__init__("Atom")
        self.elt = elt

    def build(self):
        return self.elt.build()

class Atom3(ASTNode):

    def __init__(self, elt, last=False):
        super().__init__("Atom")
        self.elt = elt
        self.last = last

    def build(self):
        ret = ""
        if self.last:
            ret += keywords["KWDLAST"]

        ret += f"({self.elt.build()})"
        return ret

class Atom4(ASTNode):

    def __init__(self, elt1, symbol, elt2):
        super().__init__("Atom")
        self.elt1 = elt1
        self.symbol = symbol
        self.elt2 = elt2

    def build(self):
        return f"{self.elt1.build()} {self.symbol} {self.elt2.build()}"
        

class QuantFormula(ASTNode):

    def __init__(self, quantifier, lvar_list, formula):
        super().__init__("QuantFormula")
        self.quantifier = quantifier
        self.lvar_list = lvar_list
        self.formula = formula

    def build(self):
        return f"{self.quantifier.build()} {self.lvar_list.build()} . \n\t{self.formula.build()}"

class LvarList(ASTNodeList):

    def __init__(self):
        super().__init__("LvarList")

    def build(self):
        ret = ""
        for c in self.children[:-1]:
            ret += c.build()
            ret += " "
        ret += self.children[-1].build()
        return ret

class Lvar(ASTNode):

    def __init__(self, var):
        super().__init__("Lvar")
        self.var = var

    def build(self):
        return self.var.build()

class Quantifier(ASTNode):

    def __init__(self, elt):
        super().__init__("Quantifier")
        self.elt = elt

    def build(self):
        return self.elt

class Tactic(ASTNode):

    def __init__(self, hdr, content):
        super().__init__("Tactic")
        self.hdr = hdr
        self.content = content
        self.presort = None

    def set_presort(self, presort):
        self.presort = presort

    def build(self):
        if self.presort is not None:
            return f"{self.hdr.build()}\n{self.presort.build()}\n{self.content.build()}"
        else:
            return f"{self.hdr.build()}\n{self.content.build()}"

class TacticHdr(ASTNode):

    def __init__(self, name):
        super().__init__("TacticHdr")
        self.name = name

    def build(self):
        return f"{keywords['KWDTACTIC']}: {self.name}"

class Presort(ASTNode):

    def __init__(self, ranking):
        super().__init__("Presort")
        self.ranking = ranking

    def build(self):
        return f"{keywords['KWDPRESORT']}: {self.ranking.build()}"

class TacticContent(ASTNode):

    def __init__(self):
        super().__init__("TacticContent")
        self.prio_lst = None
        self.deprio_lst = None

    def set_prio_list(self, prio_lst):
        self.prio_lst = prio_lst

    def set_deprio_list(self, deprio_lst):
        self.deprio_lst = deprio_lst

    def build(self):
        res = ""
        if self.prio_lst is not None:
            res += self.prio_lst.build()

        if self.deprio_lst is not None:
            res += self.deprio_lst.build()
        return res

class PrioList(ASTNodeList):

    def __init__(self):
        super().__init__("PrioList")

    def build(self):
        ret = ""
        for c in self.children[:-1]:
            ret += c.build()
            ret += "\n"
        ret += self.children[-1].build() + "\n"
        return ret

class DeprioList(ASTNodeList):

    def __init__(self):
        super().__init__("DeprioList")

    def build(self):
        ret = ""
        for c in self.children[:-1]:
            ret += c.build()
            ret += "\n"
        ret += self.children[-1].build() + "\n"
        return ret

class Prio(ASTNode):

    def __init__(self, fct_list):
        super().__init__("Prio")
        self.tactic_function_list = fct_list
        self.post_ranking = None

    def set_post_ranking(self, post_ranking):
        self.post_ranking = post_ranking

    def build(self):
        res = f"{keywords['KWDPRIO']}:\n"
        if self.post_ranking is not None:
            res += f"{{ {self.post_ranking.build()} }}"
        res += self.tactic_function_list.build()
        return res

class Deprio(ASTNode):

    def __init__(self, fct_list):
        super().__init__("Deprio")
        self.tactic_function_list = fct_list
        self.post_ranking = None

    def set_post_ranking(self, post_ranking):
        self.post_ranking = post_ranking

    def build(self):
        res = f"{keywords['KWDDEPRIO']}: "
        if self.post_ranking is not None:
            res += f"{{ {self.post_ranking.build()} }}"
        res += self.tactic_function_list.build()
        return res

class PostRanking(ASTNode):

    def __init__(self, elt):
        super().__init__("PostRanking")
        self.elt = elt

    def build(self):
        return self.elt

class TacticFunctionList(ASTNodeList):

    def __init__(self):
        super().__init__("TacticFunctionList")

    def build(self):
        ret = ""
        for c in self.children[:-1]:
            ret += "    " + c.build()
            ret += "\n"
        ret += "    " + self.children[-1].build() + "\n"
        return ret

class Function(ASTNode):

    def __init__(self, elt):
        super().__init__("Function")
        self.elt = elt

    def build(self):
        return self.elt.build()

class AndFunctionList(ASTNodeList):

    def __init__(self):
        super().__init__("AndFunctionList")

    def build(self):
        ret = ""
        for c in self.children[:-1]:
            ret += c.build()
            ret += " ∨ " # ∧
        ret += self.children[-1].build()
        return ret

class AndFunction(ASTNode):

    def __init__(self, elt):
        super().__init__("AndFunction")
        self.elt = elt

    def build(self):
        return self.elt.build()

class NotFunctionList(ASTNodeList):

    def __init__(self):
        super().__init__("NotFunctionList")

    def build(self):
        ret = ""
        for c in self.children[:-1]:
            ret += c.build()
            ret += " ∧ "
        ret += self.children[-1].build()
        return ret

class NotFunction(ASTNode):

    def __init__(self, elt, no=False):
        super().__init__("NotFunction")
        self.elt = elt
        self.no = no

    def build(self):
        if self.no:
            return f"{keywords['KWDNOT']} {self.elt.build()}"
        else:
            return self.elt.build()

class FunctionAndParams(ASTNode):

    def __init__(self, elt):
        super().__init__("FunctionAndParams")
        self.elt = elt

    def build(self):
        return self.elt

