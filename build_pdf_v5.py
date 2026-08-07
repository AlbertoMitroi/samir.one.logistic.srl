from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.units import inch
from PIL import Image
import os, math

W,H = 960,540  # 16:9 presentation canvas
OUT='output/pdf/samir-one-logistic-16x9-premium.pdf'
COVER='tmp/assets/cover-truck.png'; CARGUS='tmp/assets/cargus-logo.png'; AUTO='tmp/assets/auto-total-logo.png'
NAVY=HexColor('#05162A'); INK=HexColor('#071326'); PANEL=HexColor('#0B2746'); PANEL2=HexColor('#102F53')
CYAN=HexColor('#36D7FF'); BLUE=HexColor('#2074FF'); MINT=HexColor('#54DFB0'); WHITE=HexColor('#F7FBFF'); CLOUD=HexColor('#DCEEFF'); MUTED=HexColor('#93AEC8'); AMBER=HexColor('#FFC250'); RED=HexColor('#FF7285')
pdfmetrics.registerFont(TTFont('A','/System/Library/Fonts/Supplemental/Arial.ttf')); pdfmetrics.registerFont(TTFont('AB','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))

def fill(c,col): c.setFillColor(col); c.rect(0,0,W,H,stroke=0,fill=1)
def rr(c,x,y,w,h,r,fc,sc=None,sw=1):
    c.setFillColor(fc)
    if sc: c.setStrokeColor(sc); c.setLineWidth(sw); c.roundRect(x,y,w,h,r,stroke=1,fill=1)
    else: c.roundRect(x,y,w,h,r,stroke=0,fill=1)
def tx(c,s,x,y,sz=12,col=WHITE,b=False,a='left'):
    c.setFont('AB' if b else 'A',sz); c.setFillColor(col)
    {'left':c.drawString,'center':c.drawCentredString,'right':c.drawRightString}[a](x,y,s)
def wrap(c,s,x,y,w,sz=12,col=WHITE,b=False,lead=None):
    f='AB' if b else 'A'; lead=lead or sz*1.22; cur=''; lines=[]
    for word in s.split():
        v=(cur+' '+word).strip()
        if stringWidth(v,f,sz)<=w: cur=v
        else: lines.append(cur); cur=word
    if cur: lines.append(cur)
    for i,line in enumerate(lines): tx(c,line,x,y-i*lead,sz,col,b)
def dot(c,x,y,col=CYAN,r=4): c.setFillColor(col); c.circle(x,y,r,stroke=0,fill=1)
def arrow(c,x1,y1,x2,y2,col=CYAN,w=2):
    c.setStrokeColor(col); c.setLineWidth(w); c.line(x1,y1,x2,y2); ang=math.atan2(y2-y1,x2-x1)
    for d in (2.65,-2.65): c.line(x2,y2,x2-9*math.cos(ang+d),y2-9*math.sin(ang+d))
def route(c,points,col=CYAN,w=2,dash=True):
    c.setStrokeColor(col); c.setLineWidth(w)
    if dash: c.setDash(7,5)
    p=c.beginPath(); p.moveTo(*points[0])
    for q in points[1:]: p.lineTo(*q)
    c.drawPath(p,stroke=1,fill=0); c.setDash()
def line_icon(c,k,x,y,s=1,col=CYAN):
    c.setStrokeColor(col); c.setLineWidth(1.8*s)
    if k=='truck':
        c.roundRect(x,y+6*s,29*s,12*s,2*s,stroke=1,fill=0); c.rect(x+29*s,y+6*s,11*s,9*s,stroke=1,fill=0); c.circle(x+8*s,y+4*s,3*s,stroke=1,fill=0); c.circle(x+32*s,y+4*s,3*s,stroke=1,fill=0)
    elif k=='pin':
        c.circle(x+8*s,y+13*s,6*s,stroke=1,fill=0); c.line(x+4*s,y+8*s,x+8*s,y); c.line(x+12*s,y+8*s,x+8*s,y)
    elif k=='doc':
        c.roundRect(x,y,17*s,24*s,2*s,stroke=1,fill=0); c.line(x+4*s,y+16*s,x+13*s,y+16*s); c.line(x+4*s,y+10*s,x+13*s,y+10*s)
    elif k=='phone': c.roundRect(x,y,16*s,30*s,3*s,stroke=1,fill=0); c.circle(x+8*s,y+4*s,1*s,stroke=1,fill=0)
    elif k=='gear':
        c.circle(x+10*s,y+10*s,7*s,stroke=1,fill=0); c.circle(x+10*s,y+10*s,2*s,stroke=1,fill=0)
        for dx,dy in ((10,21),(10,-1),(-1,10),(21,10)): c.line(x+dx*s-2*s,y+dy*s,x+dx*s+2*s,y+dy*s)
    elif k=='chart':
        c.line(x,y,x,y+22*s); c.line(x,y,x+28*s,y)
        for dx,hh in ((5,7),(13,14),(21,20)): c.rect(x+dx*s,y,5*s,hh*s,stroke=1,fill=0)
def logo(c,k,cx,cy,w,h):
    if k=='cargus':
        rr(c,cx-w/2,cy-h/2,w,h,10,white); c.drawImage(CARGUS,cx-w/2+3,cy-h/2+3,w-6,h-6,preserveAspectRatio=True,anchor='c',mask='auto')
    else: c.drawImage(AUTO,cx-w/2,cy-h/2,w,h,preserveAspectRatio=True,anchor='c',mask='auto')
def slide_head(c,n,kicker,title,sub=''):
    tx(c,kicker.upper(),42,H-40,7,CYAN,True); tx(c,title,42,H-82,25,WHITE,True)
    if sub: tx(c,sub,42,H-106,10,MUTED)
    tx(c,'SAMIR ONE LOGISTIC',42,22,7,CYAN,True); tx(c,f'{n:02d} / 08',W-42,22,7,MUTED,True,'right')
def device_shadow(c,x,y,w,h,r=25):
    rr(c,x+10,y-10,w,h,r,Color(.0,.03,.07,.45)); rr(c,x,y,w,h,r,HexColor('#020A14'),HexColor('#33577E'),1.4)

def p1(c):
    fill(c,NAVY)
    im=Image.open(COVER); iw,ih=im.size; sc=max(W/iw,H/ih); nw,nh=iw*sc,ih*sc
    c.drawImage(COVER,W-nw,-8,nw,nh,mask='auto')
    c.setFillColor(Color(.02,.07,.13,.89)); c.rect(0,0,W*.56,H,stroke=0,fill=1)
    c.setFillColor(Color(.02,.07,.13,.38)); c.rect(W*.42,0,W*.58,H,stroke=0,fill=1)
    tx(c,'SAMIR ONE LOGISTIC',52,H-53,9,CYAN,True)
    for i,(s,col) in enumerate([('Transport.',WHITE),('Mai simplu.',WHITE),('Mai vizibil.',CYAN),('Mai profitabil.',WHITE)]): tx(c,s,52,H-155-i*42,32,col,True)
    tx(c,'De la comandă la profit, într-un singur sistem.',52,132,13,WHITE,True)
    tx(c,'01 / 08',W-52,28,8,WHITE,True,'right')

def p2(c):
    fill(c,NAVY); slide_head(c,2,'Ideea','Tot ce se întâmplă într-o cursă, într-un singur loc.','Comenzi, curse, șoferi, documente, costuri - aceeași imagine operațională.')
    # Sources are large, recognizable inputs
    logo(c,'cargus',144,370,150,60); logo(c,'auto',345,370,145,60)
    c.setStrokeColor(CYAN); c.setLineWidth(1.8); c.circle(505,370,14,stroke=1,fill=0); c.line(497,370,513,370); c.line(505,362,505,378); tx(c,'Comenzi directe',530,365,11,WHITE,True)
    for x in (144,345,505): arrow(c,x,332,520,275,CYAN,1.8)
    # Control Center is a product surface, not a label box
    device_shadow(c,250,98,540,166,22); rr(c,265,113,510,136,15,PANEL)
    tx(c,'SAMIR CONTROL CENTER',288,224,12,WHITE,True); tx(c,'CURSA #SO-1842',288,196,8,CYAN,True)
    tx(c,'Craiova  →  București',288,171,17,WHITE,True); line_icon(c,'truck',288,132,.8,MINT); tx(c,'În tranzit',328,139,10,MINT,True)
    # realistic small data strip
    for i,(lab,val,col) in enumerate([('ȘOFER','Ion Popescu',WHITE),('ETA','16:40',CYAN),('CMR','În așteptare',AMBER),('COST','Vizibil',MINT)]):
        x=500+i*67; tx(c,lab,x,190,6,MUTED,True); tx(c,val,x,173,7,col,True)
    tx(c,'TOT CE SE ÎNTÂMPLĂ ÎNTR-O CURSĂ, ÎNTR-UN SINGUR LOC.',W/2,57,11,CYAN,True,'center')

def p3(c):
    fill(c,INK); slide_head(c,3,'Fluxul unei curse','De la comandă la livrare','Cinci pași mari. Un singur flux de lucru.')
    y=272; c.setStrokeColor(Color(.18,.69,1,.2)); c.setLineWidth(20); c.line(90,y,870,y); c.setStrokeColor(CYAN); c.setLineWidth(2); c.line(90,y,870,y)
    stages=[('COMANDĂ','Document nou','doc'),('ALOCĂ','Șofer + camion','truck'),('URMĂREȘTE','Status live','pin'),('CMR','Document asociat','doc'),('FACTUREAZĂ','Totul pregătit','chart')]
    for i,(a,b,k) in enumerate(stages):
        x=120+i*180; c.setFillColor(PANEL); c.circle(x,y,54,stroke=0,fill=1); c.setStrokeColor(CYAN); c.setLineWidth(1.5); c.circle(x,y,54,stroke=1,fill=0)
        line_icon(c,k,x-13,y-14,1.25,MINT if i==1 else CYAN); tx(c,a,x,y-76,11,WHITE,True,'center'); tx(c,b,x,y-95,8,MUTED,False,'center')
    # end result visually bridges entire slide
    rr(c,180,88,600,59,18,Color(.06,.25,.42,.93),Color(.23,.76,1,.55),1); tx(c,'Mai puțină muncă manuală. Mai mult control asupra cursei.',W/2,110,15,WHITE,True,'center')

def p4(c):
    fill(c,NAVY); slide_head(c,4,'Control Center','Toate cursele. Live.','Hartă operațională: rute, camioane, status și ETA într-un singur ecran.')
    # Wide styled regional map
    rr(c,40,65,660,350,24,PANEL)
    c.setStrokeColor(Color(.3,.78,1,.12)); c.setLineWidth(.6)
    for i in range(1,9): c.line(55+i*72,82,55+i*72,400)
    for i in range(1,5): c.line(55,82+i*64,685,82+i*64)
    # Romania shape, schematic geographic object
    c.setFillColor(Color(.11,.39,.62,.55)); p=c.beginPath(); p.moveTo(190,170); p.lineTo(245,335); p.lineTo(388,370); p.lineTo(560,305); p.lineTo(602,191); p.lineTo(472,120); p.lineTo(316,137); p.close(); c.drawPath(p,stroke=0,fill=1)
    routes=[([(236,184),(341,245),(459,300)],MINT), ([(282,315),(390,260),(553,208)],CYAN), ([(190,248),(300,205),(474,163)],BLUE), ([(420,354),(500,278),(608,226)],AMBER)]
    for pts,col in routes:
        route(c,pts,col,2.5); dot(c,*pts[0],col,4); dot(c,*pts[-1],col,4)
    line_icon(c,'truck',329,234,.8,MINT); line_icon(c,'truck',382,248,.7,CYAN); line_icon(c,'truck',290,196,.65,BLUE); line_icon(c,'truck',489,269,.65,AMBER)
    for lab,x,y in [('Craiova',222,165),('București',444,309),('Cluj',275,324),('Timișoara',170,250),('Iași',572,205)]: tx(c,lab,x,y,8,CLOUD,True)
    # moving route tooltip
    rr(c,73,316,228,71,16,Color(.02,.1,.19,.96),Color(.19,.72,1,.4),1); tx(c,'CURSA #SO-1842',91,367,7,CYAN,True); tx(c,'Craiova → București',91,344,12,WHITE,True); tx(c,'OT-XX-XXX   •   ETA 16:40',91,325,8,MUTED)
    # quick-status rail
    rr(c,728,105,192,280,22,INK,Color(.23,.68,1,.28),1); tx(c,'12 CURSE ACTIVE',751,350,13,WHITE,True)
    for i,(n,l,col) in enumerate([('7','În tranzit',MINT),('3','La încărcare',AMBER),('2','La descărcare',CYAN)]):
        yy=290-i*63; dot(c,756,yy,col,6); tx(c,n,774,yy-6,20,col,True); tx(c,l,810,yy-3,10,WHITE,True)
    tx(c,'Concept demonstrativ',W-42,54,7,MUTED,False,'right')

def p5(c):
    fill(c,INK); slide_head(c,5,'Șofer + documente','Șoferul actualizează. Biroul vede.','Status instant și CMR asociat cursei, direct din teren.')
    # real-device treatment
    device_shadow(c,122,78,250,330,32); rr(c,136,94,222,298,22,HexColor('#102B48'))
    tx(c,'CURSA #1842',247,363,10,WHITE,True,'center'); tx(c,'Craiova → București',247,343,9,MUTED,False,'center')
    for i,(s,col) in enumerate([('AM AJUNS',CYAN),('AM ÎNCĂRCAT',CYAN),('AM PLECAT',CYAN),('AM LIVRAT',MINT)]):
        yy=292-i*43; rr(c,157,yy,180,31,8,Color(col.red,col.green,col.blue,.14),col,1); dot(c,174,yy+15,col,4); tx(c,s,188,yy+10,8,WHITE,True)
    rr(c,157,112,180,36,9,Color(.12,.43,.68,.34),CYAN,1); line_icon(c,'doc',174,120,.55,CYAN); tx(c,'ÎNCARCĂ CMR',202,125,8,WHITE,True)
    # CMR object and scan sequence
    rr(c,544,178,202,198,18,WHITE); tx(c,'CMR',645,340,15,INK,True,'center'); c.setStrokeColor(HexColor('#B6D5EA')); c.rect(577,218,136,87,stroke=1,fill=0)
    for i in range(4): c.line(597,286-i*15,693,286-i*15)
    c.setFillColor(MINT); c.circle(685,236,15,stroke=0,fill=1); tx(c,'✓',685,231,13,INK,True,'center')
    arrow(c,390,246,517,246,CYAN,2); tx(c,'Fotografie',401,266,9,MUTED,True); arrow(c,764,246,855,246,CYAN,2); rr(c,797,211,124,68,14,Color(.06,.24,.39,.96),MINT,1); tx(c,'CMR ASOCIAT',859,253,8,MINT,True,'center'); tx(c,'cursei #1842',859,234,8,WHITE,True,'center')
    tx(c,'Fotografiezi CMR-ul. Restul se întâmplă automat.',W/2,54,13,CYAN,True,'center')

def p6(c):
    fill(c,NAVY); slide_head(c,6,'Profitabilitate','Ce curse ne aduc profit?','Venit, cost și profit - explicate simplu pentru fiecare cursă.')
    # one dominant financial story
    rr(c,56,176,497,202,24,PANEL,Color(.22,.72,1,.25),1); tx(c,'CURSA #1842',83,342,8,CYAN,True); tx(c,'Craiova → București',83,313,19,WHITE,True)
    vals=[('VENIT','1.250 lei',BLUE),('COST','920 lei',WHITE),('PROFIT','+330 lei',MINT)]
    for i,(a,b,col) in enumerate(vals):
        x=83+i*151; tx(c,a,x,256,8,MUTED,True); tx(c,b,x,222,22,col,True)
        if i<2: arrow(c,x+111,236,x+136,236,Color(.22,.7,1,.55),1.5)
    tx(c,'DATE DEMONSTRATIVE',83,194,7,MUTED,True)
    # neutral partner comparison: visual only, no invented revenue values
    tx(c,'PROFITABILITATE PE PARTENER',614,357,10,WHITE,True)
    labels=[('cargus',MINT,237),('auto',CYAN,190),('direct',AMBER,145)]
    for lab,col,yy in labels:
        if lab=='cargus': logo(c,'cargus',655,yy+6,74,25)
        elif lab=='auto': logo(c,'auto',655,yy+6,78,25)
        else: tx(c,'Comenzi directe',614,yy+9,9,MUTED,True)
        rr(c,735,yy,143,12,6,Color(.08,.2,.34,.95)); rr(c,735,yy,93 if lab=='cargus' else 70 if lab=='auto' else 48,12,6,col)
    tx(c,'Exemplu de vizualizare - date demonstrative',614,112,7,MUTED)
    tx(c,'Profit / camion  •  Profit / rută  •  Profit / partener',W/2,57,10,CYAN,True,'center')

def p7(c):
    fill(c,INK); slide_head(c,7,'Portal client','Clientul verifică singur.','Status, ETA și documente - fără apel către dispecerat.')
    # monitor-like product mockup
    device_shadow(c,119,88,721,332,25); rr(c,135,104,689,299,16,WHITE)
    c.setFillColor(INK); c.roundRect(135,369,689,34,16,stroke=0,fill=1); c.rect(135,369,689,16,stroke=0,fill=1)
    dot(c,157,386,RED,3); dot(c,169,386,AMBER,3); dot(c,181,386,MINT,3); tx(c,'SAMIR ONE LOGISTIC',205,382,7,WHITE,True)
    tx(c,'Transport #SO-1842',165,341,10,INK,True); tx(c,'Craiova',165,300,17,INK,True); tx(c,'București',731,300,17,INK,True,'right')
    c.setStrokeColor(BLUE); c.setLineWidth(5); c.line(265,307,643,307); dot(c,456,307,MINT,10); line_icon(c,'truck',442,324,.65,INK)
    for x,a,b,col in [(165,'STATUS','ÎN TRANZIT',MINT),(400,'ETA','18:40',BLUE),(583,'DOCUMENTE','CMR + POD',CYAN)]:
        rr(c,x,175,148,78,13,Color(col.red,col.green,col.blue,.11)); tx(c,a,x+17,227,7,HexColor('#4E708D'),True); tx(c,b,x+17,198,14,HexColor('#0B4238') if col==MINT else INK,True)
    tx(c,'O experiență premium pentru client, sub brandul Samir One Logistic.',W/2,54,12,CYAN,True,'center')

def p8(c):
    fill(c,NAVY); tx(c,'SAMIR ONE LOGISTIC',W/2,H-49,8,CYAN,True,'center'); tx(c,'Mai puțină muncă administrativă.',W/2,H-108,24,WHITE,True,'center'); tx(c,'Mai mult control asupra fiecărei curse.',W/2,H-139,17,CYAN,True,'center')
    cx,cy=W/2,256; c.setFillColor(HexColor('#155991')); c.circle(cx,cy,70,stroke=0,fill=1); c.setStrokeColor(CYAN); c.setLineWidth(1.2); c.circle(cx,cy,70,stroke=1,fill=0)
    tx(c,'SAMIR',cx,266,17,WHITE,True,'center'); tx(c,'CONTROL CENTER',cx,246,8,WHITE,True,'center')
    items=[('COMENZI',cx-230,cy+95),('DISPECERAT',cx+230,cy+95),('TRACKING',cx-245,cy-14),('ȘOFER + DOCUMENTE',cx+245,cy-14),('COSTURI + PROFIT',cx-155,cy-118),('AUTOMATIZĂRI',cx+155,cy-118)]
    for lab,x,y in items:
        arrow(c,cx+(x-cx)*.37,cy+(y-cy)*.37,x-(x-cx)*.14,y-(y-cy)*.14,Color(.23,.7,1,.55),1)
        rr(c,x-67,y-18,134,36,12,PANEL2,Color(.22,.68,1,.27),1); tx(c,lab,x,y-3,7.5,WHITE,True,'center')
    rr(c,285,47,390,43,13,Color(.08,.33,.56,.95),CYAN,1); tx(c,'Următorul pas  →  Sesiune de descoperire digitală',W/2,62,10,WHITE,True,'center'); tx(c,'08 / 08',W-42,22,7,MUTED,True,'right')

def build():
    os.makedirs(os.path.dirname(OUT),exist_ok=True); c=canvas.Canvas(OUT,pagesize=(W,H),pageCompression=1)
    for f in (p1,p2,p3,p4,p5,p6,p7,p8): f(c); c.showPage()
    c.save()
if __name__=='__main__': build()
