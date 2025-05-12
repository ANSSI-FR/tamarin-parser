### Tamarin Parser

This repository contains the support material for the article published at Computer Security Foundations 2025.

*Formal analysis on random nonce misuse in cryptographic protocols*, G. Avoine, T. Claverie, S. Delaune.

It is composed of three main parts:
- A parser for Tamarin files, that allows recovering and rewriting the Abstract Syntax Tree of .spthy files (folder *parser*);
- Models of protocols used in the study (folder *study*);
- A server to configure the analysis and sumarizes the results for a given model (folder *server*).

The server and models are tightly linked to the original goal of the study, namely the study of random misgeneration in cryptographic protocols.
However, the Tamarin parser has been conceived to be independant of the study, so it could be repurposed for other types of analysis, from models modification to parsing of security proofs and attacks.


