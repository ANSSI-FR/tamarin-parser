## Web server

This web server can be used to upload, configure, generate and display Tamarin models and their results.

It relies on the Flask framework and SQLite3 database.
Python packages for flask and SQLite3 can be installed with `pip install -r -requirements.txt --user`
It also requires the package tamarinparser to be installed, as it uses it internally to modify models.

Once the requirements have been fulfilled, run the development server with `python app.py`.

It will automatically create a database `tamarin.db` and a resources directory `resources/`.

A stripped down (i.e., read-only) version of this server is deployed at [https://tamarinnonces.com](https://tamarinnonces.com), with the models and results presented.

### HTTP routes

The server relies on a set of routes to work.

- `/` or `/list`: used to show the list of templates known to the server
- `/upload`: used to upload a Tamarin template to the server
- `/{uuid}/configure`: used to modify the misuse cases to generate, and the options of the models. An option is the association between an option name and a set of macros to enable for the analysis. For example, in WPA2 the analysis is performed using the Macro FreshKey, that enables whether or not the PSK of the Four-Way handshake changes with each session or not.
- `/{uuid}/runner`: displays the status of all lemmas, for all misuse cases
- `/{uuid}/result`: used to upload a result file for a model to the server
- `/{uuid}/file`: retrieves the file identified by this UUID
- `/{uuid}/lemma`: used to configure the display of lemmas. Because Tamarin lemmas may not be all useful for an analysis, or are usually encoded with long names, this allows to select the lemma's results displayed as well as to give them a short handle.
- `/{uuid}/table`: results table
- `/api/pending`: list of models that have yet to run

Overall, when working with the development server, the workflow is as follows:

1. Go to `/upload` to upload a Tamarin template. It redirects to the configuration page of that template.
2. Configure the template, i.e., select which misuse cases are to be generated, which options to use, etc.
3. Run the script `run_models.py` from the script folder. It fetches the job list from the API of a to-be-defined server (http://127.0.0.1:5000/ by default), runs tamarin-prover on them, and uploads the results to the server.
4. Progress can be seen by going to the root of the server, and clicking on the table icon
