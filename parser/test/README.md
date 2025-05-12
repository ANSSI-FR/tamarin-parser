#### Content

This directory contains three files to confirm installation has processed correctly:

- test.spthy: Test protocol, it shows how a protocol would usually be coded, using Fr() facts for new randoms
- test_simple.spthy: Test protocol that uses the "simple" model of random. All randoms can be reused with any other random.
- test_role.spthy: Test protocol that uses the "role" model of random. Randoms are considered to belong to a role, such that two distinct roles cannot reuse the same random value.

The toy protocol from test.spthy is:

- A -> B: N1
- B -> A: N2
- A -> B: N3

#### Generating examples

It is possible to generate examples using the script tamparse.py:

```
tamparse.py --simple test_simple.spthy gen_simple --leak-once --leak-always --reuse-once --reuse-always
tamparse.py --role test_role.spthy gen_role --leak-once --leak-always --reuse-once --reuse-always
```
