import os
import shutil
import os.path
import uuid
from utils import hash_file
from db import *
import tamarinparser
from tamarinparser import ast_builder
from tamarinparser.scenarios import *


def write_scenario(s, parent, output_dir, case_name):
    result = s.generate()

    newfilename = f"{case_name}.spthy"
    output_file = os.path.join(output_dir, newfilename)
    with open(output_file, "w") as fp:
        fp.write(result)

    h = hash_file(output_file)
    u = uuid.uuid4()
    db_insert_file(u, parent, newfilename, output_file, h)

def collect_nonce_facts(theory):
    body = theory.body
    elts = []
    for c in body.children:
        if type(c.item) == ast_builder.Rule:
            rule = c.item.rule
            if type(rule) == ast_builder.SimpleRuleVariant:
                rule = rule.rule
        else:
            continue
        name = rule.header.rule_name
        pre_facts = rule.body.pre_facts
        for fact in pre_facts.children:
            if type(fact) == ast_builder.Empty:
                continue
            if fact.name == "Nonce":
                if type(fact) != ast_builder.Fact2 and type(fact) != ast_builder.Fact3:
                    print(f"Warning: Nonce fact misformed: {fact.build()} ; expected Nonce(~n)")
                elts.append((rule, fact))
    return elts

    
def create_cases(parent, theory, filename, output_dir, reuse_always, reuse_once, leak_once, leak_always, fmt):
    all_nonces = collect_nonce_facts(theory)

    basename = os.path.basename(filename)[:-6].replace("-", "")

    if fmt == "simple":

        s = SimpleBaseScenario(f"{basename}_basic", theory, collect_nonce_facts)
        write_scenario(s, parent, output_dir, f"{basename}_basic")

        if leak_once:
            for nonce_idx in range(len(all_nonces)):
                case_name = f"{basename}_leak_once_{nonce_idx}"
                s = SimpleLeakOnceScenario(case_name, theory, collect_nonce_facts, nonce_idx)
                write_scenario(s, parent, output_dir, case_name)

        if leak_always:
            for nonce_idx in range(len(all_nonces)):
                case_name = f"{basename}_leak_always_{nonce_idx}"
                s = SimpleLeakAlwaysScenario(case_name, theory, collect_nonce_facts, nonce_idx)
                write_scenario(s, parent, output_dir, case_name)

        if reuse_once:
            for nonce_idx1 in range(len(all_nonces)):
                for nonce_idx2 in range(nonce_idx1,len(all_nonces)):
                    case_name = f"{basename}_reuse_once_{nonce_idx1}_{nonce_idx2}"
                    s = SimpleReuseOnceScenario(case_name, theory, collect_nonce_facts, nonce_idx1, nonce_idx2)
                    write_scenario(s, parent, output_dir, case_name)

        if reuse_always:
            for nonce_idx in range(len(all_nonces)):
                case_name = f"{basename}_reuse_always_{nonce_idx}"
                s = SimpleReuseAlwaysScenario(case_name, theory, collect_nonce_facts, nonce_idx)
                write_scenario(s, parent, output_dir, case_name)
    elif fmt == "role":

        s = RoleBaseScenario(f"{basename}_basic", theory, collect_nonce_facts)
        write_scenario(s, parent, output_dir, f"{basename}_basic")

        if leak_once:
            for nonce_idx in range(len(all_nonces)):
                case_name = f"{basename}_leak_once_{nonce_idx}"
                s = RoleLeakOnceScenario(case_name, theory, collect_nonce_facts, nonce_idx)
                write_scenario(s, parent, output_dir, case_name)

        if leak_always:
            for nonce_idx in range(len(all_nonces)):
                case_name = f"{basename}_leak_always_{nonce_idx}"
                s = RoleLeakAlwaysScenario(case_name, theory, collect_nonce_facts, nonce_idx)
                write_scenario(s, parent, output_dir, case_name)

        if reuse_once:
            for nonce_idx1 in range(len(all_nonces)):
                for nonce_idx2 in range(nonce_idx1,len(all_nonces)):
                    if all_nonces[nonce_idx1][1].args.children[0].build() == all_nonces[nonce_idx2][1].args.children[0].build():
                        case_name = f"{basename}_reuse_once_{nonce_idx1}_{nonce_idx2}"
                        s = RoleReuseOnceScenario(case_name, theory, collect_nonce_facts, nonce_idx1, nonce_idx2)
                        write_scenario(s, parent, output_dir, case_name)

        if reuse_always:
            for nonce_idx in range(len(all_nonces)):
                case_name = f"{basename}_reuse_always_{nonce_idx}"
                s = RoleReuseAlwaysScenario(case_name, theory, collect_nonce_facts, nonce_idx)
                write_scenario(s, parent, output_dir, case_name)


def generate_submodels(uuid):
    model = db_get_basemodel_from_uuid(uuid)
    
    filepath = model.filepath
    basedir = os.path.dirname(filepath)
    generated_dir = os.path.join(basedir, "generated")
    
    if os.path.exists(generated_dir):
        shutil.rmtree(generated_dir)

    db_remove_children_files(uuid)

    os.makedirs(generated_dir)

    with open(filepath, "r") as basemodel:

        theory = tamarinparser.parse_theory(basemodel.read())
        create_cases(uuid, theory, model.orig_filename, generated_dir, model.reuse_always, model.reuse_once, model.leak_once, model.leak_always, model.format)
    
def collect_lemmas(file):
    content = ""
    with open(file, "r") as fp:
        content = fp.read()
    theory = tamarinparser.parse_theory(content)
    body = theory.body
    res = []
    for c in body.children:
        if type(c.item) == ast_builder.Lemma:
            hdr = c.item.lemma_hdr
            name = hdr.name
            quantifier = hdr.quantifier
            if quantifier is None:
                quantifier = "all-traces"
            else: 
                quantifier = quantifier.build()
            res.append((name, quantifier))
    return res
    
def clean_and_parse_result_file(file):
    content = ""
    with open(file, "r") as fp:
        content = fp.read()
        th_idx = content.index("theory")
        content = content[th_idx:]
        summary_idx = content.index("summary of summaries")
        summary = content[summary_idx:]
        lines = summary.split("\n")
        res = []
        for line in lines:
            if line.find("trace") == -1:
                continue
            split = line.strip().split(" ")
            name = split[0]
            result = split[2] == "verified"
            t = split[1][1:-2]

            res.append((name, t, result))

    # Rewrite the file, to remove the Maude header
    with open(file, "w") as fp:
        fp.write(content)

    return res
