import os

def get_cases(folder, needle):
    res = []
    a = list(os.walk(folder))
    for e in a[0][2]:
        if needle in e:
            res.append(os.path.join(folder,e))
    return res

def print_header(size=15):
    return """\\documentclass[crop]{standalone}
\\usepackage{utfsym}
\\usepackage{caption}

\\definecolor{ForestGreen}{RGB}{34,139,34}
\\newcommand{\\noattack}{\\color{ForestGreen}\\usym{2713}\\color{black}}
\\newcommand{\\attack}{\\color{red}\\usym{2717}\\color{black}}

\\begin{document}\n""" + "\\parbox{" + f"{size}" + "cm}{\n"

def print_caption(caption):
    return f"\\captionof{{table}}{{ {caption} }}\n"

def print_table_header(lemmas):
    start = "\\begin{tabular}{|c|c|"
    start += "c|" * len(lemmas) + "}\n"
    start += "\\hline\n"
    start += "Case & Nonce"
    for l in lemmas: 
        start += " & " + l
    start += " \\\\ \\hline\n"
    return start

def print_footer():
    return "\\end{tabular}}\n\\end{document}"

def get_result(e, lemmas):
    with open(e, "r") as fp:
        lines = fp.readlines()

    res = {}

    for line in lines:
        for lemma in lemmas:
            if line.startswith("  "+lemma):
                if "verified" in line:
                    res[lemma] = True
                elif "falsified" in line:
                    res[lemma] = False

    return res

def get_raw_results(files, lemmas):
    all_results = {}
    for p in files:
        r = get_result(p, lemmas)
        all_results[p] = r
    return all_results

def process_raw_results(all_results, lemmas, nonces):
    all_keys = list(all_results.keys())
    all_keys.sort()

    res = []
    for key in all_keys:
        if "basic" in key:
            elt1 = "No misgeneration"
            elt2 = "N/A"
        if "reuse_once" in key:
            elt1 = "Reuse Once"
            idx = key.index("reuse_once")
            n1 = f"N{key[idx+11]}"
            n2 = f"N{key[idx+13]}"
            elt2 = f"{nonces[n1]} = {nonces[n2]}"
        if "reuse_always" in key:
            elt1 = "Reuse Always"
            idx = key.index("reuse_always")
            n1 = f"N{key[idx+13]}"
            elt2 = f"{nonces[n1]}"
        if "leak_always" in key:
            elt1 = "Leak Always"
            idx = key.index("leak_always")
            n1 = f"N{key[idx+12]}"
            elt2 = f"{nonces[n1]}"

        start = elt1 + " & " + elt2
        for lemma in lemmas:
            if all_results[key][lemma]: # True means lemma is verified so there is no attack
                start += " & " + "\\noattack"
            else:
                start += " & " + "\\attack"

        res.append(start)
    return res


def get_results(files, lemmas, nonces):
    all_results = {}
    for p in files:
        r = get_result(p, lemmas)
        all_results[p] = r

    all_keys = list(all_results.keys())
    all_keys.sort()

    res = []
    for key in all_keys:
        if "basic" in key:
            elt1 = "No misgeneration"
            elt2 = "N/A"
        if "reuse_once" in key:
            elt1 = "Reuse Once"
            idx = key.index("reuse_once")
            n1 = f"N{key[idx+11]}"
            n2 = f"N{key[idx+13]}"
            elt2 = f"{nonces[n1]} = {nonces[n2]}"
        if "reuse_always" in key:
            elt1 = "Reuse Always"
            idx = key.index("reuse_always")
            n1 = f"N{key[idx+13]}"
            elt2 = f"{nonces[n1]}"
        if "leak_always" in key:
            elt1 = "Leak Always"
            idx = key.index("leak_always")
            n1 = f"N{key[idx+12]}"
            elt2 = f"{nonces[n1]}"

        start = elt1 + " & " + elt2
        for lemma in lemmas:
            if all_results[key][lemma]: # True means lemma is verified so there is no attack
                start += " & " + "\\noattack"
            else:
                start += " & " + "\\attack"

        res.append(start)
    return res

def create_table(caption, lemmas, lemma_names, folder, needle, out_file, nonces, size=15):
    fp = open(out_file, "w")
    all_results_file = get_cases(folder, needle)
    fp.write(print_header(size))
    fp.write(print_caption(caption))
    fp.write(print_table_header(lemma_names))
    for r in get_results(all_results_file, lemmas, nonces):
        fp.write(r)
        fp.write("\\\\ \\hline\n")

    fp.write(print_footer())
    fp.close()
