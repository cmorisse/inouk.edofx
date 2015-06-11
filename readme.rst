===============
EDOFX Framework
===============

EDOFX is a python framework / DSL to manipulate OFX **Version 1** files.

EDOFX has no dependencies other than Python standard library. 

EDOFX has been tested with python 2.5 to 2.7. 

Python 3 is not supported yet.

--------------------
Content of this file
--------------------

- Licence
- Installation
- Usage
   - Parse an OFX file or string
   - Inspect and manipulate OFX file
       * Navigate OFX tree
       * [[Home|Iterators]] 
       * Indexers
       * Delete Nodes
       * Modify Nodes

   - OFX tree display and export

- Package Description
    - edofx.py 
        * OFXNode
        * OFXParser
        * OFXObfuscator
    - edofx_integration.py
    - test directory description

License
=======

EDOFX is licensed under MIT License. See LICENCE.txt

Installation
============

From pypi
---------

Use pip or easy_install:

::

    $ pip install inouk.edofx 
    or
    $ easy_install inouk.edofx 

From source
-----------

Git clone from the official repository then install with:

::

    python setup.py install

   

Usage
=====

Parse an OFX file or string
---------------------------

To experiment, create a virtualenv, install inouk.edofx then launch python and use:

>>> from inouk import edofx
>>> f = open('test/fixtures/multi_account_file.ofx', 'U')  # Files must be opened using 'U' mode as the parser do not manage \r\n EOL
>>> OFX = edofx.OFXParser(f.read()).parse()
>>> OFX
<OFX>...</OFX>

OFX now contains an OFXNode's tree representation of test/fixtures/multi_account_file.ofx.

Inspect and manipulate the OFX tree
-----------------------------------

**To navigate OFX tree, use :**

>>> OFX.children 
[<SIGNONMSGSRSV1>...</SIGNONMSGSRSV1>, <BANKMSGSRSV1>...</BANKMSGSRSV1>, <CREDITCARDMSGSRSV1>...</CREDITCARDMSGSRSV1>]
>>> OFX.SIGNONMSGSRSV1.children
[<SONRS>...</SONRS>]
>>> OFX.SIGNONMSGSRSV1.SONRS.children
[<STATUS>...</STATUS>, <DTSERVER>20100305094649, <LANGUAGE>FRA]
>>> OFX.SIGNONMSGSRSV1.SONRS.DTSERVER
<DTSERVER>20100305094649
>>> OFX.SIGNONMSGSRSV1.SONRS.DTSERVER.value
'20100305094649' # This is the raw value as a string
>>> OFX.SIGNONMSGSRSV1.SONRS.DTSERVER.val # returns date or float when appropriate 
datetime.date(2010, 3, 5)

**Iterators are ok:**

>>> # To list account numbers present in file 
>>> for account in OFX.BANKMSGSRSV1.STMTTRNRS:
...     print 'account #', account.TRNUID.val
... 
account # 34995678052
account # 85576218690
account # 44498008728
account # 42025380697
account # 62631064788

**Indexers are ok:**

>>> OFX.BANKMSGSRSV1.STMTTRNRS[2].TRNUID.val
'44498008728'
>>> len(OFX.BANKMSGSRSV1.STMTTRNRS)
5

**Modify nodes**

*To delete nodes:*

>>> OFX.children
[<SIGNONMSGSRSV1>...</SIGNONMSGSRSV1>, <BANKMSGSRSV1>...</BANKMSGSRSV1>, <CREDITCARDMSGSRSV1>...</CREDITCARDMSGSRSV1>]
>>> del OFX.CREDITCARDMSGSRSV1 # Warning does not work (yet) on indexed items
>>> OFX.children
[<SIGNONMSGSRSV1>...</SIGNONMSGSRSV1>, <BANKMSGSRSV1>...</BANKMSGSRSV1>]

*To modify nodes:*

For that purpose, you must let '.value' with a string. 
Note that '.val' attribute is not ( yet ) writable. 

>>> OFX.SIGNONMSGSRSV1.SONRS.LANGUAGE
<LANGUAGE>FRA
>>> OFX.SIGNONMSGSRSV1.SONRS.LANGUAGE.value = 'Italian'
>>> OFX.SIGNONMSGSRSV1.SONRS.LANGUAGE
<LANGUAGE>Italian
>>> 

*To alter Tree structure:*

>>> OFX.SIGNONMSGSRSV1.SONRS.children.append(edofx.OFXNode(name='COLOR', value='blue')) # insert is ok too
>>> OFX.SIGNONMSGSRSV1.SONRS.children
[<STATUS>...</STATUS>, <DTSERVER>20100305094649, <LANGUAGE>Italian, <COLOR>blue]


OFX tree display and export
---------------------------

OFXNode supports 3 output / dump formats :

* OFX ; to re-export as OFX after tree/nodes modifications
* XML ; easier to read
* Obfuscated ; re-export as OFX with all sensitive information jammed. 

**Important information**: Nodes 'ACCTTYPE', 'CODE', 'STATUS', 'SEVERITY', 'LANGUAGE', 'CURDEF', 'TRNTYPE' are not obfuscated.

Examples
........

>>> print OFX.ofx_repr()
<OFX>
<SIGNONMSGSRSV1>
<SONRS>
<STATUS>
<CODE>0
<SEVERITY>INFO
</STATUS>
<DTSERVER>20100305094649
<LANGUAGE>Italian
<COLOR>blue
</SONRS>
...

>>> print OFX.obfuscated_ofx_repr()
<OFX>
<SIGNONMSGSRSV1>
<SONRS>
<STATUS>
<CODE>0
<SEVERITY>INFO
</STATUS>
<DTSERVER>20100305094649
<LANGUAGE>Italian
<COLOR>BHVB
</SONRS>

>>> print OFX.xml_repr()
<OFX>
    <SIGNONMSGSRSV1>
        <SONRS>
            <STATUS>
                <CODE>0</CODE>
                <SEVERITY>INFO</SEVERITY>
            </STATUS>
            <DTSERVER>20100305094649</DTSERVER>
            <SIZE>XXL</SIZE>
            <LANGUAGE>Italian</LANGUAGE>
            <COLOR>blue</COLOR>
        </SONRS>


OFX Headers
...........

OFX Headers are available as a dict.


Headers can be parsed in two ways:

* if the parse() has been called, they can be retrieved using attribute OFX_headers of the parser object.
* OFXParser can de asked to parse only the headers (not the content) with the parse_headers() method (Cf.  tests 7,8 and 9 of test_01_parser.py for an example).

Package description
===================

This package contains :

* edofx/__init__.py ; the framework
* tests ; contains Python unit-test classes
    - edofx_integration.py ; an example demonstrating how to parse an OFX source into specific classes.


edofx/__init__.py
-----------------

The framework by itself is structured in 3 classes:

* OFXNode
* OFXParser
* OFXObfuscator

Use python help for method level description. (Even if I'm slightly optimistic about the python help content quality...)

OFXNode
-------

OFXNode is used to store parsed OFX sources.

OFXParser
---------

OFXParser builds OFXNode tree from a string containing some OFX content.

OFXObfuscator
-------------

OFXObfuscator is a naive obfuscator based on lexical analysis. 
OFXObfuscator is able to obfuscate OFX sources OFXParser has been unable to parse. 
Use this if you want to sent me some OFX files that OFXParser fails to process.

tests
-----

There you will find 3 examples and some unittests:

- edofx_integration.py (see below)
- edofx2csv.py ; shows how to export andofx file to csv in 
- ofxplode.py ; shows how to generate a single account OFX file from a multi account one 
- unit tests

edofx_integration.py
....................

This file shows how to parse a multi account type / multi account OFX file into Statement and StatementTransaction classes and export everything into a set of per account csv files.

Most interesting part is the render_as_DOT() function.

Following render_as_DOT() code snippet shows how OFXNode makes it easy to load OFX content into arbitrary python objects:

::

    if OFX.BANKMSGSRSV1 :
        # For each account statement...
        for aSTMTTRNRS in OFX.BANKMSGSRSV1.STMTTRNRS:
            stmt = Statement('CHECKING')
            stmt.currency   = aSTMTTRNRS.STMTRS.CURDEF.val
            stmt.bank_id    = aSTMTTRNRS.STMTRS.BANKACCTFROM.BANKID.val
            stmt.branch_id  = aSTMTTRNRS.STMTRS.BANKACCTFROM.BRANCHID.val
            stmt.account_id = aSTMTTRNRS.STMTRS.BANKACCTFROM.ACCTID.val
            stmt.start_date = aSTMTTRNRS.STMTRS.BANKTRANLIST.DTSTART.val # returned as date
            stmt.end_date   = aSTMTTRNRS.STMTRS.BANKTRANLIST.DTEND.val   # returned as date
            # for each transaction in statement
            for s in aSTMTTRNRS.STMTRS.BANKTRANLIST.STMTTRN:
                st          = StatementTransaction()
                st.fitid    = s.FITID.val
                st.type     = s.TRNTYPE.val
                st.date     = s.DTPOSTED.val # returned as date
                st.amount   = s.TRNAMT.val   # returned as float
                st.name     = s.NAME.val
                st.memo     = s.MEMO.val
                stmt.transaction_list.append(st)
    
            stmt.balance      = aSTMTTRNRS.STMTRS.LEDGERBAL.BALAMT.val # returned as float
            stmt.balance_date = aSTMTTRNRS.STMTRS.LEDGERBAL.DTASOF.val # returned as date
            statement_list.append(stmt)


edofx2csv.py
............

Shows how to export an edofx file to csv format.


ofxplode.py 
...........

Takes a multi account OFX file and generates:

- a single account OFX file
- an XML representation of the single OFX file

unittests
..........

* Parser tests (test_01_parser.py)
* OFXTree export tests (test_02_OFXNode_export.py)
* Obfuscation tests (test_03_obfuscation.py)

Directory tests/fixtures contains a set of OFX file.real_file.ofx and multi_account_file.ofx have been built from real files using OFXNode.obfuscated_ofx_repr()

=======

**Disclaimer: EDOFX was my very first python code !! So many things I would have not written like this today.**
