### TamarinParser

This project parses Tamarin source files (.spthy) and recovers the Abstract Syntax Tree in Python.
It is possible to use this library to automatically modify the AST of a model and to write a new model, using the modified AST.

This way, it is possible to apply modifications at scale on Tamarin models.
The library is used to apply pre-defined transformations on models in order to study the required properties of nonces in protocols.

Under the hood, the project [ply](https://ply.readthedocs.io/en/latest/) is used to implement the parsing algorithm, based on the grammar defined.

### Installation

Installation of the package cannot be done using the usual `setup.py install` method.
This is because ply needs to be able to read and write the file `parsetab.py`.
However, by default a Python package is transformed into an archive, and its content cannot be accessed like a usual file on the system

- Install the ply PyPi package using pip: `pip install -r requirements.txt --user`
- Create a .tar.gz of the package: `python setup.py sdist`
- Install the .tar.gz: `pip install --user ./dist/tamarinparser-0.0.1.tar.gz`

### Getting started

Because this project relies heavily on the Tamarin ecosystem, some degree of familiarity is expected with the Tamarin Prover.

If the package is correctly installed, it can be accessed as a regular Python package, using `import tamarinparser`
The script `tamparse.py` is also present and should be installed in your $PATH.

To verify the installation has completed correctly, there are two toy protocols in the test/ directory.
It is possible to generate all possible misuse cases for each of these protocols with the following command lines:

```
tamparse.py --simple test/test_simple.spthy examples/simple --leak-once --leak-always --reuse-once --reuse-always
tamparse.py --role test/test_role.spthy examples/role --leak-once --leak-always --reuse-once --reuse-always
```

These commands would generate all misuse cases for model test\_simple.spthy in the directory ./examples/simple, and all misuse cases for model test\_role.spthy in the directory ./examples/role.

#### Nonce misuse

The script tamparse implements a wrapper around functions that modify the AST to automatically generate all nonce misuses cases.
Although the study has been performed on a set of models, it is possible to use the tool on other models, to study nonce misuse, without modification.

Essentially, one can replace all nonce generation facts from Fr(XX) to Random(XX), then run the published tool, and the resulting models can be checked analyzed with Tamarin.

Two types of modeling are available: simple and role.
In a "simple" model setup, the tool will create all cases of reuse, between all pair of nonces.
However, some of these cases may not be very practical (depending on the studied context).
For example, on an example protocol with two agents A and B and two nonces Na and Nb, one of the models generated would assume that A generates Na correctly, and B generates the same value as A.
This is the goal of the "role" modeling possibility.
In this model, a nonce is written as Random('XX', YY), with XX the name of the role.
With this kind of models, the tool would only generate nonce reuse inside the same role.

This choice mostly impacts the number of models generated, which may be relevant for complex protocols with several roles and nonces.

Aside from these considerations, the tool parses all rules, identify the "Random" fact being used and numbers them.
Then, it creates the correct rules to instantiate the "RandomX" facts from "Fr" facts, taking into account the exact misuse case being considered.

#### \_basic.spthy

The examples that have the suffix "\_basic" are the legitimate case, when there are no nonces misused.
In these examples, all nonces are correctly generated using Fr() facts.

#### \_reuse\_once\_X\_Y.spthy

The examples that contain "reuse\_once" in the filename assume that the pair of nonces <X, Y> is being reused once.
This means that the model will allow the generation of a fresh value such that RandomX == RandomY for one time.

This matches the case where the PRNG has a low entropy or is being wrongly initialized, and nonces have a high chance of being reused.

#### \_reuse\_always\_X.spthy

The examples that contain "reuse\_always" in the filename assume that the nonce X is always being reused.
This matches the case where the nonce is a constant.
Note that in this scenario, the nonce is a priori unknown to the attacker.

#### \_leak\_once\_X.spthy

Examples that contain "leak\_once" in their name consider that nonce X is being leaked before it is being used, but only once.

This matches the case where an attacker has managed to predict the nonce that an implementation will generate.

#### \_leak\_always\_X.spthy

Examples that contain "leak\_always" in their name consider that nonce X is always leaked before it is being used.
This matches the case where an attacker is always able to predict the nonce that an implementation will generate, for example because it is able to recover the state of a PRNG when a protocol starts.

### Tamarin Parser

Most lines of code are used to implement a parser of Tamarin files.
The most relevant source to implement such a parser are the documentation of Tamarin, where a chapter is dedicated to its syntax.
Then, one has to go through the source code of Tamarin to retrieve the syntax that is actually implemented by the tool.

Basically, there are three core elements to the parser:

- The list of tokens of the language, it is implemented in file tok.py
- The list of grammar rules, it is implemented in file syntax.py
- The Python classes that back each rule, so the AST can be manipulated in Python. They are implemented in file ast\_builder.py

Then, the file scenarios.py contains the rewrite scenarios implemented.
The file parsetab.py is automatically generated by ply from the rules and tokens.
