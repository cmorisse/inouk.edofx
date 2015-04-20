# coding: utf8


import sys

import os
import ConfigParser
from inouk.edofx import OFXParser

from optparse import OptionParser, OptionGroup

__version__ = "ofxplode.py v0.1 - april 2010" 

def main(source_file):
    """
        Takes a multi-account OFX file as input and
        output one OFX file per account.
    """
    f = open(source_file)
    p = OFXParser(f.read())
    o = p.parse()
    
    # on vire les infos sur les cartes de crédits
    try:
        del o.CREDITCARDMSGSRSV1
    except:
        pass    
    
    # first we backup all account information
    account_list = list() 
    for e in o.BANKMSGSRSV1.STMTTRNRS:
        account_list.append(e)

    # we wipe all accounts
    del o.BANKMSGSRSV1.STMTTRNRS
 
    for e in account_list:
        o.BANKMSGSRSV1.children.append(e)
        for t in o.BANKMSGSRSV1.STMTTRNRS.STMTRS.BANKTRANLIST.STMTTRN:
            t.TRNTYPE.value = t.MEMO.value # update transaction type
            t.MEMO.value = ''
            if t.TRNTYPE.value == 'PAIEMENT PAR CARTE' :
                t.MEMO.value = "Operation du %s" % (t.NAME.value[-5:],)
                t.NAME.value = t.NAME.value[:-5].lstrip().rstrip() 
            elif t.TRNTYPE.value == 'REMBOURSEMENT DE PRET' :
                t.MEMO.value = "Echeance du %s " % (t.NAME.value[-8:],)
                t.NAME.value = t.NAME.value[:-8].lstrip().rstrip() 
                
            
        
        fofx = open('compte_%s_from_%s_to_%s.ofx' %  (e.STMTRS.BANKACCTFROM.ACCTID.val, e.STMTRS.BANKTRANLIST.DTSTART.value[:8], e.STMTRS.BANKTRANLIST.DTEND.value[:8] ),'w')
        fofx.write(o.ofx_repr())
        fofx.close()
        
        fxml = open('compte_%s_from_%s_to_%s.xml' %  (e.STMTRS.BANKACCTFROM.ACCTID.val, e.STMTRS.BANKTRANLIST.DTSTART.value[:8], e.STMTRS.BANKTRANLIST.DTEND.value[:8] ),'w')
        fxml.write(o.xml_repr())
        fxml.close()

        del o.BANKMSGSRSV1.STMTTRNRS
        

if __name__ == '__main__':
    # TODO:  add an option for CA files
    
    usage = "usage: %prog ofx_source_filename"
    parser = OptionParser(usage, version=__version__)
    
    (options, args) = parser.parse_args()
    
    if not args or len(args) > 1 :
        print "18ducks - OFX file exploder"
        print
        print "    use ./ofxplode.py -h or --help for usage instructions."
        print
        sys.exit(0)

    ret = main( args[0] )
    sys.exit(ret)
    
