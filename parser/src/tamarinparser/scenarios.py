import copy
import tamarinparser.ast_builder as ast_builder
from tamarinparser.syntax import *

class LiteralChildItem(ast_builder.ASTNode):
    def __init__(self, literal):
        super().__init__("LiteralChildItem")
        self.literal = literal

    def build(self):
        return self.literal

# Format of nonce : Random(nonceId, ~n)

class Scenario(object):
    def __init__(self, name, base_theory, collect_fn):
        self.name = name

        # Copy the theory, so we don't mess with the original
        self.base_theory = copy.deepcopy(base_theory)

        self.base_theory.theory_name = self.base_theory.theory_name + f"_{name}"

        # Pass the pointer to the function, so we always have the same nonces collected in the same order
        self.collect_nonces = collect_fn

        # self.nonces : List[ (Rule, RandomFact) ]
        self.nonces = self.collect_nonces(self.base_theory)

    # Insert a rule right before the first rule
    def insert_rule(self, rule):
        idx = 0
        found = False
        for c in self.base_theory.body.children:
            if type(c.item) == ast_builder.Rule or type(c.item) == ast_builder.SimpleRuleVariant or type(c.item) == ast_builder.Macro:
                self.base_theory.body.children = self.base_theory.body.children[:idx] + [rule] + self.base_theory.body.children[idx:]
                found = True
                break
            idx += 1
        if not found:
            self.base_theory.body.children.append(rule)

    # Insert a rule right before the first restriction
    def insert_restriction(self, restriction):
        idx = 0
        found = False
        for c in self.base_theory.body.children:
            if type(c.item) == ast_builder.Restriction or type(c.item) == ast_builder.Lemma:
                self.base_theory.body.children = self.base_theory.body.children[:idx] + [restriction] + self.base_theory.body.children[idx:]
                found = True
                break
            idx += 1
        if not found:
            self.base_theory.body.children.append(restriction)

    def generate(self):
        pass

    def get_nonce_part(self, nonce):
        pass

def create_fact(name, *args):
    a = MsettermList()
    for b in args:
        a.add_elt(b)
    return Fact2(name, a)

class AbstractBaseScenario(Scenario):
    """In this model, we assume the nonce format is Random(~n)
    This scenario simply creates Fr(~n) for each Random fact encountered.
    No misuse is assumed here"""

    def __init__(self, name, theory, fn):
        super().__init__(name, theory, fn)

    # Generates the rule "GenerateRandoms" and modify the nonces names so that they match the generated nonces
    def gen_create_nonces(self):
        for (idx, (rule, nonce)) in enumerate(self.nonces):
            rule_body = SimpleRuleBody()
            gen_nonce_rule = SimpleRule(SimpleRuleHeader(f"GenRandom{idx}"), rule_body)

            pre_facts = Facts()
            post_facts = Facts()

            nonce_part = self.get_nonce_part(nonce)
            new_nonce_part = Literal(nonce_part.build() + f"{idx}")
            fresh_fact = Fact2("Fr", new_nonce_part)
            new_fact_name = f"Random{idx}"
            if len(nonce.args.children) == 1:
                out_fact = create_fact(new_fact_name, new_nonce_part)
            else:
                elts = nonce.args.children[:-1] + [new_nonce_part]
                out_fact = create_fact(new_fact_name, *elts)
            nonce.name = new_fact_name

            pre_facts.add_elt(fresh_fact)
            post_facts.add_elt(out_fact)

            rule_body.set_pre_facts(pre_facts)
            rule_body.set_post_facts(post_facts)

            self.insert_rule(BodyItem(Rule(gen_nonce_rule)))

    def generate(self):
        self.gen_create_nonces()
        return self.base_theory.build()

class SimpleBaseScenario(AbstractBaseScenario):
    """In this model, we assume the nonce format is Random(~n)
    This scenario simply creates Fr(~n) for each Random fact encountered.
    No misuse is assumed here"""

    def __init__(self, name, theory, fn):
        super().__init__(name, theory, fn)

    def get_nonce_part(self, nonce):
        return nonce.args.children[0]

class RoleBaseScenario(AbstractBaseScenario):
    """In this model, we assume the nonce format is Random(~n)
    This scenario simply creates Fr(~n) for each Random fact encountered.
    No misuse is assumed here"""

    def __init__(self, name, theory, fn):
        super().__init__(name, theory, fn)

    def get_nonce_part(self, nonce):
        return nonce.args.children[1]


class AbstractLeakOnceScenario(Scenario):
    """In this model, we assume the nonce format is Random(~n)
    This scenario leaks a nonce ~n for a given Random fact."""

    def __init__(self, name, theory, fn, idx_leak):
        super().__init__(name, theory, fn)

        self.idx_leak = idx_leak

    # Generates the rule "GenerateRandoms" and modify the nonces names so that they match the generated nonces
    def gen_create_nonces(self):
        misgen_rule_body = SimpleRuleBody()
        misgen_nonce_rule = SimpleRule(SimpleRuleHeader("MisgenerateRandoms"), misgen_rule_body)

        misgen_pre_facts = Facts()
        misgen_post_facts = Facts()

        for (idx, (rule, nonce)) in enumerate(self.nonces):
            current_rule_body = SimpleRuleBody()
            current_gen_nonce = SimpleRule(SimpleRuleHeader(f"GenRandom{idx}"), current_rule_body)

            nonce_part = self.get_nonce_part(nonce)
            new_nonce_part = Literal(nonce_part.build() + f"{idx}")
            pre_facts = Facts()
            post_facts = Facts()

            fresh_fact = Fact2("Fr", new_nonce_part)

            new_fact_name = f"Random{idx}"

            if len(nonce.args.children) == 1:
                out_fact = create_fact(new_fact_name, new_nonce_part)
            else:
                elts = nonce.args.children[:-1] + [new_nonce_part]
                out_fact = create_fact(new_fact_name, *elts)
            nonce.name = new_fact_name

            # If this is the nonce we have to leak, add an Out(fact) to the post facts of the nonce generation rule
            if idx == self.idx_leak:
                leak_fact = Fact2("Out", new_nonce_part)
                misgen_pre_facts.add_elt(fresh_fact)
                misgen_post_facts.add_elt(leak_fact)
                misgen_post_facts.add_elt(out_fact)

            pre_facts.add_elt(fresh_fact)
            post_facts.add_elt(out_fact)

            current_rule_body.set_pre_facts(pre_facts)
            current_rule_body.set_post_facts(post_facts)

            self.insert_rule(BodyItem(Rule(current_gen_nonce)))

        misgen_rule_body.set_pre_facts(misgen_pre_facts)
        misgen_rule_body.set_post_facts(misgen_post_facts)

        action_facts = Facts()
        action_facts.add_elt(Fact1("MisgenerateOnlyOnce"))

        misgen_rule_body.set_action_facts(action_facts)

        self.insert_rule(BodyItem(Rule(misgen_nonce_rule)))

    def gen_restriction(self):
        restr = LiteralChildItem(f"restriction RestrMisgeneratesOnlyOnce:\n\"All #i #j . MisgenerateOnlyOnce() @i & MisgenerateOnlyOnce() @j ==> #i = #j\"\n")
        self.insert_restriction(BodyItem(restr))

    def generate(self):
        self.gen_create_nonces()
        self.gen_restriction()
        return self.base_theory.build()

class SimpleLeakOnceScenario(AbstractLeakOnceScenario):

    def __init__(self, name, theory, fn, idx_leak):
        super().__init__(name, theory, fn, idx_leak)

    def get_nonce_part(self, nonce):
        return nonce.args.children[0]

class RoleLeakOnceScenario(AbstractLeakOnceScenario):
    def __init__(self, name, theory, fn, idx_leak):
        super().__init__(name, theory, fn, idx_leak)


    def get_nonce_part(self, nonce):
        return nonce.args.children[1]

class AbstractLeakAlwaysScenario(Scenario):
    def __init__(self, name, theory, fn, idx_leak):
        super().__init__(name, theory, fn)

        self.idx_leak = idx_leak

    # Generates the rule "GenerateRandoms" and modify the nonces names so that they match the generated nonces
    def gen_create_nonces(self):

        for (idx, (rule, nonce)) in enumerate(self.nonces):
            rule_body = SimpleRuleBody()
            gen_nonce_rule = SimpleRule(SimpleRuleHeader(f"GenRandom{idx}"), rule_body)

            pre_facts = Facts()
            post_facts = Facts()

            nonce_part = self.get_nonce_part(nonce)
            new_nonce_part = Literal(nonce_part.build() + f"{idx}")
            fresh_fact = Fact2("Fr", new_nonce_part)
            new_fact_name = f"Random{idx}"
            if len(nonce.args.children) == 1:
                out_fact = create_fact(new_fact_name, new_nonce_part)
            else:
                elts = nonce.args.children[:-1] + [new_nonce_part]
                out_fact = create_fact(new_fact_name, *elts)
            nonce.name = new_fact_name

            # If this is the nonce we have to leak, add an Out(fact) to the post facts of the nonce generation rule
            if idx == self.idx_leak:
                leak_fact = Fact2("Out", new_nonce_part)
                post_facts.add_elt(leak_fact)

            pre_facts.add_elt(fresh_fact)
            post_facts.add_elt(out_fact)

            rule_body.set_pre_facts(pre_facts)
            rule_body.set_post_facts(post_facts)

            self.insert_rule(BodyItem(Rule(gen_nonce_rule)))

    def generate(self):
        self.gen_create_nonces()
        return self.base_theory.build()

class SimpleLeakAlwaysScenario(AbstractLeakAlwaysScenario):
    def __init__(self, name, theory, fn, idx_leak):
        super().__init__(name, theory, fn, idx_leak)

    def get_nonce_part(self, nonce):
        return nonce.args.children[0]

class RoleLeakAlwaysScenario(AbstractLeakAlwaysScenario):
    def __init__(self, name, theory, fn, idx_leak):
        super().__init__(name, theory, fn, idx_leak)

    def get_nonce_part(self, nonce):
        return nonce.args.children[1]

class SimpleReuseAlwaysScenario(Scenario):
    """In this model, we assume the nonce format is Random(~n)
    This scenario reuses Random{idx1} all the time.

    Transforms:
rule A:
    [Random(~n), Random(~o)] --> []

    Into:
rule MisgenerateRandoms:
    [Fr(~n0)] --[OnlyOnce()]-> [!Random0(~n0)]

rule GenerateRandoms:
    [Fr(~n1)] --> [Random1(~n1)] # <-- this is not a typo

rule A:
    [!Random0(~n), Random1(~o)] --> []
        """

    def __init__(self, name, theory, fn, idx):
        """idx1 and idx2 are the nonce indices that are reused"""
        super().__init__(name, theory, fn)

        self.idx = idx

    # Generates the rule "GenerateRandoms" and modify the nonces names so that they match the generated nonces
    def gen_create_nonces(self):

        misgen_rule_body = SimpleRuleBody()
        misgen_nonce_rule = SimpleRule(SimpleRuleHeader("MisgenerateRandoms"), misgen_rule_body)

        misgen_pre_facts = Facts()
        misgen_post_facts = Facts()

        for (idx, (rule, nonce)) in enumerate(self.nonces):
            rule_body = SimpleRuleBody()
            gen_nonce_rule = SimpleRule(SimpleRuleHeader(f"GenRandom{idx}"), rule_body)

            pre_facts = Facts()
            post_facts = Facts()
            if idx == self.idx:
                nonce_part = nonce.args.children[0] # Extract the nonce ~n from the fact
                new_nonce_part = Literal(nonce_part.build() + f"{idx}")
                fresh_fact = Fact2("Fr", new_nonce_part)
                new_fact_name = f"!Random{idx}"
                out_fact = Fact2(new_fact_name, new_nonce_part)
                if len(nonce.args.children) == 1:
                    out_fact = create_fact(new_fact_name, new_nonce_part)
                else:
                    elts = nonce.args.children[:-1] + [new_nonce_part]
                    out_fact = create_fact(new_fact_name, *elts)
                nonce.name = new_fact_name

                misgen_pre_facts.add_elt(fresh_fact)
                misgen_post_facts.add_elt(out_fact)


            else:
                nonce_part = nonce.args.children[0] # Extract the nonce ~n from the fact
                new_nonce_part = Literal(nonce_part.build() + f"{idx}")
                fresh_fact = Fact2("Fr", new_nonce_part)
                new_fact_name = f"Random{idx}"
                out_fact = Fact2(new_fact_name, new_nonce_part)
                if len(nonce.args.children) == 1:
                    out_fact = create_fact(new_fact_name, new_nonce_part)
                else:
                    elts = nonce.args.children[:-1] + [new_nonce_part]
                    out_fact = create_fact(new_fact_name, *elts)
                nonce.name = new_fact_name

                pre_facts.add_elt(fresh_fact)
                post_facts.add_elt(out_fact)

                rule_body.set_pre_facts(pre_facts)
                rule_body.set_post_facts(post_facts)

                self.insert_rule(BodyItem(Rule(gen_nonce_rule)))

        action_facts = Facts()
        action_facts.add_elt(Fact1("MisgenerateOnlyOnce"))

        misgen_rule_body.set_action_facts(action_facts)

        misgen_rule_body.set_pre_facts(misgen_pre_facts)
        misgen_rule_body.set_post_facts(misgen_post_facts)

        self.insert_rule(BodyItem(Rule(misgen_nonce_rule)))

    def gen_restriction(self):
        restr = LiteralChildItem(f"restriction RestrMisgeneratesOnlyOnce:\n\"All #i #j . MisgenerateOnlyOnce() @i & MisgenerateOnlyOnce() @j ==> #i = #j\"\n")
        self.insert_restriction(BodyItem(restr))

    def generate(self):
        self.gen_create_nonces()
        self.gen_restriction()
        return self.base_theory.build()

class RoleReuseAlwaysScenario(Scenario):
    """In this model, we assume the nonce format is Random('role', ~n)
    This scenario reuses Random{idx1} into Random{idx2} all the time.

    Transforms:
rule A:
    [Random('A', ~n), Random('A', ~o)] --> []

    Into:

rule MisgenerateRandoms:
    [Fr(~n0)] --[MisgenerateOnlyOnce()]-> [!Random0('A', ~n0)]

rule GenRandom1:
    [Fr(~n1)] --> [Random1('A', ~n1)]

rule A:
    [!Random0('A', ~n), Random1('A', ~o)] --> []

restriction RestrMisgeneratesOnlyOnce:
    "All #i #j . MisgenerateOnlyOnce() @i & MisgenerateOnlyOnce() @j ==> #i = #j"
        """

    def __init__(self, name, theory, fn, idx):
        """idx1 and idx2 are the nonce indices that are reused in the global nonce list
        It is assumed that nonces[idx1] and nonces[idx2] are used by the same role"""
        super().__init__(name, theory, fn)

        self.idx = idx

    def gen_create_nonces(self):
        rule_body = SimpleRuleBody()
        gen_nonce_rule = SimpleRule(SimpleRuleHeader("GenerateRandoms"), rule_body)
        misgen_rule_body = SimpleRuleBody()
        misgen_nonce_rule = SimpleRule(SimpleRuleHeader("MisgenerateRandoms"), misgen_rule_body)

        pre_facts = Facts()
        post_facts = Facts()

        misgen_pre_facts = Facts()
        misgen_post_facts = Facts()

        for (idx, (rule, nonce)) in enumerate(self.nonces):
            if idx == self.idx:
                nonce_part = nonce.args.children[1] # Extract the nonce ~n from the fact
                new_nonce_part = Literal(nonce_part.build() + f"{idx}")
                fresh_fact = Fact2("Fr", new_nonce_part)
                new_fact_name = f"!Random{idx}"
                out_fact = Fact2(new_fact_name, new_nonce_part)
                if len(nonce.args.children) == 1:
                    out_fact = create_fact(new_fact_name, new_nonce_part)
                else:
                    elts = nonce.args.children[:-1] + [new_nonce_part]
                    out_fact = create_fact(new_fact_name, *elts)
                nonce.name = new_fact_name

                misgen_pre_facts.add_elt(fresh_fact)
                misgen_post_facts.add_elt(out_fact)


            else:
                nonce_part = nonce.args.children[1] # Extract the nonce ~n from the fact
                new_nonce_part = Literal(nonce_part.build() + f"{idx}")
                fresh_fact = Fact2("Fr", new_nonce_part)
                new_fact_name = f"Random{idx}"
                out_fact = Fact2(new_fact_name, new_nonce_part)
                if len(nonce.args.children) == 1:
                    out_fact = create_fact(new_fact_name, new_nonce_part)
                else:
                    elts = nonce.args.children[:-1] + [new_nonce_part]
                    out_fact = create_fact(new_fact_name, *elts)
                nonce.name = new_fact_name

                pre_facts.add_elt(fresh_fact)
                post_facts.add_elt(out_fact)

        rule_body.set_pre_facts(pre_facts)
        rule_body.set_post_facts(post_facts)

        action_facts = Facts()
        action_facts.add_elt(Fact1("MisgenerateOnlyOnce"))

        misgen_rule_body.set_action_facts(action_facts)

        misgen_rule_body.set_pre_facts(misgen_pre_facts)
        misgen_rule_body.set_post_facts(misgen_post_facts)

        self.insert_rule(BodyItem(Rule(gen_nonce_rule)))
        self.insert_rule(BodyItem(Rule(misgen_nonce_rule)))

    def gen_restriction(self):
        restr = LiteralChildItem(f"restriction RestrMisgeneratesOnlyOnce:\n\"All #i #j . MisgenerateOnlyOnce() @i & MisgenerateOnlyOnce() @j ==> #i = #j\"\n")
        self.insert_restriction(BodyItem(restr))

    def generate(self):
        self.gen_create_nonces()
        self.gen_restriction()
        return self.base_theory.build()

class SimpleReuseOnceScenario(Scenario):
    """In this model, we assume the nonce format is Random(~n)
    This scenario reuses Random{idx1} into Random{idx2} once time.

    Transforms:
rule A:
    [Random(~n), Random(~o)] --> []

    Into:

rule MisgenerateRandomsOnce:
    [Fr(~n0)] --[MisgeneratesOnlyOnce()]-> [Random0(~n0),Random1(~n0)]

restriction RestrMisgenerateOnlyOnce:
    "All #i #j . MisgenerateOnlyOnce() @i & MisgeneratesOnlyOnce() @j ==> #i = #j"

rule GenRandom0:
    [Fr(~n0)] --> [Random0(~n0)]

rule GenRandom1:
    [Fr(~n1)] --> [Random1(~n1)]

rule A:
    [Random0(~n), Random1(~o)] --> []
        """

    def __init__(self, name, theory, fn, idx1, idx2):
        super().__init__(name, theory, fn)

        self.idx1 = idx1
        self.idx2 = idx2

    # Generates the rule "GenerateRandoms" and modify the nonces names so that they match the generated nonces
    def gen_create_nonces(self):
        misgen_rule_body = SimpleRuleBody()
        misgen_nonce_rule = SimpleRule(SimpleRuleHeader("MisGenerateRandoms"), misgen_rule_body)

        misgen_pre_facts = Facts()
        misgen_post_facts = Facts()

        for (idx, (rule, nonce)) in enumerate(self.nonces):
            rule_body = SimpleRuleBody()
            gen_nonce_rule = SimpleRule(SimpleRuleHeader(f"GenRandom{idx}"), rule_body)

            pre_facts = Facts()
            post_facts = Facts()

            if idx == self.idx2:
                name_idx = self.idx1
            else:
                name_idx = idx

            nonce_part = nonce.args.children[0] # Extract the nonce ~n from the fact
            new_nonce_part = Literal(nonce_part.build() + f"{idx}")
            fresh_fact = Fact2("Fr", new_nonce_part)
            new_fact_name = f"Random{idx}"
            if len(nonce.args.children) == 1:
                out_fact = create_fact(new_fact_name, new_nonce_part)
            else:
                elts = nonce.args.children[:-1] + [new_nonce_part]
                out_fact = create_fact(new_fact_name, *elts)
            nonce.name = new_fact_name

            pre_facts.add_elt(fresh_fact)
            post_facts.add_elt(out_fact)

            if idx == self.idx2 or idx == self.idx1:
                reused_nonce_part = Literal(self.nonces[self.idx1][1].args.children[0].build() + f"{name_idx}")
                if len(nonce.args.children) == 1:
                    misgen_out_fact = create_fact(new_fact_name, reused_nonce_part)
                else:
                    elts = nonce.args.children[:-1] + [reused_nonce_part]
                    misgen_out_fact = create_fact(new_fact_name, *elts)
                misgen_pre_facts.add_elt(fresh_fact)
                misgen_post_facts.add_elt(misgen_out_fact)
                if self.idx1 == self.idx2:
                    misgen_post_facts.add_elt(misgen_out_fact)

            rule_body.set_pre_facts(pre_facts)
            rule_body.set_post_facts(post_facts)
            self.insert_rule(BodyItem(Rule(gen_nonce_rule)))

        misgen_rule_body.set_pre_facts(misgen_pre_facts)
        misgen_rule_body.set_post_facts(misgen_post_facts)

        action_facts = Facts()
        action_facts.add_elt(Fact1("MisgenerateOnlyOnce"))

        misgen_rule_body.set_action_facts(action_facts)

        self.insert_rule(BodyItem(Rule(misgen_nonce_rule)))

    # Generates the restriction "RestrMisgenerateOnlyOnce"
    def gen_restriction(self):
        restr = LiteralChildItem(f"restriction RestrMisgeneratesOnlyOnce:\n\"All #i #j . MisgenerateOnlyOnce() @i & MisgenerateOnlyOnce() @j ==> #i = #j\"\n")
        self.insert_restriction(BodyItem(restr))

    def generate(self):
        self.gen_create_nonces()
        self.gen_restriction()
        return self.base_theory.build()

class RoleReuseOnceScenario(Scenario):
    """In this model, we assume the nonce format is Random(~n)
    This scenario reuses Random{idx1} into Random{idx2} once time.

    Transforms:
rule A:
    [Random('A', ~n), Random('A', ~o)] --> []

    Into:

rule MisgenerateRandomsOnce:
    [Fr(~n0)] --[MisgeneratesOnlyOnce()]-> [Random0('A', ~n0),Random1('A', ~n0)]

restriction RestrMisgenerateOnlyOnce:
    "All #i #j . MisgenerateOnlyOnce() @i & MisgeneratesOnlyOnce() @j ==> #i = #j"

rule GenRandom0:
    [Fr(~n0)] --> [Random0('A', ~n0)]

rule GenRandom1:
    [Fr(~n1)] --> [Random1('A', ~n1)]

rule A:
    [Random0('A', ~n), Random1('A', ~o)] --> []
        """

    def __init__(self, name, theory, fn, idx1, idx2):
        super().__init__(name, theory, fn)

        self.idx1 = idx1
        self.idx2 = idx2

    # Generates the rule "GenerateRandoms" and modify the nonces names so that they match the generated nonces
    def gen_create_nonces(self):
        rule_body = SimpleRuleBody()
        gen_nonce_rule = SimpleRule(SimpleRuleHeader("GenerateRandoms"), rule_body)

        misgen_rule_body = SimpleRuleBody()
        misgen_nonce_rule = SimpleRule(SimpleRuleHeader("MisGenerateRandoms"), misgen_rule_body)

        pre_facts = Facts()
        post_facts = Facts()

        misgen_pre_facts = Facts()
        misgen_post_facts = Facts()

        for (idx, (rule, nonce)) in enumerate(self.nonces):
            if idx == self.idx2:
                name_idx = self.idx1
            else:
                name_idx = idx

            nonce_part = nonce.args.children[1] # Extract the nonce ~n from the fact
            new_nonce_part = Literal(nonce_part.build() + f"{idx}")
            fresh_fact = Fact2("Fr", new_nonce_part)
            new_fact_name = f"Random{idx}"
            if len(nonce.args.children) == 1:
                out_fact = create_fact(new_fact_name, new_nonce_part)
            else:
                elts = nonce.args.children[:-1] + [new_nonce_part]
                out_fact = create_fact(new_fact_name, *elts)
            nonce.name = new_fact_name

            pre_facts.add_elt(fresh_fact)
            post_facts.add_elt(out_fact)

            if idx == self.idx2 or idx == self.idx1:
                reused_nonce_part = Literal(self.nonces[self.idx1][1].args.children[1].build() + f"{name_idx}")
                if len(nonce.args.children) == 1:
                    misgen_out_fact = create_fact(new_fact_name, reused_nonce_part)
                else:
                    elts = nonce.args.children[:-1] + [reused_nonce_part]
                    misgen_out_fact = create_fact(new_fact_name, *elts)
                misgen_pre_facts.add_elt(fresh_fact)
                misgen_post_facts.add_elt(misgen_out_fact)
                if self.idx1 == self.idx2:
                    misgen_post_facts.add_elt(misgen_out_fact)

        rule_body.set_pre_facts(pre_facts)
        rule_body.set_post_facts(post_facts)

        misgen_rule_body.set_pre_facts(misgen_pre_facts)
        misgen_rule_body.set_post_facts(misgen_post_facts)

        action_facts = Facts()
        action_facts.add_elt(Fact1("MisgenerateOnlyOnce"))

        misgen_rule_body.set_action_facts(action_facts)

        self.insert_rule(BodyItem(Rule(misgen_nonce_rule)))
        self.insert_rule(BodyItem(Rule(gen_nonce_rule)))

    # Generates the restriction "RestrMisgenerateOnlyOnce"
    def gen_restriction(self):
        restr = LiteralChildItem(f"restriction RestrMisgeneratesOnlyOnce:\n\"All #i #j . MisgenerateOnlyOnce() @i & MisgenerateOnlyOnce() @j ==> #i = #j\"\n")
        self.insert_restriction(BodyItem(restr))

    def generate(self):
        self.gen_create_nonces()
        self.gen_restriction()
        return self.base_theory.build()


