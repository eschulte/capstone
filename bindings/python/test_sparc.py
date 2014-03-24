#!/usr/bin/env python

# Capstone Python bindings, by Nguyen Anh Quynnh <aquynh@gmail.com>

from capstone import *
from capstone.sparc import *

SPARC_CODE = "\x80\xa0\x40\x02\x85\xc2\x60\x08\x85\xe8\x20\x01\x81\xe8\x00\x00\x90\x10\x20\x01\xd5\xf6\x10\x16\x21\x00\x00\x0a\x86\x00\x40\x02\x01\x00\x00\x00\x12\xbf\xff\xff\x10\xbf\xff\xff\xa0\x02\x00\x09\x0d\xbf\xff\xff\xd4\x20\x60\x00\xd4\x4e\x00\x16\x2a\xc2\x80\x03"
SPARCV9_CODE = "\x81\xa8\x0a\x24\x89\xa0\x10\x20\x89\xa0\x1a\x60\x89\xa0\x00\xe0"

all_tests = (
        (CS_ARCH_SPARC, CS_MODE_BIG_ENDIAN, SPARC_CODE, "Sparc"),
        (CS_ARCH_SPARC, CS_MODE_BIG_ENDIAN+CS_MODE_V9, SPARCV9_CODE, "SparcV9"),
        )

def to_hex(s):
    return " ".join("0x" + "{0:x}".format(ord(c)).zfill(2) for c in s) # <-- Python 3 is OK

def to_x_32(s):
    from struct import pack
    if not s: return '0'
    x = pack(">i", s).encode('hex')
    while x[0] == '0': x = x[1:]
    return x

### Test class Cs
def test_class():
    def print_insn_detail(insn):
        # print address, mnemonic and operands
        print("0x%x:\t%s\t%s" %(insn.address, insn.mnemonic, insn.op_str))

        if len(insn.operands) > 0:
            print("\top_count: %u" %len(insn.operands))
            c = 0
            for i in insn.operands:
                if i.type == SPARC_OP_REG:
                    print("\t\toperands[%u].type: REG = %s" %(c, insn.reg_name(i.reg)))
                if i.type == SPARC_OP_IMM:
                    print("\t\toperands[%u].type: IMM = 0x%s" %(c, to_x_32(i.imm)))
                if i.type == SPARC_OP_MEM:
                    print("\t\toperands[%u].type: MEM" %c)
                    if i.mem.base != 0:
                        print("\t\t\toperands[%u].mem.base: REG = %s" \
                            %(c, insn.reg_name(i.mem.base)))
                    if i.mem.disp != 0:
                        print("\t\t\toperands[%u].mem.disp: 0x%s" \
                            %(c, to_x_32(i.mem.disp)))
                c += 1

        if insn.cc:
            print("\tConditional code: %u" %insn.cc)
        if insn.hint:
            print("\tBranch hint: %u" %insn.hint)

    for (arch, mode, code, comment) in all_tests:
        print("*" * 16)
        print("Platform: %s" %comment)
        print("Code: %s" % to_hex(code))
        print("Disasm:")

        try:
            md = Cs(arch, mode)
            md.detail = True
            for insn in md.disasm(code, 0x1000):
                print_insn_detail(insn)
                print
            print "0x%x:\n" % (insn.address + insn.size)
        except CsError as e:
            print("ERROR: %s" %e)


test_class()
