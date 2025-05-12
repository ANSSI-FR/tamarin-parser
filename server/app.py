import argparse
import string
import uuid
import os
from flask import Flask, render_template, request, abort, send_file, redirect
from werkzeug.utils import secure_filename
from db import *
from model import generate_submodels, clean_and_parse_result_file, collect_lemmas
from utils import *
import json

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(f"/list")

@app.route("/api/pending", methods=["GET"])
def pending_jobs():
    jobs = db_get_pending_jobs()
    return json.dumps(jobs)

def verify_filename(name):
    if not name.endswith(".spthy"):
        return False

    alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + "-_."
    if not set(name).issubset(set(alphabet)):
        print(name)
        return False

    return True

@app.route('/<string:uuid>/table', methods=['GET'])
def show_table(uuid):
    model = db_get_basemodel_from_uuid(uuid)
    options = db_get_options_from_uuid(uuid)
    lemmas = db_get_lemmas_from_uuid(uuid)
    trad_lemmas = {l.name: l.short_name for l in lemmas if l.enabled}

    res = {"name": model.orig_filename, "options": []}
    for option in options:
        d = {"option": option.name, "submodels": []}
        
        jobs = db_get_job_from_parent_and_option(uuid, option.name)
        print(jobs)
        for job in jobs:
            submodel_file = db_get_file_from_uuid(job.model_uuid)
            orig_filename = submodel_file.name
            print(orig_filename)
            if orig_filename.endswith("basic.spthy"):
                misuse_type = "No misuse"
                misuse_nonce = "N/A"
            elif orig_filename.find("reuse_always") >= 0:
                misuse_type = "Reuse always"
                n1 = orig_filename[:-6].split("_")[-1]
                misuse_nonce = f"N{n1}"
            elif orig_filename.find("reuse_once") >= 0:
                misuse_type = "Reuse once"
                n1, n2 = orig_filename[:-6].split("_")[-2:]
                misuse_nonce = f"N{n1} = N{n2}"
            elif orig_filename.find("leak_once") >= 0:
                misuse_type = "Leak once"
                n1 = orig_filename[:-6].split("_")[-1]
                misuse_nonce = f"N{n1}"
            elif orig_filename.find("leak_always") >= 0:
                misuse_type = "Leak always"
                n1 = orig_filename[:-6].split("_")[-1]
                misuse_nonce = f"N{n1}"

            
            i = {"model_uuid": job.model_uuid, "model_filepath": submodel_file.name, "misuse_type": misuse_type, "misused_nonce": misuse_nonce}

            if job.result_uuid != "":
                results_file = db_get_file_from_uuid(job.result_uuid)
                i["results_uuid"] = results_file.uuid
                i["results_filepath"] = results_file.name

                results = db_get_result_from_uuid(results_file.uuid)
                filtered_results = []
                for r in results:
                    if r.lemma_name in trad_lemmas:
                        if trad_lemmas[r.lemma_name] != "":
                            newresult = Result(r.id, r.uuid, trad_lemmas[r.lemma_name], r.type, r.value)
                            filtered_results.append(newresult)
                        else:
                            filtered_results.append(r)
                i["results"] = filtered_results
            else:
                i["results_uuid"] = ""
                i["results_filepath"] = ""
                i["results"] = []
            d["submodels"].append(i)
        res["options"].append(d)

    if model is None:
        abort(404, f"Basemodel {uuid} has not been found")

    return render_template("table.html", model=model, data=res, lemmas=lemmas)


@app.route('/<string:uuid>/lemma', methods=['GET'])
def show_lemmas(uuid):
    model = db_get_basemodel_from_uuid(uuid)
    lemmas = db_get_lemmas_from_uuid(uuid)
    return render_template("lemma.html", model=model, lemmas=lemmas)

@app.route('/<string:uuid>/lemma', methods=['POST'])
def update_lemmas(uuid):
    model = db_get_basemodel_from_uuid(uuid)

    i = 1
    while True:
        if not f"name{i}" in request.form:
            break
        if not f"shortname{i}" in request.form:
            abort(500, "Invalid form values")
        i += 1
    
    nb_lemmas = i

    for i in range(1,nb_lemmas):
        name = request.form[f"name{i}"]
        shortname = request.form[f"shortname{i}"]
        enabled = f"enabled{i}" in request.form
        db_update_lemma(uuid, name, shortname, enabled)

    lemmas = db_get_lemmas_from_uuid(uuid)
    return render_template("lemma.html", model=model, lemmas=lemmas)

@app.route('/<string:uuid>/file', methods=['GET'])
def file_download(uuid):
    file = db_get_file_from_uuid(uuid)
    if file is None:
        abort(404, f"File {uuid} has not been found")

    return send_file(file.path, download_name=file.name)

@app.route('/<string:uuid>/configure', methods=['GET'])
def configure(uuid):
    model = db_get_basemodel_from_uuid(uuid)
    options = db_get_options_from_uuid(uuid)
    files = db_get_children_files_from_parent(uuid)
    if model is None:
        abort(404, f"Basemodel {uuid} has not been found")

    return render_template("protocol.html", model=model, options=options, files=files)

@app.route('/result', methods=['GET'])
def result():
    basemodels = db_get_basemodels()

    res = []
    for bm in basemodels:
        o = {"uuid": bm.uuid, "name": bm.orig_filename}
        subs = []        
        submodels = db_get_children_files_from_parent(bm.uuid)
        for model in submodels:
            subs.append({"uuid": model.uuid, "name": model.name})
        o["models"] = subs
        options = db_get_options_from_uuid(bm.uuid)

        opts = []
        for opt in options:
            opts.append(opt.name)
        o["options"] = opts

        res.append(o)

    return render_template("result.html", data=res)

@app.route('/result', methods=['POST'])
def handle_result():

    if "submodel" not in request.form or "model" not in request.form or "option" not in request.form:
        abort(500, "Invalid parameters")

    if 'file' not in request.files:
        abort(500, "Expected a result file")

    model_uuid = request.form["model"]
    submodel_uuid = request.form["submodel"]
    option_name = request.form["option"]

    job = db_get_job(model_uuid, submodel_uuid, option_name)
    if job is None:
        abort(500, "This set of parameters does not match any known configuration to study")

    # A result already exists, remove it
    if job.result_uuid != "":
        f = db_get_file_from_uuid(job.result_uuid)
        os.remove(f.path)
        db_remove_file_from_uuid(job.result_uuid)

    file = request.files['file']

    basedir = f"resources/{model_uuid}/results"
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    u = uuid.uuid4()
    out_filename = f"{basedir}/{u}.spthy"
    file.save(out_filename)

    h = hash_file(out_filename)

    parent_file = db_get_file_from_uuid(submodel_uuid)
    results_filename =  parent_file.name.replace(".spthy", "_results.spthy")

    db_insert_file(u, model_uuid, results_filename, out_filename, h)

    db_update_job(submodel_uuid, model_uuid, option_name, 1, u)
    parsed = clean_and_parse_result_file(out_filename)
    for result in parsed:
        db_insert_result(u, result[0], result[1], result[2])

    return redirect(f"/{u}/result")

@app.route('/<string:uuid>/result', methods=['GET'])
def display_result(uuid):

    file = db_get_file_from_uuid(uuid)
    
    results = db_get_result_from_uuid(uuid)

    return render_template("display_result.html", file=file, lemmas=results)

@app.route('/<string:uuid>/configure', methods=['POST'])
def configure_model(uuid):
    model = db_get_basemodel_from_uuid(uuid)
    if model is None:
        abort(404, f"Basemodel {uuid} has not been found")

    if "nonceFormat" not in request.form or request.form["nonceFormat"] not in ["simple", "role"]:
        abort(500, f"Nonce format must be Simple or Role")

    nonce_format = request.form["nonceFormat"]

    reuse_once = ("ReuseOnce" in request.form)
    reuse_always = ("ReuseAlways" in request.form)
    leak_once = ("LeakOnce" in request.form)
    leak_always = ("LeakAlways" in request.form)

    nb_options = len(request.form) - 4

    options = parse_options(request.form, nb_options)
    print(options)
    if options is None:
        abort(500, "Invalid form values")

    print(nb_options)
    if len(options) < 1:
        options = [("Standard", "")]

    # Update the model and options
    db_update_basemodel(uuid, reuse_once, reuse_always, leak_once, leak_always, nonce_format)
    db_update_options(uuid, options)

    # Generate the file entries
    generate_submodels(uuid)

    submodels = db_get_children_files_from_parent(uuid)
    db_remove_jobs_per_parent(uuid)
    for option in options:
        for submodel in submodels:
            db_insert_job(submodel.uuid, submodel.parent_uuid, option[0], 0, "")

    return configure(uuid)

@app.route('/<string:uuid>/runner', methods=['GET'])
def runner(uuid):
    model = db_get_basemodel_from_uuid(uuid)
    options = db_get_options_from_uuid(uuid)
    lemmas = db_get_lemmas_from_uuid(uuid)
    trad_lemmas = {l.name: l.short_name for l in lemmas if l.enabled}

    res = []
    for option in options:
        d = {"option": option.name, "flags": option.flags, "submodels": []}
        
        jobs = db_get_job_from_parent_and_option(uuid, option.name)
        for job in jobs:
            submodel_file = db_get_file_from_uuid(job.model_uuid)
            i = {"model_uuid": job.model_uuid, "model_filepath": submodel_file.name}

            if job.result_uuid != "":
                results_file = db_get_file_from_uuid(job.result_uuid)
                i["results_uuid"] = results_file.uuid
                i["results_filepath"] = results_file.name

                results = db_get_result_from_uuid(results_file.uuid)
                filtered_results = []
                for r in results:
                    if r.lemma_name in trad_lemmas:
                        if trad_lemmas[r.lemma_name] != "":
                            newresult = Result(r.id, r.uuid, trad_lemmas[r.lemma_name], r.type, r.value)
                            filtered_results.append(newresult)
                        else:
                            filtered_results.append(r)
                i["results"] = filtered_results
            else:
                i["results_uuid"] = ""
                i["results_filepath"] = ""
                i["results"] = []
            d["submodels"].append(i)
        res.append(d)

    if model is None:
        abort(404, f"Basemodel {uuid} has not been found")

    return render_template("runner.html", model=model, data=res, lemmas=lemmas)

def parse_options(form, nb):
    res = []
    alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + "_"

    m = nb//2
    for i in range(m):
        if f"name{i}" not in form or f"macro{i}" not in form:
            return None

        name = form[f"name{i}"]
        macro = form[f"macro{i}"]
        if not set(name).issubset(set(alphabet)):
            return None
        if not set(macro).issubset(set(alphabet+",")):
            return None

        res.append((name, macro))
    return res

@app.route('/upload', methods=['GET'])
def upload():
    return render_template("upload.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']

        if not verify_filename(file.filename):
            return "Filename should be ([a-zA-Z0-9-_.]*).spthy"

        u = uuid.uuid4()
        basedir = f"resources/{u}"
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        out_filename = f"{basedir}/basemodel.spthy"
        file.save(out_filename)

        h = hash_file(out_filename)

        db_create_basemodel(u, file.filename, out_filename)
        db_insert_file(u, None, file.filename, out_filename, h)

        db_update_options(u, [("Standard", "")])
        insert_lemmas(u, out_filename)

        return redirect(f"/{u}/configure")

@app.route("/list", methods=['GET'])
def list_basemodels():
    models = db_get_basemodels()[::-1] # Sort from most recent to less recent
    return render_template("list_basemodels.html", models=models)

def insert_lemmas(model, filename):
    all_lemmas = collect_lemmas(filename)
    for lemma in all_lemmas:
        db_insert_lemma(model, lemma[0], lemma[1], "", True)

if __name__ == '__main__':
    os.makedirs("resources", exist_ok=True)
    init_db()

    parser = argparse.ArgumentParser(prog="TamarinDisplay", description="Configure models, display Tamarin results for nonce misuse")

    parser.add_argument("--port", default = 5000)
    parser.add_argument("--host", default="127.0.0.1")

    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=False)
