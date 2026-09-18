#!/usr/bin/env python3
"""Generate the AetherArray Rev A KiCad project from the decision 0003 architecture.

The four RF channels come from one hierarchical sheet instantiated four times, so
they are identical by construction rather than by inspection.
"""
import os, re, uuid, json

OUT   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PROJ  = "aetherarray-reva"
STOCK = r"C:\Program Files\KiCad\10.0\share\kicad\symbols"
NS    = uuid.UUID("6f1c9a52-3d44-4f0e-9c21-1aec00000a01")
U     = lambda k: str(uuid.uuid5(NS, k))

DS_PE = "https://www.psemi.com/pdf/datasheets/pe4259ds.pdf"
DS_AD = "https://www.analog.com/media/en/technical-documentation/data-sheets/AD8318.pdf"

# ------------------------------------------------------------------ s-expr utils
def balanced(txt, start):
    i = txt.index("(", start); d = 0; j = i
    while True:
        if txt[j] == "(": d += 1
        elif txt[j] == ")":
            d -= 1
            if d == 0: return txt[i:j + 1]
        j += 1

def extract(libfile, name):
    txt = open(os.path.join(STOCK, libfile), encoding="utf-8").read()
    m = re.search(r'^\t\(symbol "%s"' % re.escape(name), txt, re.M)
    if not m: raise SystemExit("missing symbol %s:%s" % (libfile, name))
    return balanced(txt, m.start())

SUB_RE = re.compile(r'^\t\t\(symbol "([^"]+)_(\d+_\d+)"', re.M)

def resolve(libfile, name, depth=0):
    """Return a symbol block with any (extends ...) chain flattened into it.

    KiCad derives package variants from a base symbol, so the pins live on the
    ancestor. Embedding a derived symbol on its own would give a pinless part.
    """
    if depth > 8: raise SystemExit("extends chain too deep: %s" % name)
    blk = extract(libfile, name)
    m = re.search(r'\(extends "([^"]+)"\)', blk)
    if not m:
        return blk
    parent = resolve(libfile, m.group(1), depth + 1)
    subs = []
    for sm in SUB_RE.finditer(parent):
        sub = balanced(parent, sm.start())
        subs.append(re.sub(r'^\(symbol "[^"]+_(\d+_\d+)"',
                           lambda mm: '(symbol "%s_%s"' % (name, mm.group(1)), sub, count=1))
    body = blk[:blk.rindex(")")].replace(m.group(0), "").rstrip()
    body += "\n" + "\n".join("\t\t" + s.replace("\n", "\n\t\t") for s in subs) + "\n\t)"
    return body

PIN_RE = re.compile(
    r'\(pin\s+(\w+)\s+(\w+)\s*\(at\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\)'
    r'.*?\(name\s+"([^"]*)".*?\(number\s+"([^"]*)"', re.S)

def pins_of(block):
    return [(g[6], g[5], float(g[2]), float(g[3]), float(g[4]))
            for g in (m.groups() for m in PIN_RE.finditer(block))]

# ------------------------------------------------------------------ own symbols
def mk_pin(num, name, x, y, ang, etype):
    return ('\t\t\t(pin %s line (at %s %s %s) (length 2.54)\n'
            '\t\t\t\t(name "%s" (effects (font (size 1.27 1.27))))\n'
            '\t\t\t\t(number "%s" (effects (font (size 1.27 1.27))))\n\t\t\t)'
            % (etype, x, y, ang, name, num))

def mk_symbol(name, value, desc, ds, pins, w, h, props=()):
    p = ['\t(symbol "%s"' % name, '\t\t(pin_names (offset 0.254))',
         '\t\t(exclude_from_sim no) (in_bom yes) (on_board yes)',
         '\t\t(property "Reference" "U" (at 0 %.2f 0) (effects (font (size 1.27 1.27))))' % (h + 2.54),
         '\t\t(property "Value" "%s" (at 0 %.2f 0) (effects (font (size 1.27 1.27))))' % (value, -h - 2.54),
         '\t\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))',
         '\t\t(property "Datasheet" "%s" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))' % ds,
         '\t\t(property "Description" "%s" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))' % desc]
    for k, v in props:
        p.append('\t\t(property "%s" "%s" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))' % (k, v))
    p += ['\t\t(symbol "%s_0_1"' % name,
          '\t\t\t(rectangle (start %.2f %.2f) (end %.2f %.2f) (stroke (width 0.254)'
          ' (type default)) (fill (type background)))' % (-w, h, w, -h), '\t\t)',
          '\t\t(symbol "%s_1_1"' % name]
    p += [mk_pin(*q) for q in pins]
    p += ['\t\t)', '\t)']
    return "\n".join(p)

PE_PINS = [("5","RFC",-12.7,0,0,"passive"), ("1","RF1",12.7,5.08,180,"passive"),
           ("3","RF2",12.7,-5.08,180,"passive"), ("4","CTRL",-12.7,-5.08,0,"input"),
           ("6","VDD",0,12.7,270,"power_in"), ("2","GND",0,-12.7,90,"power_in")]
AD_PINS = [("14","INHI",-17.78,10.16,0,"input"), ("15","INLO",-17.78,7.62,0,"input"),
           ("16","ENBL",-17.78,2.54,0,"input"),  ("10","TADJ",-17.78,-2.54,0,"input"),
           ("5","CLPF",-17.78,-7.62,0,"passive"),("6","VOUT",17.78,10.16,180,"output"),
           ("7","VSET",17.78,7.62,180,"input"),  ("13","TEMP",17.78,2.54,180,"output"),
           ("3","VPSI",-7.62,17.78,270,"power_in"),("4","VPSI2",-2.54,17.78,270,"power_in"),
           ("9","VPSO",2.54,17.78,270,"power_in"),
           ("1","CMIP",-10.16,-17.78,90,"power_in"),("2","CMIP2",-7.62,-17.78,90,"power_in"),
           ("11","CMIP3",-5.08,-17.78,90,"power_in"),("12","CMIP4",-2.54,-17.78,90,"power_in"),
           ("8","CMOP",2.54,-17.78,90,"power_in")]
TL_PINS = [("1","A",-10.16,0,0,"passive"), ("2","B",10.16,0,180,"passive")]

NUC_SIGNALS = ([("EN%d" % n, "output") for n in range(4)]
               + [("B45_%d" % n, "output") for n in range(4)]
               + [("B90_%d" % n, "output") for n in range(4)]
               + [("B180_%d" % n, "output") for n in range(4)]
               + [("MON_SEL", "output"), ("ADC_DET", "input"), ("ADC_TEMP", "input"),
                  ("I2C_SCL", "bidirectional"), ("I2C_SDA", "bidirectional"),
                  ("+5V", "power_out"), ("+3V3", "power_out"),
                  ("GND", "power_out"), ("GND2", "passive"), ("GND3", "passive")])
NUC_PINS = []
for _i, (_nm, _ty) in enumerate(NUC_SIGNALS):
    if _i < 13:
        NUC_PINS.append((str(_i + 1), _nm, -20.32, 30.48 - _i * 5.08, 0, _ty))
    else:
        NUC_PINS.append((str(_i + 1), _nm, 20.32, 30.48 - (_i - 13) * 5.08, 180, _ty))


def symbol_lib():
    out = ['(kicad_symbol_lib', '\t(version 20241209)',
           '\t(generator "kicad_symbol_editor")', '\t(generator_version "9.0")']
    out.append(mk_symbol("PE4259-63", "PE4259-63",
        "SPDT RF switch 10 MHz to 3000 MHz, SC-70-6. Pin table from vendor data sheet "
        "table 7. Single-pin control mode: pin 6 is VDD and requires bypassing. "
        "CTRL polarity (which level selects RF1) is still to confirm; it affects "
        "firmware only, not this netlist.",
        DS_PE, PE_PINS, 12.7, 12.7,
        (("MPN","PE4259-63"), ("Manufacturer","pSemi"), ("Package","SC-70-6"))))
    out.append(mk_symbol("AD8318", "AD8318",
        "1 MHz to 8 GHz logarithmic detector, 16-lead LFCSP. Slope -25 mV/dB, "
        "single 5 V supply, 68 mA typical. Exposed pad is internally tied to CMIP "
        "and must be soldered to ground.",
        DS_AD, AD_PINS, 17.78, 17.78,
        (("MPN","AD8318ACPZ"), ("Manufacturer","Analog Devices"), ("Package","LFCSP-16"))))
    out.append(mk_symbol("TLINE_SYMBOLIC", "TLINE",
        "Symbolic transmission line. Electrical length lives in EL_DEG; the physical "
        "length is a layout parameter and is deliberately not fixed here. See "
        "hardware/rev-a/layout-constraints.md.",
        "", TL_PINS, 10.16, 3.81,
        (("EL_DEG","TBD"), ("Z0_OHM","50"), ("LAYOUT","set at layout from stack-up and f0"))))
    out.append(mk_symbol("NUCLEO_G0_IF", "NUCLEO_G0_IF",
        "Board interface to an STM32G0 Nucleo carrying 17 control lines, 2 converter "
        "returns, I2C and the incoming supplies. The Nucleo sources every rail and "
        "every control line, so those pins are power outputs and outputs.",
        "", NUC_PINS, 20.32, 33.02,
        (("Fn","2x13 2.54 mm header, mates to the Nucleo through a ribbon"),)))
    out.append(")")
    return "\n".join(out) + "\n"

CUST = {}
def custom(nm):
    if not CUST:
        txt = symbol_lib()
        for n in ("PE4259-63", "AD8318", "TLINE_SYMBOLIC", "NUCLEO_G0_IF"):
            CUST[n] = balanced(txt, re.search(r'^\t\(symbol "%s"' % re.escape(n), txt, re.M).start())
    return CUST[nm]

LIBC = {}
def stock(libid, f, n):
    if libid not in LIBC: LIBC[libid] = resolve(f, n)
    return LIBC[libid]

# ------------------------------------------------------------------ sheet model
STUB = {0:(-1,0), 180:(1,0), 90:(0,1), 270:(0,-1)}
SNAP = lambda v: round(v / 1.27) * 1.27
def Lc(n): return ("local", n)
def Hi(n): return ("hier", n)
def Gl(n): return ("global", n)

class Sheet:
    def __init__(self, name, paper, suuid, sub_paths=None):
        self.name, self.paper, self.uuid = name, paper, suuid
        self.sub_paths = sub_paths
        self.body, self.libs = [], {}

    def emit(self):
        o = ['(kicad_sch', '\t(version 20250114)', '\t(generator "eeschema")',
             '\t(generator_version "9.0")', '\t(uuid "%s")' % self.uuid,
             '\t(paper "%s")' % self.paper, '\t(lib_symbols']
        for libid, blk in self.libs.items():
            b = re.sub(r'^\(symbol "[^"]*"', '(symbol "%s"' % libid, blk, count=1)
            o.append("\n".join(("\t\t" + l) if l.strip() else l for l in b.split("\n")))
        o.append('\t)')
        o += self.body
        if self.sub_paths is None:
            o.append('\t(sheet_instances (path "/" (page "1")))')
        o += ['\t(embedded_fonts no)', ')']
        return "\n".join(o) + "\n"

def place(sh, libid, blk, ref, value, x, y, nets, props=(), inst=None):
    """Place a symbol; stub each pin and label it. nets keys are pin numbers or names."""
    if libid not in sh.libs: sh.libs[libid] = blk
    x, y = SNAP(x), SNAP(y)
    pl = pins_of(blk)
    known = {p[0] for p in pl} | {p[1] for p in pl}
    unknown = set(nets) - known
    if unknown:
        raise SystemExit("%s %s: unknown pins %s (have %s)"
                         % (libid, ref, sorted(unknown), sorted(known)))
    b = ['\t(symbol', '\t\t(lib_id "%s")' % libid, '\t\t(at %.2f %.2f 0)' % (x, y),
         '\t\t(unit 1)', '\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)',
         '\t\t(uuid "%s")' % U("s:%s:%s" % (sh.name, ref)),
         '\t\t(property "Reference" "%s" (at %.2f %.2f 0)'
         ' (effects (font (size 1.27 1.27)) (justify left)))' % (ref, x - 20, y - 24),
         '\t\t(property "Value" "%s" (at %.2f %.2f 0)'
         ' (effects (font (size 1.27 1.27)) (justify left)))' % (value, x - 20, y - 21.5)]
    for k, v in props:
        b.append('\t\t(property "%s" "%s" (at %.2f %.2f 0)'
                 ' (effects (font (size 1.27 1.27)) (hide yes)))' % (k, v, x, y))
    for num, nm, px, py, ang in pl:
        b.append('\t\t(pin "%s" (uuid "%s"))' % (num, U("p:%s:%s:%s" % (sh.name, ref, num))))
    if inst:
        b.append('\t\t(instances (project "%s"' % PROJ)
        for path, r in inst:
            b.append('\t\t\t(path "%s" (reference "%s") (unit 1))' % (path, r))
        b.append('\t\t))')
    else:
        b.append('\t\t(instances (project "%s" (path "/%s" (reference "%s") (unit 1))))'
                 % (PROJ, sh.uuid, ref))
    b.append('\t)')
    sh.body.append("\n".join(b))

    for num, nm, px, py, ang in pl:
        cx, cy = x + px, y - py
        dx, dy = STUB[int(ang) % 360]
        ex, ey = cx + dx * 6.35, cy + dy * 6.35
        net = nets.get(num, nets.get(nm))
        key = "%s:%s:%s" % (sh.name, ref, num)
        if net is None:
            sh.body.append('\t(no_connect (at %.2f %.2f) (uuid "%s"))' % (cx, cy, U("nc:" + key)))
            continue
        sh.body.append('\t(wire (pts (xy %.2f %.2f) (xy %.2f %.2f)) (stroke (width 0)'
                       ' (type default)) (uuid "%s"))' % (cx, cy, ex, ey, U("w:" + key)))
        kind, label = net
        just = "left" if dx >= 0 else "right"
        if kind == "hier":
            sh.body.append('\t(hierarchical_label "%s" (shape passive) (at %.2f %.2f 0)'
                           ' (effects (font (size 1.27 1.27)) (justify %s)) (uuid "%s"))'
                           % (label, ex, ey, just, U("h:" + key)))
        elif kind == "global":
            sh.body.append('\t(global_label "%s" (shape passive) (at %.2f %.2f 0)'
                           ' (fields_autoplaced yes) (effects (font (size 1.27 1.27))'
                           ' (justify %s)) (uuid "%s"))' % (label, ex, ey, just, U("g:" + key)))
        else:
            sh.body.append('\t(label "%s" (at %.2f %.2f 0) (effects (font (size 1.27 1.27))'
                           ' (justify %s bottom)) (uuid "%s"))' % (label, ex, ey, just, U("l:" + key)))

S_R   = lambda: stock("Device:R", "Device.kicad_sym", "R")
S_C   = lambda: stock("Device:C", "Device.kicad_sym", "C")
S_TP  = lambda: stock("Connector:TestPoint", "Connector.kicad_sym", "TestPoint")
S_SMA = lambda: stock("Connector:Conn_Coaxial", "Connector.kicad_sym", "Conn_Coaxial")
S_HDR = lambda: stock("Connector_Generic:Conn_02x13_Odd_Even",
                      "Connector_Generic.kicad_sym", "Conn_02x13_Odd_Even")
S_T   = lambda: stock("Sensor_Temperature:MCP9808_MSOP",
                      "Sensor_Temperature.kicad_sym", "MCP9808_MSOP")
PWRSYM = {"+3V3": ("power:+3V3", "+3V3"), "+5V": ("power:+5V", "+5V"),
          "GND": ("power:GND", "GND")}
def S_PWR(k): return stock(PWRSYM[k][0], "power.kicad_sym", PWRSYM[k][1])
S_FLG = lambda: stock("power:PWR_FLAG", "power.kicad_sym", "PWR_FLAG")

def pwr(sh, kind, ref, x, y, inst=None):
    blk = S_PWR(kind)
    place(sh, PWRSYM[kind][0], blk, ref, kind, x, y, {"1": Gl(kind)}, inst=inst)

ROOT_UUID = U("root")
CHU  = [U("chsheet:%d" % n) for n in range(4)]
PATH = ["/%s/%s" % (ROOT_UUID, s) for s in CHU]
def I(fmt): return [(PATH[n], fmt % (n + 1)) for n in range(4)]

# ------------------------------------------------------------------ channel sheet
def build_channel():
    sh = Sheet("rf-channel", "A2", U("chfile"), sub_paths=PATH)
    pe, tl = custom("PE4259-63"), custom("TLINE_SYMBOLIC")
    X, Y, DX, DY = 50.8, 50.8, 76.2, 82.55
    P = lambda c, r: (X + c * DX, Y + r * DY)

    place(sh, "aetherarray:PE4259-63", pe, "U101", "PE4259-63", *P(0, 0),
          nets={"RFC": Hi("RF_COM"), "RF1": Lc("CHAIN_IN"), "RF2": Lc("TERM"),
                "CTRL": Hi("EN"), "VDD": Gl("+3V3"), "GND": Gl("GND")},
          props=(("MPN","PE4259-63"),("Fn","channel enable: RF1 through, RF2 to 50R")),
          inst=I("U%d01"))
    place(sh, "Device:R", S_R(), "R101", "50R", *P(1, 0),
          nets={"1": Lc("TERM"), "2": Gl("GND")},
          props=(("Fn","channel termination, holds the element at 50R when disabled"),),
          inst=I("R%d01"))
    place(sh, "Connector:TestPoint", S_TP(), "TP101", "TP_RF_IN", *P(2, 0),
          nets={"1": Lc("CHAIN_IN")}, inst=I("TP%d01"))
    place(sh, "Connector:TestPoint", S_TP(), "TP102", "TP_RF_OUT", *P(3, 0),
          nets={"1": Hi("RF_EL")}, inst=I("TP%d02"))

    prev, sw = "CHAIN_IN", 2
    for bi, deg in enumerate(("45", "90", "180")):
        ctl = "B" + deg
        out = Hi("RF_EL") if deg == "180" else Lc("N_%s_OUT" % deg)
        place(sh, "aetherarray:PE4259-63", pe, "U10%d" % sw, "PE4259-63", *P(0, bi + 1),
              nets={"RFC": Lc(prev), "RF1": Lc("N%s_REF_A" % deg), "RF2": Lc("N%s_DLY_A" % deg),
                    "CTRL": Hi(ctl), "VDD": Gl("+3V3"), "GND": Gl("GND")},
              props=(("MPN","PE4259-63"),("Fn","%s degree bit, input selector" % deg)),
              inst=I("U%%d0%d" % sw))
        sw += 1
        place(sh, "aetherarray:TLINE_SYMBOLIC", tl, "TL10%d" % (2*bi+1), "REF_%s" % deg, *P(1, bi + 1),
              nets={"1": Lc("N%s_REF_A" % deg), "2": Lc("N%s_REF_B" % deg)},
              props=(("EL_DEG","0"),("Z0_OHM","50"),
                     ("LAYOUT","reference arm of the %s degree bit" % deg)),
              inst=I("TL%%d0%d" % (2*bi+1)))
        place(sh, "aetherarray:TLINE_SYMBOLIC", tl, "TL10%d" % (2*bi+2), "DLY_%s" % deg, *P(2, bi + 1),
              nets={"1": Lc("N%s_DLY_A" % deg), "2": Lc("N%s_DLY_B" % deg)},
              props=(("EL_DEG",deg),("Z0_OHM","50"),
                     ("LAYOUT","delay arm: %s degrees more than the reference arm at f0" % deg)),
              inst=I("TL%%d0%d" % (2*bi+2)))
        place(sh, "aetherarray:PE4259-63", pe, "U10%d" % sw, "PE4259-63", *P(3, bi + 1),
              nets={"RFC": out, "RF1": Lc("N%s_REF_B" % deg), "RF2": Lc("N%s_DLY_B" % deg),
                    "CTRL": Hi(ctl), "VDD": Gl("+3V3"), "GND": Gl("GND")},
              props=(("MPN","PE4259-63"),("Fn","%s degree bit, output selector" % deg)),
              inst=I("U%%d0%d" % sw))
        sw += 1
        prev = "N_%s_OUT" % deg

    for i in range(7):
        place(sh, "Device:C", S_C(), "C10%d" % (i + 1), "100nF", *P(4 + i % 2, i // 2),
              nets={"1": Gl("+3V3"), "2": Gl("GND")},
              props=(("Fn","VDD bypass for one PE4259-63, single-pin control mode"),),
              inst=I("C%%d0%d" % (i + 1)))
    return sh

# ------------------------------------------------------------------ root sheet
def build_root():
    sh = Sheet("root", "A0", ROOT_UUID)
    pe, ad, tl = custom("PE4259-63"), custom("AD8318"), custom("TLINE_SYMBOLIC")
    X, Y, DX, DY = 50.8, 50.8, 82.55, 82.55
    P = lambda c, r: (X + c * DX, Y + r * DY)

    # common port and measurement path selector
    place(sh, "Connector:Conn_Coaxial", S_SMA(), "J904", "SMA_COMMON", *P(0, 0),
          nets={"1": Lc("COM_SMA"), "2": Gl("GND")},
          props=(("Fn","common port: analyser, or source in transmit"),))
    place(sh, "aetherarray:PE4259-63", pe, "U900", "PE4259-63", *P(1, 0),
          nets={"RFC": Lc("NET_COMMON"), "RF1": Lc("COM_SMA"), "RF2": Lc("DET_IN"),
                "CTRL": Lc("MON_SEL"), "VDD": Gl("+3V3"), "GND": Gl("GND")},
          props=(("MPN","PE4259-63"),
                 ("Fn","measurement path select: analyser on RF1, detector on RF2")))
    place(sh, "Device:C", S_C(), "C900", "100nF", *P(2, 0),
          nets={"1": Gl("+3V3"), "2": Gl("GND")},
          props=(("Fn","VDD bypass for U900"),))

    # reciprocal 4-way Wilkinson tree
    tree = [("TL901","TL902","NET_COMMON","NODE_A","NODE_B","R900"),
            ("TL903","TL904","NODE_A","CH0_RF","CH1_RF","R901"),
            ("TL905","TL906","NODE_B","CH2_RF","CH3_RF","R902")]
    for i, (ta, tb, src, oa, ob, riso) in enumerate(tree):
        place(sh, "aetherarray:TLINE_SYMBOLIC", tl, ta, "QW_70R7", *P(3, i),
              nets={"1": Lc(src), "2": Lc(oa)},
              props=(("EL_DEG","90"),("Z0_OHM","70.7"),
                     ("LAYOUT","quarter wave arm of a 2-way Wilkinson at f0")))
        place(sh, "aetherarray:TLINE_SYMBOLIC", tl, tb, "QW_70R7", *P(4, i),
              nets={"1": Lc(src), "2": Lc(ob)},
              props=(("EL_DEG","90"),("Z0_OHM","70.7"),
                     ("LAYOUT","quarter wave arm of a 2-way Wilkinson at f0")))
        place(sh, "Device:R", S_R(), riso, "100R", *P(5, i),
              nets={"1": Lc(oa), "2": Lc(ob)},
              props=(("Fn","Wilkinson isolation resistor"),))

    # four channel sheets
    for n in range(4):
        sx, sy = 40.64 + n * 76.2, 660.4
        pins = [("RF_COM", "passive", 180), ("EN", "input", 180), ("B45", "input", 180),
                ("B90", "input", 180), ("B180", "input", 180), ("RF_EL", "passive", 0)]
        b = ['\t(sheet', '\t\t(at %.2f %.2f)' % (sx, sy), '\t\t(size 50.8 76.2)',
             '\t\t(exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)',
             '\t\t(stroke (width 0.1524) (type solid)) (fill (color 0 0 0 0.0000))',
             '\t\t(uuid "%s")' % CHU[n],
             '\t\t(property "Sheetname" "CH%d" (at %.2f %.2f 0)'
             ' (effects (font (size 1.27 1.27)) (justify left bottom)))' % (n, sx, sy - 0.7),
             '\t\t(property "Sheetfile" "rf-channel.kicad_sch" (at %.2f %.2f 0)'
             ' (effects (font (size 1.27 1.27)) (justify left top)))' % (sx, sy + 76.9)]
        for k, (pname, ptype, ang) in enumerate(pins):
            px = sx + 50.8 if ang == 0 else sx
            py = sy + 10.16 + k * 10.16
            just = "left" if ang == 0 else "right"
            b.append('\t\t(pin "%s" %s (at %.2f %.2f %d) (uuid "%s")'
                     ' (effects (font (size 1.27 1.27)) (justify %s)))'
                     % (pname, ptype, px, py, ang, U("sp:%d:%s" % (n, pname)), just))
            sh.body.append('\t(wire (pts (xy %.2f %.2f) (xy %.2f %.2f)) (stroke (width 0)'
                           ' (type default)) (uuid "%s"))'
                           % (px, py, px + (6.35 if ang == 0 else -6.35), py,
                              U("sw:%d:%s" % (n, pname))))
            netname = {"RF_COM": "CH%d_RF" % n, "RF_EL": "EL%d_RF" % n,
                       "EN": "EN%d" % n, "B45": "B45_%d" % n,
                       "B90": "B90_%d" % n, "B180": "B180_%d" % n}[pname]
            sh.body.append('\t(label "%s" (at %.2f %.2f 0) (effects (font (size 1.27 1.27))'
                           ' (justify %s bottom)) (uuid "%s"))'
                           % (netname, px + (6.35 if ang == 0 else -6.35), py,
                              "left" if ang == 0 else "right", U("sl:%d:%s" % (n, pname))))
        b.append('\t\t(instances (project "%s" (path "/%s" (page "%d"))))' % (PROJ, ROOT_UUID, n + 2))
        b.append('\t)')
        sh.body.append("\n".join(b))
        place(sh, "Connector:Conn_Coaxial", S_SMA(), "J90%d" % n, "SMA_EL%d" % n, *P(9, n),
              nets={"1": Lc("EL%d_RF" % n), "2": Gl("GND")},
              props=(("Fn","element port %d: R1 and R2 per element access" % n),))

    # detector
    place(sh, "Device:C", S_C(), "C901", "100pF", *P(0, 1),
          nets={"1": Lc("DET_IN"), "2": Lc("AD_INHI")},
          props=(("Fn","INHI ac coupling"),))
    place(sh, "Device:C", S_C(), "C902", "100pF", *P(1, 1),
          nets={"1": Lc("AD_INLO"), "2": Gl("GND")},
          props=(("Fn","INLO ac coupling to ground"),))
    place(sh, "aetherarray:AD8318", ad, "U901", "AD8318", *P(0, 2),
          nets={"INHI": Lc("AD_INHI"), "INLO": Lc("AD_INLO"), "ENBL": Gl("+5V"),
                "TADJ": Lc("TADJ_N"), "CLPF": Lc("CLPF_N"),
                "VOUT": Lc("VOUT_N"), "VSET": Lc("VOUT_N"), "TEMP": Lc("TEMP_N"),
                "VPSI": Gl("+5V"), "VPSI2": Gl("+5V"), "VPSO": Gl("+5V"),
                "CMIP": Gl("GND"), "CMIP2": Gl("GND"), "CMIP3": Gl("GND"),
                "CMIP4": Gl("GND"), "CMOP": Gl("GND")},
          props=(("MPN","AD8318ACPZ"),
                 ("Fn","measurement mode: VOUT tied to VSET. ENBL to VPSI for normal operation")))
    for ref, val, nets_, fn, cell in (
        ("C903","100nF",{"1":Gl("+5V"),"2":Gl("GND")},"VPSI decoupling",(0,5)),
        ("C904","1nF", {"1":Gl("+5V"),"2":Gl("GND")},"VPSI high frequency decoupling",(1,5)),
        ("C905","100nF",{"1":Gl("+5V"),"2":Gl("GND")},"VPSO decoupling",(2,5)),
        ("C906","220pF",{"1":Lc("CLPF_N"),"2":Gl("GND")},"loop filter, value provisional",(3,5)),
        ("C907","100nF",{"1":Lc("ADC_DET"),"2":Gl("GND")},"VOUT anti alias",(4,5)),
        ("C908","100nF",{"1":Lc("ADC_TEMP"),"2":Gl("GND")},"TEMP anti alias",(5,5))):
        place(sh, "Device:C", S_C(), ref, val, *P(*cell), nets=nets_, props=(("Fn",fn),))
    place(sh, "Device:R", S_R(), "R903", "18k", *P(0, 3),
          nets={"1": Lc("TADJ_N"), "2": Gl("GND")},
          props=(("Fn","TADJ temperature compensation set resistor, value provisional"),))
    place(sh, "Device:R", S_R(), "R904", "1k", *P(1, 3),
          nets={"1": Lc("VOUT_N"), "2": Lc("ADC_DET")}, props=(("Fn","VOUT series to converter"),))
    place(sh, "Device:R", S_R(), "R905", "1k", *P(2, 3),
          nets={"1": Lc("TEMP_N"), "2": Lc("ADC_TEMP")}, props=(("Fn","TEMP series to converter"),))
    place(sh, "Connector:TestPoint", S_TP(), "TP900", "TP_VOUT", *P(3, 3), nets={"1": Lc("ADC_DET")})
    place(sh, "Connector:TestPoint", S_TP(), "TP901", "TP_TEMP", *P(4, 3), nets={"1": Lc("ADC_TEMP")})
    place(sh, "Connector:TestPoint", S_TP(), "TP902", "TP_5V", *P(5, 3), nets={"1": Gl("+5V")})
    place(sh, "Connector:TestPoint", S_TP(), "TP903", "TP_3V3", *P(6, 3), nets={"1": Gl("+3V3")})
    place(sh, "Connector:TestPoint", S_TP(), "TP904", "TP_GND", *P(7, 3), nets={"1": Gl("GND")})

    # temperature telemetry
    place(sh, "Sensor_Temperature:MCP9808_MSOP", S_T(), "U902", "MCP9808", *P(0, 4),
          nets={"SDA": Lc("I2C_SDA"), "SCL": Lc("I2C_SCL"), "V_{DD}": Gl("+3V3"),
                "GND": Gl("GND"), "A0": Gl("GND"), "A1": Gl("GND"), "A2": Gl("GND")},
          props=(("MPN","MCP9808T-E/MS"),
                 ("Fn","R4 sensor 1, sited by the phase shifting network, address 0x18")))
    place(sh, "Sensor_Temperature:MCP9808_MSOP", S_T(), "U903", "MCP9808", *P(1, 4),
          nets={"SDA": Lc("I2C_SDA"), "SCL": Lc("I2C_SCL"), "V_{DD}": Gl("+3V3"),
                "GND": Gl("GND"), "A0": Gl("+3V3"), "A1": Gl("GND"), "A2": Gl("GND")},
          props=(("MPN","MCP9808T-E/MS"),
                 ("Fn","R4 sensor 2, sited by the detector, address 0x19")))
    place(sh, "Device:R", S_R(), "R906", "4k7", *P(2, 4),
          nets={"1": Lc("I2C_SDA"), "2": Gl("+3V3")}, props=(("Fn","I2C pull up"),))
    place(sh, "Device:R", S_R(), "R907", "4k7", *P(3, 4),
          nets={"1": Lc("I2C_SCL"), "2": Gl("+3V3")}, props=(("Fn","I2C pull up"),))
    place(sh, "Device:C", S_C(), "C909", "100nF", *P(4, 4),
          nets={"1": Gl("+3V3"), "2": Gl("GND")}, props=(("Fn","U902 decoupling"),))
    place(sh, "Device:C", S_C(), "C910", "100nF", *P(5, 4),
          nets={"1": Gl("+3V3"), "2": Gl("GND")}, props=(("Fn","U903 decoupling"),))

    # control and power interface to the Nucleo
    hdr = {nm: (Gl(nm[:-1]) if nm.startswith("GND") and nm != "GND"
                else (Gl(nm) if nm in ("+5V", "+3V3", "GND") else Lc(nm)))
           for nm, _t in NUC_SIGNALS}
    place(sh, "aetherarray:NUCLEO_G0_IF", custom("NUCLEO_G0_IF"), "J905",
          "NUCLEO_G0_IF", *P(6, 4), nets=hdr,
          props=(("Fn","interface to an STM32G0 Nucleo: 17 control lines, 2 converter"
                       " returns, I2C, and the incoming 5 V and 3V3 rails"),))
    return sh
# ------------------------------------------------------------------ emit
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "aetherarray.kicad_sym"), "w", encoding="utf-8").write(symbol_lib())
open(os.path.join(OUT, "sym-lib-table"), "w", encoding="utf-8").write(
    '(sym_lib_table\n  (version 7)\n  (lib (name "aetherarray")(type "KiCad")'
    '(uri "${KIPRJMOD}/aetherarray.kicad_sym")(options "")(descr "AetherArray Rev A parts"))\n)\n')
ch = build_channel()
open(os.path.join(OUT, "rf-channel.kicad_sch"), "w", encoding="utf-8").write(ch.emit())
rt = build_root()
open(os.path.join(OUT, PROJ + ".kicad_sch"), "w", encoding="utf-8").write(rt.emit())
open(os.path.join(OUT, PROJ + ".kicad_pro"), "w", encoding="utf-8").write(json.dumps({
    "board": {"design_settings": {}}, "boards": [], "cvpcb": {"equivalence_files": []},
    "erc": {"erc_exclusions": [], "meta": {"version": 0}, "rule_severities": {},
            "rule_severitieses": {}, "pin_map": [], "severities": {}},
    "libraries": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
    "meta": {"filename": PROJ + ".kicad_pro", "version": 3},
    "net_settings": {"classes": [{"name": "Default"}]},
    "pcbnew": {"page_layout_descr_file": ""},
    "schematic": {"legacy_lib_dir": "", "legacy_lib_list": []},
    "sheets": [[ROOT_UUID, "Root"]] + [[CHU[n], "CH%d" % n] for n in range(4)],
    "text_variables": {}}, indent=2))
print("written to", OUT)
