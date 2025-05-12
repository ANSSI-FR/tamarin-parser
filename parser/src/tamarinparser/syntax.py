from tamarinparser.tok import *
from tamarinparser.ast_builder import *
import ply.yacc as yacc

s_parser = None

def p_security_protocol_theory(p):
    'security_protocol_theory : KWDTHEORY IDENT KWDBEGIN body KWDEND'
    p[0] = SecurityProtocolTheory(p[2], p[4])

def p_body_1(p):
    '''body : body body_item'''
    b = Body()
    b.add_body(p[1])
    b.add_item(p[2])
    p[0] = b

def p_body_2(p):
    '''body : body_item'''
    b = Body()
    b.add_item(p[1])
    p[0] = b

def p_body_item(p):
    '''body_item : signature_spec
                | global_heuristic
                | rule
                | restriction
                | tactic
                | section
                | macro
                | axiom
                | predicate
                | lemma
                | test
                | diff_lemma
                | forgotten_comment'''
                #| formal_comment'''

    p[0] = BodyItem(p[1])

def p_test(p):
    'test : KWDTEST IDENT COLON formula_start formula formula_end'
    p[0] = Test(p[2], p[4], p[5], p[6], p[7])

def p_forgotten_comment(p):
    'forgotten_comment : FORGOTTEN_COMMENT'
    p[0] = ForgottenComment()

def p_macro(p):
    '''macro : MACRO_INCLUDE
             | MACRO_IFDEF
             | MACRO_ELSE
             | MACRO_ENDIF
             | MACRO_DEFINE'''
    p[0] = Macro(p[1])

def p_section(p):
    'section : SECTION'
    p[0] = Section(p[1])

def p_signature_spec(p):
    '''signature_spec : functions
                      | equations
                      | builtins'''
    p[0] = SignatureSpec(p[1])

def p_functions(p):
    'functions : KWDFUNCTIONS COLON function_list'
    p[0] = Functions(p[3])

def p_function_list_1(p):
    '''function_list : function_list COMMA function_sym'''
    p[0] = FunctionList()
    p[0].add_function_list(p[1])
    p[0].add_function(p[3])

def p_function_list_2(p):
    '''function_list : function_sym'''
    p[0] = FunctionList()
    p[0].add_function(p[1])

def p_function_sym_1(p):
    '''function_sym : IDENT SLASH arity'''
    p[0] = FunctionSym(p[1], p[3])

def p_function_sym_2(p):
    '''function_sym : IDENT SLASH arity LBRACKET KWDPRIVATE RBRACKET'''
    p[0] = FunctionSym(p[1], p[3], private=True)

def p_function_sym_3(p):
    '''function_sym : IDENT SLASH arity LBRACKET KWDDESTRUCTOR RBRACKET'''
    p[0] = FunctionSym(p[1], p[3], destructor=True)

def p_arity(p):
    '''arity : NATURAL'''
    p[0] = Arity(p[1])

def p_equations(p):
    '''equations : KWDEQUATIONS COLON equation_list'''
    p[0] = Equations(p[3])

def p_equation_list_1(p):
    '''equation_list : equation_list COMMA equation'''
    p[0] = EquationList()
    p[0].add_equation_list(p[1])
    p[0].add_equation(p[3])

def p_equation_list_2(p):
    '''equation_list : equation'''
    p[0] = EquationList()
    p[0].add_equation(p[1])

def p_equation(p):
    'equation : term EQUAL term'
    p[0] = Equation(p[1], p[3])

def p_builtins(p):
    'builtins : KWDBUILTINS COLON builtin_list'
    p[0] = Builtins(p[3])

def p_builtin_list_1(p):
    '''builtin_list : builtin_list COMMA builtin'''
    p[0] = BuiltinList()
    p[0].add_builtin_list(p[1])
    p[0].add_builtin(p[3])

def p_builtin_list_2(p):
    '''builtin_list : builtin'''
    p[0] = BuiltinList()
    p[0].add_builtin(p[1])

def p_builtin(p):
    '''builtin : KWDDIFFIEHELLMAN
                 | KWDHASHING
                 | KWDSYMMETRICENCRYPTION
                 | KWDASYMMETRICENCRYPTION
                 | KWDSIGNING
                 | KWDBILINEARPAIRING
                 | KWDXOR
                 | KWDMULTISET
                 | KWDREVEALINGSIGNING'''
    p[0] = Builtin(p[1])

def p_global_heuristic(p):
    'global_heuristic : KWDHEURISTIC COLON goal_ranking_list'
    p[0] = GlobalHeuristic(p[3])

def p_goal_ranking_list(p):
    '''goal_ranking_list : goal_ranking_list standard_goal_ranking'''
    p[0] = GoalRankingList()
    p[0].add_goal_ranking_list(p[1])
    p[0].add_goal_ranking(p[2])

def p_goal_ranking_list_1(p):
    '''goal_ranking_list : goal_ranking_list oracle_goal_ranking'''
    p[0] = GoalRankingList()
    p[0].add_goal_ranking_list(p[1])
    p[0].add_goal_ranking(p[2])

def p_goal_ranking_list_2(p):
    '''goal_ranking_list : standard_goal_ranking'''
    p[0] = GoalRankingList()
    p[0].add_goal_ranking(p[1])

def p_goal_ranking_list_3(p):
    '''goal_ranking_list : oracle_goal_ranking'''
    p[0] = GoalRankingList()
    p[0].add_goal_ranking(p[1])

def p_standard_goal_ranking(p):
    'standard_goal_ranking : IDENT'
    p[0] = StandardGoalRanking(p[1])

def p_oracle_goal_ranking(p):
    'oracle_goal_ranking : HEURISTICORACLE'
    p[0] = OracleGoalRanking(p[1])

def p_rule_1(p):
    '''rule : simple_rule
          | simple_rule_variant
          | diff_rule'''
    p[0] = Rule(p[1])

def p_simple_rule_variant(p):
    '''simple_rule_variant : simple_rule variants'''
    p[0] = SimpleRuleVariant(p[1], p[2])

def p_diff_rule(p):
    '''diff_rule : simple_rule KWDLEFT rule KWDRIGHT rule'''
    p[0] = DiffRule(p[1], p[3], p[5])

def p_simple_rule(p):
    'simple_rule : simple_rule_hdr simple_rule_body'
    p[0] = SimpleRule(p[1], p[2])

def p_simple_rule_hdr(p):
    'simple_rule_hdr : simple_rule_header'
    p.lexer.begin("allowleftright")
    p[0] = p[1]

def p_simple_rule_header_1(p):
    'simple_rule_header : KWDRULE IDENT COLON'
    p[0] = SimpleRuleHeader(p[2])

def p_simple_rule_header_2(p):
    'simple_rule_header : KWDRULE modulo IDENT COLON'
    p[0] = SimpleRuleHeader(p[3])
    p[0].add_modulo(p[2])

def p_simple_rule_header_3(p):
    'simple_rule_header : KWDRULE IDENT rule_attrs COLON'
    p[0] = SimpleRuleHeader(p[2])
    p[0].add_rule_attrs(p[3])

def p_simple_rule_header_4(p):
    'simple_rule_header : KWDRULE modulo IDENT rule_attrs COLON'
    p[0] = SimpleRuleHeader(p[3])
    p[0].add_modulo(p[2])
    p[0].add_rule_attrs(p[4])

def p_simple_rule_body_1(p):
    'simple_rule_body : LBRACKET facts RBRACKET FORWARDARROW LBRACKET facts rbracket_reset_state'
    p[0] = SimpleRuleBody()
    p[0].set_pre_facts(p[2])
    p[0].set_post_facts(p[6])

def p_simple_rule_body_2(p):
    'simple_rule_body : LBRACKET facts RBRACKET LACTIONFACTARROW facts RACTIONFACTARROW LBRACKET facts rbracket_reset_state'
    p[0] = SimpleRuleBody()
    p[0].set_pre_facts(p[2])
    p[0].set_action_facts(p[5])
    p[0].set_post_facts(p[8])

def p_simple_rule_body_3(p):
    'simple_rule_body : let_block LBRACKET facts RBRACKET FORWARDARROW LBRACKET facts rbracket_reset_state'
    p[0] = SimpleRuleBody()
    p[0].set_let_block(p[1])
    p[0].set_pre_facts(p[3])
    p[0].set_post_facts(p[7])

def p_simple_rule_body_4(p):
    'simple_rule_body : let_block LBRACKET facts RBRACKET LACTIONFACTARROW facts RACTIONFACTARROW LBRACKET facts rbracket_reset_state'
    p[0] = SimpleRuleBody()
    p[0].set_let_block(p[1])
    p[0].set_pre_facts(p[3])
    p[0].set_action_facts(p[6])
    p[0].set_post_facts(p[9])

# No need a class for this
def p_rbracket_reset_state(p):
    'rbracket_reset_state : RBRACKET'
    p.lexer.begin("INITIAL")

def p_variants(p):
    'variants : KWDVARIANTS simple_rule_list'
    p[0] = Variants(p[2])

def p_simple_rule_list_1(p):
    '''simple_rule_list : simple_rule_list COMMA simple_rule'''
    p[0] = SimpleRuleList()
    p[0].add_simple_rule_list(p[1])
    p[0].add_simple_rule(p[3])

def p_simple_rule_list_2(p):
    '''simple_rule_list : simple_rule'''
    p[0] = SimpleRuleList()
    p[0].add_simple_rule(p[1])

def p_modulo(p):
    '''modulo : LPAREN KWDMODULO IDENT RPAREN'''
    p[0] = Modulo(p[3])

def p_rule_attrs(p):
    '''rule_attrs : LBRACKET rule_attr_list RBRACKET'''
    p[0] = RuleAttrs(p[2])

def p_rule_attr_list_1(p):
    '''rule_attr_list : rule_attr_list COMMA rule_attr'''
    p[0] = RuleAttrList()
    p[0].add_rule_attr_list(p[1])
    p[0].add_rule_attr(p[3])

def p_rule_attr_list_2(p):
    '''rule_attr_list : rule_attr'''
    p[0] = RuleAttrList()
    p[0].add_rule_attr(p[1])

def p_rule_attr(p):
    '''rule_attr : color_equal hexcolor
                | colour_equal hexcolor
                | color_equal quoted_hexcolor
                | colour_equal quoted_hexcolor'''
    p[0] = RuleAttr(p[1], p[2])

def p_color_equal(p):
    'color_equal : COLOREQUAL'
    p[0] = ColorEqual(p[1])

def p_colour_equal(p):
    'colour_equal : COLOUREQUAL'
    p[0] = ColorEqual(p[1])

def p_hexcolor_1(p):
    'hexcolor : HASH HEXCOLOR'
    p[0] = Hexcolor(p[2])

def p_hexcolor_2(p):
    'hexcolor : HEXCOLOR'
    p[0] = Hexcolor(p[1])

def p_quoted_hexcolor_1(p):
    'quoted_hexcolor : QUOTED_HEXCOLOR'
    p[0] = Hexcolor(p[1])

def p_quoted_hexcolor_2(p):
    'quoted_hexcolor : HASH_QUOTED_HEXCOLOR'
    p[0] = Hexcolor(p[1])

def p_let_block(p):
    'let_block : KWDLET let_block_stmt_list KWDIN'
    p[0] = LetBlock(p[2])

def p_let_block_stmt_list_1(p):
    '''let_block_stmt_list : let_block_stmt_list let_block_stmt'''
    p[0] = LetBlockStmtList()
    p[0].add_stmt_list(p[1])
    p[0].add_stmt(p[2])

def p_let_block_stmt_list_2(p):
    '''let_block_stmt_list : let_block_stmt'''
    p[0] = LetBlockStmtList()
    p[0].add_stmt(p[1])

def p_let_block_stmt(p):
    '''let_block_stmt : msg_var EQUAL msetterm'''
    p[0] = LetBlockStmt(p[1], p[3])

def p_msg_var_1(p):
    'msg_var : IDENT'
    p[0] = MsgVar(p[1])

def p_msg_var_2(p):
    'msg_var : IDENTDOTNATURAL'
    p[0] = MsgVar(p[1])

def p_msg_var_3(p):
    'msg_var : IDENT COLON IDENT' # After colon should be 'msg'
    p[0] = MsgVar(p[1], post=p[3])

def p_msg_var_4(p):
    'msg_var : IDENTDOTNATURAL COLON IDENT' # After colon should be 'msg'
    p[0] = MsgVar(p[1], post=p[3])

def p_restriction_1(p):
    'restriction : KWDRESTRICTION IDENT COLON formula_start formula formula_end'
    p[0] = Restriction()
    p[0].set_name(p[2])
    p[0].set_formula(p[4], p[5], p[6])

def p_restriction_2(p):
    'restriction : KWDRESTRICTION IDENT restriction_attrs COLON formula_start formula formula_end'
    p[0] = Restriction()
    p[0].set_name(p[2])
    p[0].set_restriction_attrs(p[2])
    p[0].set_formula(p[5], p[6], p[7])

def p_restriction_3(p):
    'restriction : KWDRESTRICTIONS COLON restriction_list'
    p[0] = Restriction(restrictions=True)
    p[0].set_restriction_list(p[3])

def p_restriction_list_1(p):
    '''restriction_list : restriction_list restriction_elt'''
    p[0] = RestrictionList()
    p[0].add_restriction_list(p[1])
    p[0].add_restriction(p[2])

def p_restriction_list_2(p):
    '''restriction_list : restriction_elt'''
    p[0] = RestrictionList()
    p[0].add_restriction(p[1])

def p_restriction_elt(p):
    'restriction_elt : formula_start formula formula_end'
    p[0] = RestrictionElt(p[1], p[2], p[3])

def p_restriction_attrs(p):
    '''restriction_attrs : LBRACKET KWDLEFT RBRACKET
                    | LBRACKET KWDRIGHT RBRACKET'''
    p[0] = RestrictionAttrs(p[2])

def p_axiom_1(p):
    '''axiom : KWDAXIOM IDENT COLON formula_start formula formula_end'''
    p[0] = Axiom(p[2])
    p[0].set_formula(p[4], p[5], p[6])

def p_axiom_2(p):
    '''axiom : KWDAXIOM IDENT LBRACKET KWDRIGHT RBRACKET COLON formula_start formula formula_end
             | KWDAXIOM IDENT LBRACKET KWDLEFT RBRACKET COLON formula_start formula formula_end'''
    p[0] = Axiom(p[2])
    p[0].set_direction(p[4])
    p[0].set_formula(p[7], p[8], p[9])

def p_predicate(p):
    'predicate : KWDPREDICATE COLON formula'
    p[0] = Predicate(p[3])

def p_lemma_1(p):
    'lemma : lemma_header lemma_body'
    p[0] = Lemma(p[1], p[2])

def p_lemma_2(p):
    'lemma : lemma_header lemma_acc lemma_body'
    p[0] = Lemma(p[1], p[3])
    p[0].set_lemma_acc(p[2])

def p_lemma_header_1(p):
    'lemma_header : KWDLEMMA IDENT COLON'
    p[0] = LemmaHeader(p[2])

def p_lemma_header_2(p):
    'lemma_header : KWDLEMMA modulo IDENT COLON'
    p[0] = LemmaHeader(p[3])
    p[0].set_modulo(p[2])

def p_lemma_header_3(p):
    'lemma_header : KWDLEMMA IDENT lemma_attrs COLON'
    p[0] = LemmaHeader(p[2])
    p[0].set_lemma_attrs(p[3])

def p_lemma_header_4(p):
    'lemma_header : KWDLEMMA modulo IDENT lemma_attrs COLON'
    p[0] = LemmaHeader(p[3])
    p[0].set_lemma_attrs(p[4])
    p[0].set_modulo(p[2])

def p_lemma_header_5(p):
    'lemma_header : KWDLEMMA IDENT COLON trace_quantifier'
    p[0] = LemmaHeader(p[2])
    p[0].set_quantifier(p[4])

def p_lemma_header_6(p):
    'lemma_header : KWDLEMMA modulo IDENT COLON trace_quantifier'
    p[0] = LemmaHeader(p[3])
    p[0].set_modulo(p[2])
    p[0].set_quantifier(p[5])

def p_lemma_header_7(p):
    'lemma_header : KWDLEMMA IDENT lemma_attrs COLON trace_quantifier'
    p[0] = LemmaHeader(p[2])
    p[0].set_lemma_attrs(p[3])
    p[0].set_quantifier(p[5])

def p_lemma_header_8(p):
    'lemma_header : KWDLEMMA modulo IDENT lemma_attrs COLON trace_quantifier'
    p[0] = LemmaHeader(p[3])
    p[0].set_modulo(p[2])
    p[0].set_lemma_attrs(p[4])
    p[0].set_quantifier(p[6])

def p_lemma_acc_1(p):
    'lemma_acc : lemma_list KWDACCOUNT KWDFOR'
    p[0] = LemmaAcc(p[1], p[2])

def p_lemma_acc_2(p):
    'lemma_acc : lemma_list KWDACCOUNTS KWDFOR'
    p[0] = LemmaAcc(p[1], p[2])

def p_lemma_list_1(p):
    '''lemma_list : lemma_list COMMA IDENT'''
    p[0] = LemmaList()
    p[0].add_lemma_list(p[1])
    p[0].add_elt(p[3])

def p_lemma_list_2(p):
    '''lemma_list : IDENT'''
    p[0] = LemmaList()
    p[0].add_elt(p[1])

def p_lemma_body_1(p):
    'lemma_body : formula_start formula formula_end proof_skeleton'
    p[0] = LemmaBody(p[1], p[2], p[3])
    p[0].set_proof_skeleton(p[4])

def p_lemma_body_2(p):
    'lemma_body : formula_start formula formula_end'
    p[0] = LemmaBody(p[1], p[2], p[3])

def p_trace_quantifier(p):
    '''trace_quantifier : KWDALLTRACES
                      | KWDEXISTSTRACE'''
    p[0] = TraceQuantifier(p[1])

def p_lemma_attrs(p):
    'lemma_attrs : LBRACKET lemma_attr_list RBRACKET'
    p[0] = LemmaAttrs(p[2])

def p_lemma_attr_list_1(p):
    '''lemma_attr_list : lemma_attr_list COMMA lemma_attr'''
    p[0] = LemmaAttrList()
    p[0].add_lemma_attr_list(p[1])
    p[0].add_lemma_attr(p[3])

def p_lemma_attr_list_2(p):
    '''lemma_attr_list : lemma_attr'''
    p[0] = LemmaAttrList()
    p[0].add_lemma_attr(p[1])

def p_lemma_attr(p):
    'lemma_attr : lemma_attr_content'
    p[0] = LemmaAttr(p[1])

def p_lemma_attr_content_1(p):
    '''lemma_attr_content : KWDSOURCES
                | KWDREUSE
                | KWDUSEINDUCTION
                | KWDLEFT
                | KWDRIGHT'''
    p[0] = LemmaAttrContent(p[1])

def p_lemma_attr_content_2(p):
    '''lemma_attr_content : KWDHIDELEMMAEQUAL IDENT'''
    p[0] = LemmaAttrContent(p[1])
    p[0].set_ident(p[2])

def p_lemma_attr_content_3(p):
    '''lemma_attr_content : KWDHEURISTICEQUAL lemma_goal_rankings'''
    p[0] = LemmaAttrContent(p[1])
    p[0].set_goal_rankings(p[2])

def p_lemma_goal_rankings_1(p):
    '''lemma_goal_rankings : LBRACE lemma_goal_ranking_list RBRACE'''
    p[0] = LemmaGoalRankings()
    p[0].set_lemma_goal_ranking_list(p[2])

def p_lemma_goal_rankings_2(p):
    '''lemma_goal_rankings : lemma_goal_ranking'''
    p[0] = LemmaGoalRankings()
    p[0].set_lemma_goal_ranking_list(p[1])

def p_lemma_goal_rankings_3(p):
    '''lemma_goal_rankings : oracle_goal_ranking'''
    p[0] = LemmaGoalRankings()
    p[0].set_oracle_goal_ranking_list(p[1])

def p_lemma_goal_ranking_list_1(p):
    '''lemma_goal_ranking_list : lemma_goal_ranking_list COMMA lemma_goal_ranking'''
    p[0] = LemmaGoalRankingList()
    p[0].add_lemma_goal_ranking_list(p[1])
    p[0].add_lemma_goal_ranking(p[3])

def p_lemma_goal_ranking_list_2(p):
    '''lemma_goal_ranking_list : lemma_goal_ranking'''
    p[0] = LemmaGoalRankingList()
    p[0].add_lemma_goal_ranking(p[1])

def p_lemma_goal_ranking(p):
    'lemma_goal_ranking : IDENT'
    p[0] = LemmaGoalRanking(p[1])

def p_proof_skeleton_1(p):
    '''proof_skeleton : KWDSOLVED'''
    p[0] = ProofSkeleton(solved=True)

def p_proof_skeleton_2(p):
    '''proof_skeleton : KWDBY proof_method'''
    p[0] = ProofSkeleton(by=p[2])

def p_proof_skeleton_3(p):
    '''proof_skeleton : proof_method proof_skeleton'''
    p[0] = ProofSkeleton()
    p[0].set_method(p[1])
    p[0].set_skeleton(p[2])

def p_proof_skeleton_4(p):
    '''proof_skeleton : proof_method KWDCASE IDENT proof_skeleton
                      | proof_method KWDCASE NATURAL proof_skeleton'''
    p[0] = ProofSkeleton()
    p[0].set_method(p[1])
    p[0].set_case(p[3])
    p[0].set_skeleton(p[4])

def p_proof_skeleton_5(p):
    '''proof_skeleton : proof_method KWDCASE IDENT proof_skeleton proof_skeleton_inner_list
                      | proof_method KWDCASE NATURAL proof_skeleton proof_skeleton_inner_list'''
    p[0] = ProofSkeleton()
    p[0].set_method(p[1])
    p[0].set_case(p[3])
    p[0].set_skeleton(p[4])
    p[0].set_proof_inner_list(p[5])
                      

def p_proof_skeleton_6(p):
    '''proof_skeleton : proof_method KWDCASE IDENT proof_skeleton KWDQED
                      | proof_method KWDCASE NATURAL proof_skeleton KWDQED'''
    p[0] = ProofSkeleton()
    p[0].set_method(p[1])
    p[0].set_case(p[3])
    p[0].set_skeleton(p[4])
    p[0].set_qed(True)

def p_proof_skeleton_7(p):
    '''proof_skeleton : proof_method KWDCASE IDENT proof_skeleton proof_skeleton_inner_list KWDQED
                      | proof_method KWDCASE NATURAL proof_skeleton proof_skeleton_inner_list KWDQED'''
    p[0] = ProofSkeleton()
    p[0].set_method(p[1])
    p[0].set_case(p[3])
    p[0].set_skeleton(p[4])
    p[0].set_proof_inner_list(p[5])
    p[0].set_qed(True)

def p_proof_skeleton_inner_list_1(p):
    '''proof_skeleton_inner_list : proof_skeleton_inner_list proof_skeleton_inner_elt'''
    p[0] = ProofSkeletonInnerList()
    p[0].add_inner_list(p[1])
    p[0].add_inner_elt(p[2])

def p_proof_skeleton_inner_list_2(p):
    '''proof_skeleton_inner_list : proof_skeleton_inner_elt'''
    p[0] = ProofSkeletonInnerList()
    p[0].add_inner_elt(p[1])

def p_proof_skeleton_inner_elt(p):
    '''proof_skeleton_inner_elt : KWDNEXT KWDCASE IDENT proof_skeleton 
                              | KWDNEXT KWDCASE IDENT proof_skeleton KWDQED
                              | KWDNEXT KWDCASE NATURAL proof_skeleton
                              | KWDNEXT KWDCASE NATURAL proof_skeleton KWDQED'''
    p[0] = ProofSkeletonInnerElt(p[3], p[4])
    if len(p) > 5:
        p[0].set_qed(True)

def p_proof_method(p):
    '''proof_method : KWDSORRY
                    | KWDSIMPLIFY
                    | KWDSOLVE LPAREN goal RPAREN
                    | KWDCONTRADICTION
                    | KWDINDUCTION'''
    p[0] = ProofMethod(p[1])
    if len(p) > 2:
        p[0].set_goal(p[3])

def p_diff_lemma_1(p):
    'diff_lemma : KWDDIFFLEMMA IDENT COLON diff_proof_skeleton'
    p[0] = DiffLemma(p[2], p[4])

def p_diff_lemma_2(p):
    'diff_lemma : KWDDIFFLEMMA IDENT lemma_attrs COLON diff_proof_skeleton'
    p[0] = DiffLemma(p[2], p[5])
    p[0].set_attrs(p[3])

def p_diff_proof_method(p):
    '''diff_proof_method : KWDSORRY
                    | KWDRULEEQ
                    | KWDBACKWARDSEARCH
                    | KWDATTACK
                    | KWDUNFINISHABLEDIFF
                    | KWDSTEP LPAREN proof_method RPAREN'''
    p[0] = DiffProofMethod(p[1])
    if len(p) > 2:
        p[0].set_goal(p[3])

def p_diff_proof_skeleton_1(p):
    '''diff_proof_skeleton : KWDMIRRORED'''
    p[0] = DiffProofSkeleton(mirrored=True)

def p_diff_proof_skeleton_2(p):
    '''diff_proof_skeleton : KWDBY diff_proof_method'''
    p[0] = DiffProofSkeleton(by=p[2])

def p_diff_proof_skeleton_3(p):
    '''diff_proof_skeleton : diff_proof_method diff_proof_skeleton'''
    p[0] = DiffProofSkeleton()
    p[0].set_method(p[1])
    p[0].set_skeleton(p[2])

def p_diff_proof_skeleton_4(p):
    '''diff_proof_skeleton : diff_proof_method KWDCASE IDENT diff_proof_skeleton
                           | diff_proof_method KWDCASE NATURAL diff_proof_skeleton'''
    p[0] = DiffProofSkeleton()
    p[0].set_method(p[1])
    p[0].set_case(p[3])
    p[0].set_skeleton(p[4])

def p_diff_proof_skeleton_5(p):
    '''diff_proof_skeleton : diff_proof_method KWDCASE IDENT diff_proof_skeleton KWDQED
                           | diff_proof_method KWDCASE NATURAL diff_proof_skeleton KWDQED'''
    p[0] = DiffProofSkeleton()
    p[0].set_method(p[1])
    p[0].set_case(p[3])
    p[0].set_skeleton(p[4])
    p[0].set_qed(True)

def p_diff_proof_skeleton_6(p):
    '''diff_proof_skeleton : diff_proof_method KWDCASE IDENT diff_proof_skeleton diff_proof_skeleton_inner_list
                           | diff_proof_method KWDCASE NATURAL diff_proof_skeleton diff_proof_skeleton_inner_list'''
    p[0] = DiffProofSkeleton()
    p[0].set_method(p[1])
    p[0].set_case(p[3])
    p[0].set_skeleton(p[4])
    p[0].set_proof_inner_list(p[5])

def p_diff_proof_skeleton_7(p):
    '''diff_proof_skeleton : diff_proof_method KWDCASE IDENT diff_proof_skeleton diff_proof_skeleton_inner_list KWDQED
                           | diff_proof_method KWDCASE NATURAL diff_proof_skeleton diff_proof_skeleton_inner_list KWDQED'''
    p[0] = DiffProofSkeleton()
    p[0].set_method(p[1])
    p[0].set_case(p[3])
    p[0].set_skeleton(p[4])
    p[0].set_proof_inner_list(p[5])
    p[0].set_qed(True)

def p_diff_proof_skeleton_inner_list_1(p):
    '''diff_proof_skeleton_inner_list : diff_proof_skeleton_inner_list diff_proof_skeleton_inner_elt'''
    p[0] = DiffProofSkeleton()
    p[0].add_inner_list(p[1])
    p[0].add_elt(p[2])

def p_diff_proof_skeleton_inner_list_2(p):
    '''diff_proof_skeleton_inner_list : diff_proof_skeleton_inner_elt'''
    p[0] = DiffProofSkeleton()
    p[0].add_elt(p[1])

def p_diff_proof_skeleton_inner_elt(p):
    '''diff_proof_skeleton_inner_elt : KWDNEXT KWDCASE IDENT diff_proof_skeleton 
                              | KWDNEXT KWDCASE IDENT diff_proof_skeleton KWDQED
                              | KWDNEXT KWDCASE NATURAL diff_proof_skeleton
                              | KWDNEXT KWDCASE NATURAL diff_proof_skeleton KWDQED'''
    p[0] = DiffProofSkeletonInnerElt(p[3], p[4])
    if len(p) > 5:
        p[0].set_qed(True)

def p_goal_1(p):
    'goal : fact GOALTRIANGLE natural_sub node_var'
    p[0] = Goal1(p[1], p[3], p[4])

def p_goal_2(p):
    'goal : fact AROBA node_var'
    p[0] = Goal2(p[1], p[3])

def p_goal_3(p):
    'goal : LPAREN node_var COMMA natural RPAREN GOALARROW LPAREN node_var COMMA natural RPAREN'
    p[0] = Goal3(p[2], p[4], p[8], p[10])

def p_goal_4(p):
    'goal : formula_list'
    p[0] = Goal4(p[1])

def p_goal_5(p):
    'goal : KWDSPLITEQS LPAREN natural RPAREN'
    p[0] = Goal5(p[3])

def p_goal_formula_list_1(p):
    '''formula_list : formula_list FORMULASEP formula'''
    p[0] = GoalFormulaList()
    p[0].add_list(p[1])
    p[0].add_elt(p[3])

def p_goal_formula_list_2(p):
    '''formula_list : formula'''
    p[0] = GoalFormulaList()
    p[0].add_elt(p[1])

def p_node_var_1(p):
    'node_var : HASH IDENT'
    p[0] = NodeVar(f"#{p[2]}")

def p_node_var_2(p):
    'node_var : IDENT'
    p[0] = NodeVar(f"{p[1]}")

def p_node_var_3(p):
    'node_var : IDENTDOTNATURAL'
    p[0] = NodeVar(f"{p[1]}")

def p_node_var_4(p):
    'node_var : IDENTDOTNATURAL COLON KWDNODE'
    p[0] = NodeVar(f"{p[1]}:{p[3]}")

def p_node_var_5(p):
    'node_var : IDENT COLON KWDNODE'
    p[0] = NodeVar(f"{p[1]}:{p[3]}")

def p_node_var_6(p):
    'node_var : HASH IDENTDOTNATURAL'
    p[0] = NodeVar(f"#{p[2]}")

def p_node_var_7(p):
    'node_var : NATURAL' # Test this, to handle function( 1 )
    p[0] = NodeVar(f"{p[1]}")

def p_natural(p):
    'natural : NATURAL'
    p[0] = Natural(f"{p[1]}")

def p_natural_sub_1(p):
    '''natural_sub : natural_sub little_digit'''
    p[0] = NaturalSub()
    p[0].add_list(p[1])
    p[0].add_elt(p[2])

def p_natural_sub_2(p):
    '''natural_sub : little_digit'''
    p[0] = NaturalSub()
    p[0].add_elt(p[1])

def p_little_digit(p):
    '''little_digit : LITTLE0
                    | LITTLE1
                    | LITTLE2
                    | LITTLE3
                    | LITTLE4
                    | LITTLE5
                    | LITTLE6
                    | LITTLE7
                    | LITTLE8
                    | LITTLE9'''
    p[0] = LittleDigit(p[1])

#def p_formal_comment(p):
#    'formal_comment : IDENT LFORMALCOMMENT IDENT RFORMALCOMMENT'

def p_tupleterm(p):
    'tupleterm : LOWER msetterm_list HIGHER'
    p[0] = Tupleterm(p[2])

def p_msetterm_list(p):
    '''msetterm_list : msetterm_list COMMA msetterm
                    | msetterm'''
    p[0] = MsettermList()
    if len(p) > 2:
        p[0].add_list(p[1])
        p[0].add_elt(p[3])
    else:
        p[0].add_elt(p[1])

def p_msetterm(p):
    'msetterm : xorterm_list'
    p[0] = Msetterm(p[1])

def p_xorterm_list(p):
    '''xorterm_list : xorterm_list PLUS xorterm
                    | xorterm'''
    p[0] = XortermList()
    if len(p) > 2:
        p[0].add_list(p[1])
        p[0].add_elt(p[3])
    else:
        p[0].add_elt(p[1])

def p_xorterm(p):
    'xorterm : multterm_list'
    p[0] = Xorterm(p[1])

def p_multterm_list(p):
    '''multterm_list : multterm_list OPXOR multterm
                    | multterm_list XORSYMBOL multterm
                    | multterm'''
    p[0] = MulttermList()
    if len(p) > 2:
        p[0].add_list(p[1])
        p[0].add_elt(p[3])
    else:
        p[0].add_elt(p[1])

def p_multterm(p):
    'multterm : expterm_list'
    p[0] = Multterm(p[1])

def p_expterm_list(p):
    '''expterm_list : expterm_list MULTIPLY expterm
                    | expterm'''
    p[0] = ExptermList()
    if len(p) > 2:
        p[0].add_list(p[1])
        p[0].add_elt(p[3])
    else:
        p[0].add_elt(p[1])

def p_expterm(p):
    'expterm : term_list'
    p[0] = Expterm(p[1])

def p_term_list(p):
    '''term_list : term_list EXPONENTIAL term
                    | term'''
    p[0] = TermList()
    if len(p) > 2:
        p[0].add_list(p[1])
        p[0].add_elt(p[3])
    else:
        p[0].add_elt(p[1])

def p_term(p):
    '''term : tupleterm
            | LPAREN msetterm_list RPAREN
            | nullary_fun
            | binary_app
            | nary_app
            | literal'''
    if len(p) > 2:
        p[0] = Term(p[2], lst=True)
    else:
        p[0] = Term(p[1])


def p_nullary_fun(p):
    'nullary_fun : IDENT'
    p[0] = NullaryFun(p[1])

def p_binary_app(p):
    'binary_app : binary_fun LBRACE msetterm_list RBRACE term'
    p[0] = BinaryApp(p[1], p[3], p[5])

def p_binary_fun(p):
    'binary_fun : IDENT'
    p[0] = BinaryFun(p[1])

def p_nary_app(p):
    '''nary_app : nary_fun LPAREN RPAREN
                | nary_fun LPAREN msetterm_list RPAREN'''
    if len(p) > 4:
        p[0] = NaryApp(p[1], termlist=p[3])
    else:
        p[0] = NaryApp(p[1])

def p_nary_fun(p):
    'nary_fun : IDENT'
    p[0] = NaryFun(p[1])

def p_literal_1(p):
    '''literal : LITERAL'''
    p[0] = Literal(p[1])

def p_literal_2(p):
    '''literal : TILDE LITERAL'''
    p[0] = Literal(p[1]+p[2])

def p_literal_3(p):
    '''literal : nonnode_var'''
    p[0] = Literal(p[1], b=True)

def p_nonnode_var_1_1(p):
    'nonnode_var : IDENT'
    p[0] = NonnodeVar(p[1])

def p_nonnode_var_1_2(p):
    'nonnode_var : DOLLAR IDENT'
    p[0] = NonnodeVar(p[1]+p[2])

def p_nonnode_var_1_3(p):
    'nonnode_var : IDENTDOTNATURAL'
    p[0] = NonnodeVar(p[1])

def p_nonnode_var_1_4(p):
    'nonnode_var : DOLLAR IDENTDOTNATURAL'
    p[0] = NonnodeVar(p[1]+p[2])

def p_nonnode_var_1_5(p):
    'nonnode_var : DOLLAR NATURAL'
    p[0] = NonnodeVar(p[1]+p[2])

def p_nonnode_var_2_1(p):
    'nonnode_var : IDENT COLON IDENT' # Should be 'pub' or 'fresh' as ident
    p[0] = NonnodeVar(p[1]+p[2]+p[3])

def p_nonnode_var_2_2(p):
    'nonnode_var : IDENTDOTNATURAL COLON IDENT' # Should be 'pub' or 'fresh' as ident
    p[0] = NonnodeVar(p[1]+p[2]+p[3])

def p_nonnode_var_3_1(p):
    'nonnode_var : TILDE IDENT'
    p[0] = NonnodeVar(p[1]+p[2])

def p_nonnode_var_3_2(p):
    'nonnode_var : TILDE IDENTDOTNATURAL'
    p[0] = NonnodeVar(p[1]+p[2])

def p_nonnode_var_5_1(p):
    'nonnode_var : msg_var'
    p[0] = NonnodeVar(p[1], b=True)

def p_nonnode_var_6(p):
    'nonnode_var : NATURAL' # Test this
    p[0] = NonnodeVar(p[1])

def p_facts_1(p):
    '''facts : facts COMMA fact'''
    p[0] = Facts()
    p[0].add_list(p[1])
    p[0].add_elt(p[3])

def p_facts_2(p):
    '''facts : fact
            | empty'''
    p[0] = Facts()
    p[0].add_elt(p[1])

def p_empty(p):
    'empty : '
    p[0] = Empty()

def p_fact_1(p):
    'fact : IDENT LPAREN RPAREN'
    p[0] = Fact1(p[1] + p[2] + p[3])

def p_fact_2(p):
    'fact : BANG IDENT LPAREN RPAREN'
    p[0] = Fact1(p[1] + p[2] + p[3] + p[4])

def p_fact_3(p):
    'fact : IDENT LPAREN msetterm_list RPAREN'
    p[0] = Fact2(p[1], p[3])

def p_fact_4(p):
    'fact : BANG IDENT LPAREN msetterm_list RPAREN'
    p[0] = Fact3(p[2], p[4])

def p_fact_5(p):
    'fact : IDENT LPAREN RPAREN fact_annotes'
    p[0] = Fact4(p[1], p[4])

def p_fact_6(p):
    'fact : BANG IDENT LPAREN RPAREN fact_annotes'
    p[0] = Fact5(p[2], p[5])

def p_fact_7(p):
    'fact : IDENT LPAREN msetterm_list RPAREN fact_annotes'
    p[0] = Fact6(p[1], p[3], p[5])

def p_fact_8(p):
    'fact : BANG IDENT LPAREN msetterm_list RPAREN fact_annotes'
    p[0] = Fact7(p[2], p[4], p[6])

def p_fact_annotes(p):
    'fact_annotes : LBRACKET fact_annote_list RBRACKET'
    p[0] = FactAnnotes(p[2])

def p_fact_annote_list(p):
    '''fact_annote_list : fact_annote_list COMMA fact_annote
                        | fact_annote'''
    p[0] = FactAnnoteList()
    if len(p) > 2:
        p[0].add_list(p[1])
        p[0].add_elt(p[3])
    else:
        p[0].add_elt(p[1])

def p_fact_annote(p):
    '''fact_annote : PLUS
                    | MINUS
                    | KWDNOPRECOMP'''
    p[0] = FactAnnote(p[1])

def p_formula_start(p):
    'formula_start : DOUBLEQUOTE'
    p.lexer.begin("formula")
    p[0] = FormulaStart()

def p_formula_end(p):
    'formula_end : DOUBLEQUOTE'
    p.lexer.begin("INITIAL")
    p[0] = FormulaEnd()

def p_formula_1(p):
    'formula : imp'
    p[0] = Formula1(p[1])

def p_formula_2(p):
    'formula : imp EQUIVALENT imp'
    p[0] = Formula2(p[1], p[2], p[3])

def p_formula_3(p):
    'formula : imp UNIEQUIVALENT imp'
    p[0] = Formula2(p[1], p[2], p[3])

def p_imp_1(p):
    'imp : disjunction'
    p[0] = Imp1(p[1])

def p_imp_2(p):
    'imp : disjunction IMPLY imp'
    p[0] = Imp2(p[1], p[2], p[3])

def p_imp_3(p):
    'imp : disjunction UNIIMPLY imp'
    p[0] = Imp2(p[1], p[2], p[3])

def p_imp_4(p):
    'imp : disjunction IMPLY IDENT' # Catch "==> F/T"
    p[0] = Imp3(p[1], p[2], p[3])

def p_disjunction(p):
    '''disjunction : disjunction DISJUNCTION conjunction
                | disjunction UNIDISJUNCTION conjunction
                | conjunction'''
    p[0] = Disjunction(p[1])
    if len(p) > 2:
        p[0].set_symbol(p[2])
        p[0].set_elt2(p[3])

def p_conjunction(p):
    '''conjunction : conjunction CONJUNCTION negation
                | conjunction UNICONJUNCTION negation
                | negation'''
    p[0] = Conjunction(p[1])
    if len(p) > 2:
        p[0].set_symbol(p[2])
        p[0].set_elt2(p[3])

def p_negation_1(p):
    '''negation : atom'''
    p[0] = Negation1(p[1])

def p_negation_2(p):
    '''negation : KWDNOT atom
                | UNINOT atom'''
    p[0] = Negation2(p[2], p[1])

def p_negation_3(p):
    '''negation : KWDNOT IDENT
                | UNINOT IDENT'''
    p[0] = Negation3(p[2], p[1])

def p_negation_4(p):
    '''negation : KWDNOT LPAREN IDENT RPAREN
                | UNINOT LPAREN IDENT RPAREN'''
    p[0] = Negation4(p[3], p[1])

def p_atom_1(p):
    '''atom : UNIFALSE
           | UNITRUE
           | IDENT
           | NATURAL'''
    p[0] = Atom1(p[1])
# IDENT :  # Note sure about potential side effects of this, it is used to catch "T" and "F" without defining them as tokens
# NATURAL : # Some people use naturals as function arguments...

def p_atom_2(p):
    '''atom : quant_formula'''
    p[0] = Atom2(p[1])

def p_atom_3(p):
    '''atom : LPAREN formula RPAREN
            | KWDLAST LPAREN node_var RPAREN'''
    if len(p) > 4:
        p[0] = Atom3(p[3], last=True)
    else:
        p[0] = Atom3(p[2])

def p_atom_4(p):
    '''atom : fact AROBA node_var
           | node_var LOWER node_var
           | msetterm EQUAL msetterm
           | node_var EQUAL node_var'''
    p[0] = Atom4(p[1], p[2], p[3])

def p_quant_formula(p):
    '''quant_formula : quantifier lvar_list DOT formula'''
    p[0] = QuantFormula(p[1], p[2], p[4])

def p_lvar_list(p):
    '''lvar_list : lvar_list lvar
              | lvar'''
    p[0] = LvarList()
    if len(p) > 2:
        p[0].add_list(p[1])
        p[0].add_elt(p[2])
    else:
        p[0].add_elt(p[1])

def p_lvar(p):
    '''lvar : nonnode_var
            | node_var'''
    p[0] = Lvar(p[1])

def p_quantifier(p):
    '''quantifier : KWDEXISTS
                 | UNIEXISTS
                 | KWDFORALL
                 | UNIFORALL'''
    p[0] = Quantifier(p[1])

def p_tactic_1(p):
    'tactic : tactic_hdr tactic_content'
    p[0] = Tactic(p[1], p[2])

def p_tactic_2(p):
    'tactic : tactic_hdr presort tactic_content'
    p[0] = Tactic(p[1], p[3])
    p[0].set_presort(p[2])

def p_tactic_hdr(p):
    'tactic_hdr : KWDTACTIC COLON IDENT'
    p[0] = TacticHdr(p[3])

def p_presort(p):
    'presort : KWDPRESORT COLON standard_goal_ranking'
    p[0] = Presort(p[3])

def p_tactic_content_1(p):
    'tactic_content : prio_list'
    p[0] = TacticContent()
    p[0].set_prio_list(p[1])
    
def p_tactic_content_2(p):
    'tactic_content : deprio_list'
    p[0] = TacticContent()
    p[0].set_deprio_list(p[1])
    
def p_tactic_content_3(p):
    'tactic_content : prio_list deprio_list'
    p[0] = TacticContent()
    p[0].set_prio_list(p[1])
    p[0].set_deprio_list(p[2])

def p_prio_list(p):
    '''prio_list : prio_list prio
                | prio'''
    p[0] = PrioList()
    if len(p) > 2:
        p[0].add_list(p[1])
        p[0].add_elt(p[2])
    else:
        p[0].add_elt(p[1])

def p_deprio_list(p):
    '''deprio_list : deprio_list deprio
                   | deprio'''
    p[0] = DeprioList()
    if len(p) > 2:
        p[0].add_list(p[1])
        p[0].add_elt(p[2])
    else:
        p[0].add_elt(p[1])

def p_prio_1(p):
    'prio : KWDPRIO COLON tactic_function_list'
    p[0] = Prio(p[3])

def p_prio_2(p):
    'prio : KWDPRIO COLON LBRACE post_ranking RBRACE tactic_function_list'
    p[0] = Prio(p[6])
    p[0].set_post_ranking(p[4])

def p_deprio_1(p):
    'deprio : KWDDEPRIO COLON tactic_function_list'
    p[0] = Deprio(p[3])

def p_deprio_2(p):
    'deprio : KWDDEPRIO COLON LBRACE post_ranking RBRACE tactic_function_list'
    p[0] = Deprio(p[6])
    p[0].set_post_ranking(p[4])

def p_post_ranking(p):
    'post_ranking : IDENT'
    p[0] = PostRanking(p[1])

def p_tactic_function_list(p):
    '''tactic_function_list : tactic_function_list tactic_function
                  | tactic_function'''
    p[0] = TacticFunctionList()
    if len(p) > 2:
        p[0].add_list(p[1])
        p[0].add_elt(p[2])
    else:
        p[0].add_elt(p[1])

def p_function(p):
    'tactic_function : and_function_list'
    p[0] = Function(p[1])

def p_and_function_list(p):
    '''and_function_list : and_function_list DISJUNCTION and_function
                        | and_function'''
    p[0] = AndFunctionList()
    if len(p) > 2:
        p[0].add_list(p[1])
        p[0].add_elt(p[3])
    else:
        p[0].add_elt(p[1])

def p_and_function(p):
    '''and_function : not_function_list'''
    p[0] = AndFunction(p[1])

def p_not_function_list(p):
    '''not_function_list : not_function_list CONJUNCTION not_function
                        | not_function'''
    p[0] = NotFunctionList()
    if len(p) > 2:
        p[0].add_list(p[1])
        p[0].add_elt(p[3])
    else:
        p[0].add_elt(p[1])

def p_not_function_1(p):
    'not_function : function_and_params'
    p[0] = NotFunction(p[1])

def p_not_function_2(p):
    'not_function : KWDNOT function_and_params'
    p[0] = NotFunction(p[2], no=True)


def p_function_and_params(p):
    '''function_and_params : REGEX_STRING
                   | ISFACTNAME_STRING
                   | ISINFACTTERMS_STRING
                   | DHRENOISE_STRING
                   | DEFAULTNOISE_STRING
                   | REASONABLENONCESNOISE_STRING
                   | NONABSURDGOAL_STRING'''
    p[0] = FunctionAndParams(p[1])


    
def p_error(p):
    if p:
        print("Syntax error at token", p, "in line", p.lineno)
        # Just discard the token and tell the parser it's okay.
        s_parser.errok()
    else:
         print("Syntax error at EOF")
