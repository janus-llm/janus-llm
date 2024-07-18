 ** This test file was copied from:
 ** https://www.ibm.com/support/knowledgecenter/en/SSLTBW_2.1.0/com.ibm.zos.v2r1.asma100/appndxe.htm
 **

                                         High Level Assembler Option Summary                                   Page    1
                                                                                            HLASM R6.0  2008/07/11 17.48
  No Overriding ASMAOPT Parameters
  No Overriding Parameters
  No Process Statements


  Options for this Assembly
  NOADATA
    ALIGN
  NOASA
    BATCH
    CODEPAGE(047C)
  NOCOMPAT
  NODBCS
  NODECK
    DXREF
    ESD
  NOEXIT
    FLAG(0,ALIGN,CONT,EXLITW,NOIMPLEN,NOPAGE0,PUSH,RECORD,NOSUBSTR,USING0)
  NOFOLD
  NOGOFF
  NOINFO
    LANGUAGE(EN)
  NOLIBMAC
    LINECOUNT(60)
    LIST(121)
    MACHINE(,NOLIST)
    MXREF(SOURCE)
    OBJECT
    OPTABLE(UNI,NOLIST)
  NOPCONTROL
  NOPESTOP
  NOPROFILE
  NORA2
  NORENT
    RLD
    RXREF
    SECTALGN(8)
    SIZE(MAX)
  NOSUPRWARN
    SYSPARM()
  NOTERM
  NOTEST
    THREAD
  NOTRANSLATE
    TYPECHECK(MAGNITUDE,REGISTER)
    USING(NOLIMIT,MAP,WARN(15))
    XREF(SHORT,UNREFS)

  No Overriding DD Names

BIGNAME                                       External Symbol Dictionary                                       Page    2
Symbol   Type   Id     Address  Length   Owner Id Flags Alias-of                            HLASM R6.0  2008/07/11 17.48
A         SD 00000001 00000000 000000DE             00
PD2       CM 00000002 00000000 00000814             00    A

BIGNAME  Sample program.  1ST TITLE statement has no name, 2ND one does                                        Page    3
  Active Usings: None
  Loc  Object Code    Addr1 Addr2  Stmt   Source Statement                                  HLASM R6.0  2008/07/11 17.48
                                      2 **************************************************************          00002000
                                      3 *   Licensed Materials - Property of IBM                     *          00003000
                                      4 *                                                            *          00004000
                                      5 *   5696-234   5647-A01                                      *          00005000
                                      6 *                                                            *          00006000
                                      7 *   (C) Copyright IBM Corp. 1992, 2000. All Rights Reserved. *          00007000
                                      8 *                                                            *          00008000
                                      9 *   US Government Users Restricted Rights - Use,             *          00009000
                                     10 *   duplication or disclosure restricted by GSA ADP          *          00010000
                                     11 *   Schedule Contract with IBM Corp.                         *          00011000
                                     12 *                                                            *          00012000
                                     13 **************************************************************          00013000
                                     14 *********************************************************************   00014000
                                     15 * DISCLAIMER OF WARRANTIES                                          *   00015000
                                     16 *  The following enclosed code is sample code created by IBM        *   00016000
                                     17 *  Corporation. This sample code is licensed under the terms of     *   00017000
                                     18 *  the High Level Assembler license, but is not part of any         *   00018000
                                     19 *  standard IBM product.  It is provided to you solely for the      *   00019000
                                     20 *  purpose of demonstrating the usage of some of the features of    *   00020000
                                     21 *  High Level Assembler.  The code is not supported by IBM and      *   00021000
                                     22 *  is provided on an "AS IS" basis, without warranty of any kind.   *   00022000
                                     23 *  IBM shall not be liable for any damages arising out of your      *   00023000
                                     24 *  use of the sample code, even if IBM has been advised of the      *   00024000
                                     25 *  possibility of such damages.                                     *   00025000
                                     26 *********************************************************************   00026000
000000                00000 000DE    27 a        csect                                                          00027000
                 R:8  00000          28          using *,8                                                      00028000
000000 1BFF                          29          sr    15,15      Set return code to zero                       00029000
000002 07FE                          30          br    14          and return.                                  00030000
                                     32 **********************************************************************  00032000
                                     33 *              PUSH  and POP  statements                             *  00033000
                                     34 * Push down the PRINT statement, replace it, retrieve original       *  00034000
                                     35 **********************************************************************  00035000
                                     37          push  print     Save Default setting '  PRINT ON,NODATA,GEN'   00037000
                                B    38          print nogen,data                                               00038000
000004 0A23                          39          wto   mf=(E,(1))                    Expansion not shown        00039000
