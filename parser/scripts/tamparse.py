#!/bin/env python3
import copy
import os.path
import argparse

from tamarinparser.syntax import *
from tamarinparser.scenarios import *
from tamarinparser.tok import *
import ply.yacc as yacc

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
            if fact.name == "Random":
                if type(fact) != ast_builder.Fact2 and type(fact) != ast_builder.Fact3:
                    print(f"Warning: Random fact misformed: {fact.build()} ; expected Random(~n)")
                elts.append((rule, fact))
    return elts

def create_dir(directory):
    # Create the directory, or do nothing if it already exists
    os.makedirs(directory, exist_ok=True)

def verify_args(args):
    output_dir = args.output_dir
    filename = args.filename

    if not filename.endswith(".spthy"):
        print("Expected a Tamarin file (*.spthy)")
        quit()

    if not os.path.isfile(filename):
        print(f"File does not exists: {filename}")
        quit()

    if os.path.exists(output_dir) and not os.path.isdir(output_dir):
        print(f"{output_dir} exists and is not a directory")
        quit()

    if not (args.simple or args.role):
        print(f"Type of model not provided")
        quit()

def write_scenario(s, output_dir, case_name):
    result = s.generate()

    newfilename = f"{case_name}.spthy"
    output_file = os.path.join(output_dir, newfilename)
    print(output_file)
    with open(output_file, "w") as fp:
        fp.write(result)
    
def create_cases(theory, args, filename, output_dir):
    all_nonces = collect_nonce_facts(theory)

    basename = os.path.basename(filename)[:-6].replace("-", "")

    if args.simple:

        s = SimpleBaseScenario(f"{basename}_basic", theory, collect_nonce_facts)
        write_scenario(s, args.output_dir, f"{basename}_basic")

        if args.leak_once:
            for nonce_idx in range(len(all_nonces)):
                case_name = f"{basename}_leak_once_{nonce_idx}"
                s = SimpleLeakOnceScenario(case_name, theory, collect_nonce_facts, nonce_idx)
                write_scenario(s, args.output_dir, case_name)

        if args.leak_always:
            for nonce_idx in range(len(all_nonces)):
                case_name = f"{basename}_leak_always_{nonce_idx}"
                s = SimpleLeakAlwaysScenario(case_name, theory, collect_nonce_facts, nonce_idx)
                write_scenario(s, args.output_dir, case_name)

        if args.reuse_once:
            for nonce_idx1 in range(len(all_nonces)):
                for nonce_idx2 in range(nonce_idx1,len(all_nonces)):
                    case_name = f"{basename}_reuse_once_{nonce_idx1}_{nonce_idx2}"
                    s = SimpleReuseOnceScenario(case_name, theory, collect_nonce_facts, nonce_idx1, nonce_idx2)
                    write_scenario(s, args.output_dir, case_name)

        if args.reuse_always:
            for nonce_idx in range(len(all_nonces)):
                case_name = f"{basename}_reuse_always_{nonce_idx}"
                s = SimpleReuseAlwaysScenario(case_name, theory, collect_nonce_facts, nonce_idx)
                write_scenario(s, args.output_dir, case_name)
    elif args.role:

        s = RoleBaseScenario(f"{basename}_basic", theory, collect_nonce_facts)
        write_scenario(s, args.output_dir, f"{basename}_basic")

        if args.leak_once:
            for nonce_idx in range(len(all_nonces)):
                case_name = f"{basename}_leak_once_{nonce_idx}"
                s = RoleLeakOnceScenario(case_name, theory, collect_nonce_facts, nonce_idx)
                write_scenario(s, args.output_dir, case_name)

        if args.leak_always:
            for nonce_idx in range(len(all_nonces)):
                case_name = f"{basename}_leak_always_{nonce_idx}"
                s = RoleLeakAlwaysScenario(case_name, theory, collect_nonce_facts, nonce_idx)
                write_scenario(s, args.output_dir, case_name)

        if args.reuse_once:
            for nonce_idx1 in range(len(all_nonces)):
                for nonce_idx2 in range(nonce_idx1,len(all_nonces)):
                    if all_nonces[nonce_idx1][1].args.children[0].build() == all_nonces[nonce_idx2][1].args.children[0].build():
                        case_name = f"{basename}_reuse_once_{nonce_idx1}_{nonce_idx2}"
                        s = RoleReuseOnceScenario(case_name, theory, collect_nonce_facts, nonce_idx1, nonce_idx2)
                        write_scenario(s, args.output_dir, case_name)

        if args.reuse_always:
            for nonce_idx in range(len(all_nonces)):
                case_name = f"{basename}_reuse_always_{nonce_idx}"
                s = RoleReuseAlwaysScenario(case_name, theory, collect_nonce_facts, nonce_idx)
                write_scenario(s, args.output_dir, case_name)


def main():
    parser = argparse.ArgumentParser(prog="NMTamarin", description="Generate all random misgeneration cases")
    parser.add_argument("filename")
    parser.add_argument("output_dir")

    parser.add_argument("--simple", action="store_true")
    parser.add_argument("--role", action="store_true")
    parser.add_argument("--leak-once", action="store_true")
    parser.add_argument("--leak-always", action="store_true")
    parser.add_argument("--reuse-once", action="store_true")
    parser.add_argument("--reuse-always", action="store_true")

    args = parser.parse_args()
    verify_args(args)
    create_dir(args.output_dir)
    filename = args.filename

    parser = yacc.yacc()
    content = open(filename, "r").read()
    theory = parser.parse(content)

    create_cases(theory, args, filename, args.output_dir)

if __name__ == "__main__":
    main()
