from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from PIL import Image
import os, math

W,H=A4
OUT='output/pdf/samir-one-logistic-pitch-8-pagini.pdf'
COVER='tmp/assets/cover-truck.png'
CARGUS='tmp/assets/cargus-logo.png'
AUTO='tmp/assets/auto-total-logo.png'

NAVY=HexColor('#06172B'); INK=HexColor('#071426'); BLUE=HexColor('#1F72FF'); CYAN=HexColor('#38D6FF')
MINT=HexColor('#51DDAE'); CLOUD=HexColor('#EEF7FF'); SKY=HexColor('#DCEFFF'); MUTED=HexColor('#9AB2CB')
PANEL=HexColor('#102E51'); SLATE=HexColor('#173B64'); AMBER=HexColor('#FFBD45'); RED=HexColor('#FF6B7A')
pdfmetrics.registerFont(TTFont('A','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('AB','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))

def rect(c,x,y,w,h,fill,stroke=None,r=16,sw=1):
    c.setFillColor(fill)
    if stroke: c.setStrokeColor(stroke); c.setLineWidth(sw); c.roundRect(x,y,w,h,r,stroke=1,fill=1)
    else: c.roundRect(x,y,w,h,r,stroke=0,fill=1)
def text(c,s,x,y,sz=12,col=white,bold=False,align='left'):
    c.setFont('AB' if bold else 'A',sz); c.setFillColor(col)
    {'left':c.drawString,'center':c.drawCentredString,'right':c.drawRightString}[align](x,y,s)
def para(c,s,x,y,w,sz=12,col=white,bold=False,leading=None):
    font='AB' if bold else 'A'; leading=leading or sz*1.24; line=''; out=[]
    for word in s.split():
        trial=(line+' '+word).strip()
        if stringWidth(trial,font,sz)<=w: line=trial
        else: out.append(line); line=word
    if line: out.append(line)
    for i,line in enumerate(out): text(c,line,x,y-i*leading,sz,col,bold)
    return y-len(out)*leading
def footer(c,n,dark=True):
    text(c,'SAMIR ONE LOGISTIC',42,28,7,CYAN if dark else BLUE,True)
    text(c,f'{n:02d} / 08',W-42,28,7,MUTED if dark else HexColor('#5E7690'),True,'right')
def top(c,kicker,title,sub='',light=False):
    col=INK if light else white; muted=HexColor('#5D7993') if light else MUTED
    text(c,kicker,42,H-46,8,BLUE if light else CYAN,True)
    text(c,title,42,H-104,28,col,True)
    if sub: para(c,sub,42,H-129,W-84,11,muted)
def stroke_arrow(c,x1,y1,x2,y2,col=CYAN,w=2):
    c.setStrokeColor(col); c.setLineWidth(w); c.line(x1,y1,x2,y2); a=math.atan2(y2-y1,x2-x1)
    for d in (2.62,-2.62): c.line(x2,y2,x2-9*math.cos(a+d),y2-9*math.sin(a+d))
def dot(c,x,y,col=CYAN,r=4): c.setFillColor(col); c.circle(x,y,r,1,0)
def logo(c,which,cx,cy,w,h):
    if which=='cargus':
        rect(c,cx-w/2,cy-h/2,w,h,white,r=10)
        c.drawImage(CARGUS,cx-w/2+3,cy-h/2+3,w-6,h-6,preserveAspectRatio=True,anchor='c',mask='auto')
    else: c.drawImage(AUTO,cx-w/2,cy-h/2,w,h,preserveAspectRatio=True,anchor='c',mask='auto')
def truck(c,x,y,s=1,col=CYAN):
    c.setStrokeColor(col); c.setLineWidth(2*s); c.roundRect(x,y+7*s,30*s,13*s,2*s,stroke=1,fill=0); c.rect(x+30*s,y+7*s,12*s,10*s,stroke=1,fill=0)
    c.circle(x+9*s,y+5*s,3*s,0,1); c.circle(x+34*s,y+5*s,3*s,0,1)
def pin(c,x,y,s=1,col=CYAN):
    c.setStrokeColor(col); c.setLineWidth(2*s); c.circle(x+8*s,y+13*s,6*s,0,1); c.line(x+4*s,y+8*s,x+8*s,y); c.line(x+12*s,y+8*s,x+8*s,y)
def doc(c,x,y,s=1,col=CYAN):
    c.setStrokeColor(col); c.setLineWidth(1.7*s); c.roundRect(x,y,17*s,24*s,2*s,stroke=1,fill=0)
    c.line(x+4*s,y+16*s,x+13*s,y+16*s); c.line(x+4*s,y+10*s,x+13*s,y+10*s)
def phone_frame(c,x,y,w,h):
    rect(c,x,y,w,h,HexColor('#020B16'),HexColor('#47698E'),r=28,sw=1.2); rect(c,x+9,y+10,w-18,h-20,HexColor('#102C4B'),r=21)
    c.setFillColor(HexColor('#516A86')); c.roundRect(x+w*.38,y+h-14,w*.24,4,2,stroke=0,fill=1)
def map_grid(c,x,y,w,h,light=False):
    rect(c,x,y,w,h,HexColor('#0C2745') if not light else HexColor('#D8EEFF'),r=22)
    c.setStrokeColor(Color(.38,.76,1,.14) if not light else Color(.08,.4,.7,.15)); c.setLineWidth(.6)
    for i in range(1,6): c.line(x+i*w/6,y+12,x+i*w/6,y+h-12)
    for i in range(1,5): c.line(x+12,y+i*h/5,x+w-12,y+i*h/5)
    # stylized Romania-Europa landmass
    c.setFillColor(Color(.12,.37,.58,.55) if not light else Color(.46,.75,.94,.38)); p=c.beginPath(); p.moveTo(x+w*.20,y+h*.29); p.lineTo(x+w*.31,y+h*.70); p.lineTo(x+w*.49,y+h*.82); p.lineTo(x+w*.67,y+h*.65); p.lineTo(x+w*.77,y+h*.35); p.lineTo(x+w*.58,y+h*.18); p.lineTo(x+w*.37,y+h*.20); p.close(); c.drawPath(p,1,0)
def route(c,pts,col=CYAN,w=2):
    c.setStrokeColor(col); c.setLineWidth(w); c.setDash(7,4); p=c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    c.drawPath(p,1,0); c.setDash()
    for i,q in enumerate(pts): dot(c,*q,MINT if i==len(pts)-1 else col,5)

def p1(c):
    c.setFillColor(NAVY); c.rect(0,0,W,H,stroke=0,fill=1)
    im=Image.open(COVER); iw,ih=im.size; scale=max(W*.72/iw,H*.86/ih); nw,nh=iw*scale,ih*scale
    c.drawImage(COVER,W-nw+70,-10,nw,nh,mask='auto')
    c.setFillColor(Color(.02,.07,.13,.88)); c.rect(0,0,W*.68,H,stroke=0,fill=1); c.setFillColor(Color(.02,.08,.15,.4)); c.rect(W*.45,0,W*.55,H,stroke=0,fill=1)
    text(c,'SAMIR ONE LOGISTIC',42,H-66,9,CYAN,True)
    text(c,'Transport.',42,H-186,38,white,True); text(c,'Mai simplu.',42,H-232,38,white,True)
    text(c,'Mai vizibil.',42,H-278,38,CYAN,True); text(c,'Mai profitabil.',42,H-324,38,white,True)
    para(c,'O propunere de digitalizare pentru fiecare cursă.',42,H-374,260,13,CLOUD)
    rect(c,42,98,250,70,Color(.04,.16,.29,.88),r=16); text(c,'O CURSĂ. O SINGURĂ IMAGINE.',60,139,8,CYAN,True); text(c,'De la comandă până la profit.',60,116,12,white,True)
    footer(c,1)

def p2(c):
    c.setFillColor(CLOUD); c.rect(0,0,W,H,stroke=0,fill=1)
    text(c,'IDEEA',42,H-46,8,BLUE,True)
    text(c,'Tot ce se întâmplă într-o cursă.',42,H-104,26,INK,True)
    text(c,'Într-un singur loc.',42,H-138,26,INK,True)
    text(c,'De la comandă până la profit - fără informație împrăștiată.',42,H-165,11,HexColor('#5D7993'))
    # input lane
    rect(c,42,530,W-84,82,white,HexColor('#C6E0F5'),r=18)
    logo(c,'cargus',115,571,112,48); logo(c,'auto',279,571,104,48)
    c.setStrokeColor(BLUE); c.setLineWidth(1.6); c.circle(430,571,13,0,1); c.line(423,571,437,571); c.line(430,564,430,578)
    text(c,'Comenzi directe',454,566,10,INK,True)
    stroke_arrow(c,112,526,W/2,468,BLUE,1.8); stroke_arrow(c,279,526,W/2,468,BLUE,1.8); stroke_arrow(c,432,549,W/2,468,BLUE,1.8)
    # central dominant product
    rect(c,57,274,W-114,170,INK,None,r=26); text(c,'SAMIR CONTROL CENTER',W/2,404,18,white,True,'center'); text(c,'o singură cursă, urmărită cap-coadă',W/2,381,9,MUTED,False,'center')
    c.setStrokeColor(Color(.22,.77,1,.22)); c.line(81,356,W-81,356)
    items=[('COMANDĂ','SO-1842'),('CURSĂ','Craiova → București'),('STATUS','În tranzit'),('CMR','Așteptat'),('PROFIT','Vizibil')]
    for i,(a,b) in enumerate(items):
        x=82+i*87; text(c,a,x,329,6,MUTED,True); text(c,b,x,307,8,CLOUD,True)
        if i<4: stroke_arrow(c,x+62,315,x+79,315,CYAN,1)
    text(c,'Tot ce se întâmplă într-o cursă, într-un singur loc.',W/2,210,16,INK,True,'center')
    footer(c,2,False)

def p3(c):
    c.setFillColor(NAVY); c.rect(0,0,W,H,stroke=0,fill=1); top(c,'FLUXUL CURSEI','De la comandă la livrare','O singură bandă vizuală. O singură poveste.')
    # central visual route band
    y=430; c.setStrokeColor(Color(.22,.82,1,.2)); c.setLineWidth(18); c.line(62,y,W-62,y); c.setStrokeColor(CYAN); c.setLineWidth(2); c.line(62,y,W-62,y)
    steps=[('COMANDĂ','Cursă nouă','doc'),('ALOCĂ','Șofer + camion','truck'),('URMĂREȘTE','Status live','pin'),('CMR','Documente','doc'),('FACTUREAZĂ','Totul pregătit','doc')]
    for i,(k,b,ic) in enumerate(steps):
        x=72+i*112; c.setFillColor(INK); c.circle(x,y,32,1,0); c.setStrokeColor(CYAN); c.setLineWidth(2); c.circle(x,y,32,0,1)
        if ic=='truck': truck(c,x-21,y-12,.9,MINT)
        elif ic=='pin': pin(c,x-9,y-16,.9,CYAN)
        else: doc(c,x-8,y-12,.9,CYAN)
        text(c,k,x,y-60,8,CYAN,True,'center'); para(c,b,x-49,y-78,98,8,CLOUD,True,10)
    # a delivery ticket below
    rect(c,68,163,W-136,148,Color(.06,.18,.32,.96),HexColor('#1F70B5'),r=20)
    text(c,'CURSA #SO-1842',93,274,9,CYAN,True); text(c,'Craiova  →  București',93,241,22,white,True); truck(c,92,196,1.25,MINT); text(c,'În tranzit',152,205,12,MINT,True)
    text(c,'Mai puțină muncă manuală.',W/2,104,17,white,True,'center'); footer(c,3)

def p4(c):
    c.setFillColor(INK); c.rect(0,0,W,H,stroke=0,fill=1); top(c,'CONTROL CENTER','Toate cursele. Live.','O hartă care arată exact ce se întâmplă acum.')
    map_grid(c,30,164,W-60,520)
    x,y,w,h=30,164,W-60,520
    pts=[(x+w*.23,y+h*.24),(x+w*.46,y+h*.46),(x+w*.63,y+h*.64)]
    route(c,pts,CYAN,3); truck(c,pts[1][0]-19,pts[1][1]-14,1,MINT)
    # route focus overlay
    rect(c,52,468,245,157,Color(.025,.11,.21,.94),Color(.22,.72,1,.35),r=16)
    text(c,'CURSA #SO-1842',70,597,8,CYAN,True); text(c,'Craiova → București',70,568,15,white,True); truck(c,70,520,.78,MINT); text(c,'OT-XX-XXX',110,530,9,CLOUD,True); text(c,'Ion Popescu',70,497,9,CLOUD,True); dot(c,70,478,MINT,4); text(c,'În tranzit',82,474,9,MINT,True); text(c,'ETA 16:40',211,474,9,CLOUD,True)
    # activity panel
    rect(c,329,272,206,235,Color(.025,.11,.21,.94),Color(.22,.72,1,.28),r=16)
    text(c,'12 CURSE ACTIVE',350,477,11,white,True)
    status=[('7','În tranzit',MINT),('3','La încărcare',AMBER),('2','La descărcare',CYAN)]
    for i,(n,l,col) in enumerate(status):
        yy=425-i*49; dot(c,354,yy,col,5); text(c,n,371,yy-4,16,col,True); text(c,l,399,yy-3,9,CLOUD,True)
    text(c,'Concept demonstrativ',W-42,89,7,MUTED,False,'right'); footer(c,4)

def p5(c):
    c.setFillColor(HexColor('#0A2542')); c.rect(0,0,W,H,stroke=0,fill=1); top(c,'ȘOFER + DOCUMENTE','Șoferul actualizează. Biroul vede.','O actualizare simplă, în momentul în care se întâmplă.')
    phone_frame(c,54,150,205,450)
    text(c,'Cursa de azi',156,554,11,white,True,'center'); text(c,'Craiova → București',156,534,8,MUTED,False,'center')
    actions=[('Am ajuns',CYAN),('Am încărcat',CYAN),('Am plecat',CYAN),('Am livrat',MINT)]
    for i,(lab,col) in enumerate(actions):
        yy=466-i*55; rect(c,75,yy,163,38,Color(col.red,col.green,col.blue,.15),col,r=10); dot(c,94,yy+19,col,5); text(c,lab,108,yy+14,9,white,True)
    rect(c,75,203,163,40,Color(.12,.43,.68,.42),CYAN,r=10); doc(c,91,211,.56,CYAN); text(c,'Fotografiază CMR',118,216,8,white,True)
    # cMR as visual object and flow
    rect(c,314,356,205,225,white,None,r=24); text(c,'CMR',416,541,13,INK,True,'center'); c.setStrokeColor(HexColor('#B8D6EB')); c.rect(344,400,145,109,stroke=1,fill=0)
    for i in range(4): c.line(365,484-i*20,465,484-i*20)
    doc(c,330,269,.9,CYAN); stroke_arrow(c,365,282,410,282,CYAN,2); c.setFillColor(MINT); c.circle(440,282,20,1,0); text(c,'✓',440,276,15,INK,True,'center'); stroke_arrow(c,467,282,502,282,CYAN,2); text(c,'FACTURARE',516,277,8,CLOUD,True,'right')
    text(c,'Fotografiezi CMR-ul. Restul se întâmplă automat.',W/2,104,15,white,True,'center'); footer(c,5)

def p6(c):
    c.setFillColor(CLOUD); c.rect(0,0,W,H,stroke=0,fill=1); top(c,'PROFITABILITATE','Ce curse ne aduc profit?','Un singur ecran explică venitul, costul și profitul unei curse.',True)
    rect(c,42,375,W-84,216,white,HexColor('#B9D7EA'),r=22)
    text(c,'CURSA #1842',70,559,8,BLUE,True); logo(c,'cargus',455,546,88,38)
    text(c,'Craiova → București',70,518,20,INK,True); text(c,'Date demonstrative',70,494,8,HexColor('#617C94'))
    vals=[('VENIT','1.250 lei',BLUE),('COST','920 lei',INK),('PROFIT','+330 lei',MINT)]
    for i,(a,b,col) in enumerate(vals):
        x=70+i*151; text(c,a,x,449,8,HexColor('#607D97'),True); text(c,b,x,418,19,col,True)
    text(c,'Profit comparat pe partener',42,324,13,INK,True)
    # comparation rather than generic widgets
    rect(c,42,138,W-84,151,INK,None,r=20); text(c,'CARGUS',72,247,8,CLOUD,True); c.setFillColor(MINT); c.roundRect(165,237,225,12,6,stroke=0,fill=1); text(c,'+ 330 lei',425,239,10,MINT,True)
    text(c,'AUTO TOTAL',72,205,8,CLOUD,True); c.setFillColor(CYAN); c.roundRect(165,195,170,12,6,stroke=0,fill=1); text(c,'+ 250 lei',425,197,10,CYAN,True)
    text(c,'COMENZI DIRECTE',72,163,8,CLOUD,True); c.setFillColor(AMBER); c.roundRect(165,153,125,12,6,stroke=0,fill=1); text(c,'+ 180 lei',425,155,10,AMBER,True)
    text(c,'Profit / camion   •   Profit / rută   •   Profit / partener',W/2,93,9,HexColor('#4F6C85'),True,'center'); footer(c,6,False)

def p7(c):
    c.setFillColor(NAVY); c.rect(0,0,W,H,stroke=0,fill=1); top(c,'PORTAL CLIENT','Clientul verifică singur.','Status, ETA și documente - fără apel către dispecerat.')
    # refined live portal, dominant object
    rect(c,39,177,W-78,466,white,None,r=24)
    c.setFillColor(INK); c.roundRect(39,600,W-78,43,24,stroke=0,fill=1); c.rect(39,600,W-78,20,stroke=0,fill=1)
    dot(c,62,621,RED,3); dot(c,74,621,AMBER,3); dot(c,86,621,MINT,3); text(c,'SAMIR ONE LOGISTIC',112,616,8,white,True)
    text(c,'Transport #SO-1842',70,558,11,INK,True); text(c,'Craiova',70,515,17,INK,True); text(c,'Berlin',445,515,17,INK,True,'right')
    c.setStrokeColor(BLUE); c.setLineWidth(5); c.line(144,523,425,523); dot(c,292,523,MINT,10); truck(c,271,542,.7,INK)
    rect(c,70,390,165,78,HexColor('#E8FFF6'),None,r=14); text(c,'STATUS',89,443,7,HexColor('#4B7A68'),True); text(c,'ÎN TRANZIT',89,416,16,HexColor('#18875E'),True)
    rect(c,255,390,123,78,SKY,None,r=14); text(c,'ETA',273,443,7,HexColor('#5E7E9A'),True); text(c,'18:40',273,416,16,INK,True)
    rect(c,398,390,117,78,HexColor('#F2F6FA'),None,r=14); text(c,'ȘOFER',416,443,7,HexColor('#5E7E9A'),True); text(c,'M. Popescu',416,416,10,INK,True)
    text(c,'DOCUMENTE',70,347,8,HexColor('#5E7E9A'),True); doc(c,70,296,.7,MINT); text(c,'CMR disponibil',97,303,10,INK,True); doc(c,258,296,.7,MINT); text(c,'POD disponibil',285,303,10,INK,True)
    text(c,'Portal Samir - o experiență premium pentru client.',W/2,112,14,white,True,'center'); footer(c,7)

def p8(c):
    c.setFillColor(INK); c.rect(0,0,W,H,stroke=0,fill=1); c.setFillColor(Color(.12,.45,1,.14)); c.circle(W/2,H/2,210,stroke=0,fill=1)
    text(c,'SAMIR ONE LOGISTIC',W/2,H-110,9,CYAN,True,'center'); text(c,'Mai puțină administrare.',W/2,H-210,28,white,True,'center'); text(c,'Mai mult control asupra transportului.',W/2,H-248,19,CYAN,True,'center')
    cx,cy=W/2,348; c.setFillColor(HexColor('#1A5A96')); c.circle(cx,cy,73,1,0); c.setStrokeColor(CYAN); c.setLineWidth(1.3); c.circle(cx,cy,73,0,1); text(c,'SAMIR',cx,357,16,white,True,'center'); text(c,'CONTROL CENTER',cx,337,9,CLOUD,True,'center')
    items=[('COMENZI',cx-182,cy+112),('ALOCĂRI',cx+182,cy+112),('TRACKING',cx-205,cy),('DOCUMENTE',cx+205,cy),('COSTURI',cx-157,cy-120),('PROFIT',cx+157,cy-120),('ȘOFER',cx-74,cy-168),('AUTOMATIZĂRI',cx+74,cy-168)]
    for lab,x,y in items:
        stroke_arrow(c,cx+(x-cx)*.42,cy+(y-cy)*.42,x-(x-cx)*.13,y-(y-cy)*.13,Color(.28,.75,1,.5),1)
        rect(c,x-57,y-20,114,40,Color(.06,.19,.33,.96),Color(.22,.64,1,.22),r=13); text(c,lab,x,y-3,7.5,white,True,'center')
    rect(c,72,87,W-144,52,Color(.08,.31,.52,.96),CYAN,r=15); text(c,'Următorul pas  →  Sesiune de descoperire digitală',W/2,106,11,white,True,'center'); footer(c,8)

def build():
    os.makedirs(os.path.dirname(OUT),exist_ok=True); c=canvas.Canvas(OUT,pagesize=A4,pageCompression=1)
    for f in (p1,p2,p3,p4,p5,p6,p7,p8): f(c); c.showPage()
    c.save()
if __name__=='__main__': build()
