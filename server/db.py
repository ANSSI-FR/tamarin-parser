import sqlite3
import datetime
from collections import namedtuple

Bm = namedtuple("Basemodel", ("id", "created", "uuid", "orig_filename", "filepath", "reuse_once", "reuse_always", "leak_once", "format", "leak_always"))
Option = namedtuple("Option", ("id", "name", "flags"))
File = namedtuple("File", ("id", "uuid", "parent_uuid", "name", "path", "hash"))
Job = namedtuple("Job", ("id", "model_uuid", "parent_uuid", "option_name", "run", "result_uuid"))
Result = namedtuple("Result", ("id", "uuid", "lemma_name", "type", "value")) # value = 1 means proven, value = 0 means falsified
Lemma = namedtuple("Lemma", ("id", "uuid", "name", "type", "short_name", "enabled"))

def Basemodel(_id, created, uuid, orig_filename, filepath, reuse_once, reuse_always, leak_once, _format, leak_always):
    reuse_once = (reuse_once == 1)
    reuse_always = (reuse_always == 1)
    leak_once = (leak_once == 1)
    leak_always = (leak_always == 1)
    return Bm(_id, created, uuid, orig_filename, filepath, reuse_once, reuse_always, leak_once, _format, leak_always)

def get_db_conn():
    con = sqlite3.connect("tamarin.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    return con

def init_db():
    con = get_db_conn()
    con.execute("""CREATE TABLE IF NOT EXISTS basemodel ( id INTEGER PRIMARY KEY AUTOINCREMENT, created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, uuid TEXT NOT NULL, orig_filename TEXT NOT NULL, filepath TEXT NOT NULL, reuseonce INTEGER NOT NULL DEFAULT 0, reusealways INTEGER NOT NULL DEFAULT 0, leakonce INTEGER NOT NULL DEFAULT 0, format TEXT NOT NULL, leakalways INTEGER NOT NULL DEFAULT 0)""")
    con.execute("""CREATE TABLE IF NOT EXISTS options (id INTEGER PRIMARY KEY AUTOINCREMENT, uuid TEXT NOT NULL, name TEXT NOT NULL, flags TEXT) """);
    con.execute("""CREATE TABLE IF NOT EXISTS file (id INTEGER PRIMARY KEY AUTOINCREMENT, uuid TEXT NOT NULL, parentuuid TEXT, name TEXT NOT NULL, path TEXT NOT NULL, hash TEXT NOT NULL) """);
    con.execute("""CREATE TABLE IF NOT EXISTS job (id INTEGER PRIMARY KEY AUTOINCREMENT, modeluuid TEXT NOT NULL, parentuuid TEXT, optionname TEXT, run INTEGER NOT NULL, resultuuid TEXT) """);
    con.execute("""CREATE TABLE IF NOT EXISTS result (id INTEGER PRIMARY KEY AUTOINCREMENT, uuid TEXT NOT NULL, lemmaname TEXT NOT NULL, type TEXT NOT NULL, value INTEGER NOT NULL) """);
    con.execute("""CREATE TABLE IF NOT EXISTS lemma (id INTEGER PRIMARY KEY AUTOINCREMENT, uuid TEXT NOT NULL, name TEXT NOT NULL, type TEXT NOT NULL, shortname TEXT, enabled INTEGER NOT NULL) """);
    con.commit()
    con.close()

def db_insert_lemma(uuid, name, t, short_name, enabled):
    enabled = 1 if enabled else 0
    con = get_db_conn()
    con.execute("INSERT INTO lemma (uuid, name, type, shortname, enabled) VALUES (?, ?, ?, ?, ?)", (str(uuid), name, t, short_name, enabled))
    con.commit()
    con.close()

def db_get_lemmas_from_uuid(uuid):
    con = get_db_conn()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM lemma WHERE uuid LIKE ?", (str(uuid), ))
    res = []
    for e in cursor.fetchall():
        res.append(Lemma(*e))
    con.close()
    return res

def db_update_lemma(uuid, name, short_name, enabled):
    enabled = 1 if enabled else 0
    con = get_db_conn()
    con.execute("UPDATE lemma SET shortname = ?, enabled = ? WHERE uuid LIKE ? AND name LIKE ?", (short_name, enabled, uuid, name))
    con.commit()
    con.close()

def db_create_basemodel(uuid, orig_filename, filepath):
    t = datetime.datetime.now()
    con = get_db_conn()
    con.execute("INSERT INTO basemodel (created, uuid, orig_filename, filepath, reuseonce, reusealways, leakonce, format, leakalways) VALUES (?, ?, ?, ?, 0, 0, 0, 'simple', 0)", (t, str(uuid), orig_filename, filepath))
    con.commit()
    con.close()

def db_insert_result(uuid, lemma, t, value):
    con = get_db_conn()
    value = 1 if value else 0
    con.execute("INSERT INTO result (uuid, lemmaname, type,  value) VALUES (?, ?, ?, ?)", (str(uuid), lemma, t, value))
    con.commit()
    con.close()

def db_get_result_from_uuid(uuid):
    con = get_db_conn()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM result WHERE uuid LIKE ?", (str(uuid),))
    res = []
    for e in cursor.fetchall():
        res.append(Result(*e))
    
    con.close()
    return res

def db_remove_result_from_uuid(uuid):
    con = get_db_conn()
    con.execute("DELETE FROM result WHERE uuid LIKE ?", (str(uuid),))
    con.commit()
    con.close()

def db_insert_job(model_uuid, parent_uuid, option_name, run, result_uuid):
    con = get_db_conn()
    con.execute("INSERT INTO job (modeluuid, parentuuid, optionname, run, resultuuid) VALUES (?, ?, ?, ?, ?)", (str(model_uuid), str(parent_uuid or ""), option_name, run, result_uuid))
    con.commit()
    con.close()

def db_update_job(model_uuid, parent_uuid, option_name, run, result_uuid):
    con = get_db_conn()
    con.execute("UPDATE job SET run = ?, resultuuid = ? WHERE modeluuid LIKE ? AND parentuuid LIKE ? AND optionname LIKE ?", (run, str(result_uuid), str(model_uuid), str(parent_uuid or ""), option_name))
    con.commit()
    con.close()

def db_remove_jobs_per_parent(parent_uuid):
    con = get_db_conn()
    con.execute("DELETE FROM job WHERE parentuuid LIKE ?", (str(parent_uuid),))
    con.commit()
    con.close()

def db_get_pending_jobs():
    con = get_db_conn()
    cursor = con.cursor()
    cursor.execute("SELECT j.parentuuid, j.modeluuid, j.optionname, o.flags FROM job AS j LEFT JOIN options AS o ON j.parentuuid = o.uuid AND j.optionname = o.name WHERE run = 0")
        
    res = []
    for e in cursor.fetchall():
        res.append({"parent_uuid": e[0],
                    "model_uuid": e[1],
                    "option": e[2],
                    "flags": e[3]})

    con.close()
    return res

def db_get_job(parent_uuid, model_uuid, option_name):
    con = get_db_conn()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM job WHERE parentuuid LIKE ? AND modeluuid LIKE ? AND optionname LIKE ?", (str(parent_uuid), str(model_uuid), option_name))

    res = cursor.fetchone()

    if res is None:
        return None

    con.close()
    return Job(*res)

def db_get_job_from_parent_and_option(parent_uuid, option_name):
    con = get_db_conn()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM job WHERE parentuuid LIKE ? AND optionname LIKE ?", (str(parent_uuid), option_name))

    res = []
    for e in cursor.fetchall():
        res.append(Job(*e))

    con.close()
    return res

def db_insert_file(uuid, parentuuid, name, path, h):
    con = get_db_conn()
    con.execute("INSERT INTO file (uuid, parentuuid, name, path, hash) VALUES (?, ?, ?, ?, ?)", (str(uuid), str(parentuuid or ""), name, path, h))
    con.commit()
    con.close()

def db_remove_children_files(parentuuid):
    con = get_db_conn()
    con.execute("DELETE FROM file WHERE parentuuid LIKE ?", (str(parentuuid),))
    con.commit()
    con.close()

def db_remove_file_from_uuid(uuid):
    con = get_db_conn()
    con.execute("DELETE FROM file WHERE uuid LIKE ?", (str(uuid),))
    con.commit()
    con.close()

def db_get_children_files_from_parent(parentuuid):
    con = get_db_conn()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM file WHERE parentuuid LIKE ?", (str(parentuuid),))
    res = []
    for e in cursor.fetchall():
        res.append(File(*e))

    con.close()

    return res

def db_get_file_from_uuid(uuid):
    con = get_db_conn()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM file WHERE uuid LIKE ?", (str(uuid),))
    res = cursor.fetchone()
    if res is not None:
        res = File(*res)

    con.close()

    return res

def db_get_basemodels():
    con = get_db_conn()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM basemodel")
    res = []
    for i in cursor.fetchall():
        res.append(Basemodel(*i))
    con.close()
    return res

def db_get_basemodel_from_uuid(uuid):
    con = get_db_conn()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM basemodel WHERE uuid LIKE ?", (uuid,))
    res = cursor.fetchone()
    if res is not None:
        res = Basemodel(*res)

    con.close()
    return res

def db_update_basemodel(uuid, reuse_once, reuse_always, leak_once, leak_always, _format):
    r = {False: 0, True: 1}
    reuse_once = r[reuse_once]
    reuse_always = r[reuse_always]
    leak_once = r[leak_once]
    leak_always = r[leak_always]

    con = get_db_conn()
    con.execute("UPDATE basemodel SET reuseonce = ?, reusealways = ?, leakonce = ?, leakalways = ?, format = ? WHERE uuid LIKE ?", (reuse_once, reuse_always, leak_once, leak_always, _format, uuid))
    con.commit()
    con.close()

def db_update_options(uuid, options):
    con = get_db_conn()
    con.execute("DELETE FROM options WHERE uuid LIKE ?", (str(uuid),))
    for o in options:
        con.execute("INSERT INTO options (uuid, name, flags) VALUES (?, ?, ?)", (str(uuid), o[0], o[1]))
    con.commit()
    con.close()

def db_get_options_from_uuid(uuid):
    con = get_db_conn()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM options WHERE uuid LIKE ?", (str(uuid),))
    resp = []
    for elt in cursor.fetchall():
        resp.append(Option(elt[0], elt[2], elt[3]))
    con.close()
    return resp

