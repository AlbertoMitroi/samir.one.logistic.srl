from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from PIL import Image
import os

W, H = A4
OUT = 'output/pdf/samir-one-logistic-transformare-digitala.pdf'
ASSET = 'tmp/assets/cover-truck.png'
CARGUS_LOGO = 'tmp/assets/cargus-logo.png'
AUTO_TOTAL_LOGO = 'tmp/assets/auto-total-logo.png'

NAVY = HexColor('#07182D')
NAVY2 = HexColor('#0D2542')
PANEL = HexColor('#102C4C')
BLUE = HexColor('#2176FF')
CYAN = HexColor('#42D9FF')
MINT = HexColor('#52E0AE')
WHITE = HexColor('#F7FBFF')
MUTED = HexColor('#9BB2CC')
SOFT = HexColor('#DDEBFA')
GOLD = HexColor('#F9C65B')
RED = HexColor('#FF7A8A')

pdfmetrics.registerFont(TTFont('Arial', '/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialB', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'))

def rr(c,x,y,w,h,r=16,fill=PANEL,stroke=None,sw=1):
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke); c.setLineWidth(sw)
        c.roundRect(x,y,w,h,r,fill=1,stroke=1)
    else: c.roundRect(x,y,w,h,r,fill=1,stroke=0)

def txt(c,s,x,y,size=12,color=WHITE,bold=False,align='left'):
    c.setFont('ArialB' if bold else 'Arial', size); c.setFillColor(color)
    if align=='center': c.drawCentredString(x,y,s)
    elif align=='right': c.drawRightString(x,y,s)
    else: c.drawString(x,y,s)

def wrap(c,s,x,y,width,size=12,leading=None,color=WHITE,bold=False):
    leading = leading or size*1.27
    words=s.split(); line=''; lines=[]
    font='ArialB' if bold else 'Arial'
    for word in words:
        test=(line+' '+word).strip()
        if stringWidth(test,font,size) <= width: line=test
        else: lines.append(line); line=word
    if line: lines.append(line)
    for i,line in enumerate(lines): txt(c,line,x,y-i*leading,size,color,bold)
    return y-len(lines)*leading

def pill(c,s,x,y,fill=Color(.1,.25,.42),color=CYAN):
    w=stringWidth(s,'ArialB',7)+18
    rr(c,x,y,w,18,9,fill)
    txt(c,s,x+9,y+6,7,color,True)
    return w

def page(c,n,kicker='SAMIR ONE LOGISTIC'):
    c.setFillColor(NAVY); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(Color(.13,.46,1,.08)); c.circle(W+45,H-25,190,fill=1,stroke=0)
    c.setFillColor(Color(.25,.85,1,.06)); c.circle(-50,70,135,fill=1,stroke=0)
    txt(c,kicker,42,H-38,8,CYAN,True)
    c.setStrokeColor(Color(.35,.7,1,.25)); c.line(42,H-50,W-42,H-50)
    txt(c,f'{n:02d} / 15',W-42,28,8,MUTED,True,'right')

def title(c,h,sub=None):
    txt(c,h,42,H-105,28,WHITE,True)
    if sub: wrap(c,sub,42,H-128,W-84,11,15,MUTED)

def dot(c,x,y,color=CYAN,r=4):
    c.setFillColor(color); c.circle(x,y,r,fill=1,stroke=0)

def line_arrow(c,x1,y1,x2,y2,color=CYAN,width=2):
    c.setStrokeColor(color); c.setLineWidth(width); c.line(x1,y1,x2,y2)
    import math
    a=math.atan2(y2-y1,x2-x1)
    for d in (2.65,-2.65): c.line(x2,y2,x2-9*math.cos(a+d),y2-9*math.sin(a+d))

def icon(c,kind,x,y,scale=1,color=CYAN):
    c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(1.7*scale)
    if kind=='truck':
        c.roundRect(x,y+4*scale,27*scale,11*scale,2*scale,fill=0,stroke=1)
        c.rect(x+27*scale,y+4*scale,11*scale,9*scale,fill=0,stroke=1)
        c.circle(x+8*scale,y+3*scale,3*scale,fill=0,stroke=1); c.circle(x+31*scale,y+3*scale,3*scale,fill=0,stroke=1)
    elif kind=='pin':
        c.circle(x+8*scale,y+12*scale,6*scale,fill=0,stroke=1); c.line(x+4*scale,y+7*scale,x+8*scale,y); c.line(x+12*scale,y+7*scale,x+8*scale,y)
    elif kind=='doc':
        c.roundRect(x,y,18*scale,24*scale,2*scale,fill=0,stroke=1); c.line(x+4*scale,y+16*scale,x+14*scale,y+16*scale); c.line(x+4*scale,y+10*scale,x+14*scale,y+10*scale)
    elif kind=='phone':
        c.roundRect(x,y,16*scale,30*scale,3*scale,fill=0,stroke=1); c.circle(x+8*scale,y+4*scale,1*scale,fill=1,stroke=0)
    elif kind=='chart':
        c.line(x,y,x,y+22*scale); c.line(x,y,x+28*scale,y)
        for dx,hh in ((5,7),(13,14),(21,20)): c.rect(x+dx*scale,y,5*scale,hh*scale,fill=0,stroke=1)
    elif kind=='user':
        c.circle(x+10*scale,y+18*scale,5*scale,fill=0,stroke=1)
        c.arc(x+2*scale,y,x+18*scale,y+15*scale,0,180)
    elif kind=='gear':
        c.circle(x+10*scale,y+10*scale,7*scale,fill=0,stroke=1); c.circle(x+10*scale,y+10*scale,2*scale,fill=1,stroke=0)
        for dx,dy in ((10,21),(10,-1),(-1,10),(21,10)): c.rect(x+dx*scale-2,y+dy*scale-2,4*scale,4*scale,fill=1,stroke=0)
    elif kind=='check':
        c.setLineWidth(2.5*scale); c.line(x,y+7*scale,x+6*scale,y+1*scale); c.line(x+6*scale,y+1*scale,x+17*scale,y+15*scale)

def status(c,label,x,y,color):
    rr(c,x,y,78,19,9,Color(color.red,color.green,color.blue,.12),color)
    dot(c,x+10,y+9.5,color,3); txt(c,label,x+18,y+6,7,color,True)

def info_card(c,label,value,x,y,w,h,accent=CYAN,kind=None,small=False):
    rr(c,x,y,w,h,14,Color(.06,.17,.30,.95),Color(.28,.56,.82,.18))
    c.setFillColor(accent); c.rect(x,y,w,4,fill=1,stroke=0)
    if kind: icon(c,kind,x+16,y+h-39,.7,accent)
    tx=x+16 if not kind else x+48
    txt(c,label,tx,y+h-23,8,MUTED,True)
    txt(c,value,x+16,y+18,18 if not small else 13,WHITE,True)

def mock_map(c,x,y,w,h):
    rr(c,x,y,w,h,18,Color(.055,.15,.27,.96),Color(.2,.5,.8,.2))
    c.setStrokeColor(Color(.3,.7,1,.14)); c.setLineWidth(.6)
    for i in range(1,5): c.line(x+i*w/5,y+10,x+i*w/5,y+h-10)
    for i in range(1,4): c.line(x+10,y+i*h/4,x+w-10,y+i*h/4)
    pts=[(x+w*.18,y+h*.2),(x+w*.32,y+h*.62),(x+w*.55,y+h*.48),(x+w*.77,y+h*.78)]
    c.setStrokeColor(CYAN); c.setLineWidth(2); c.setDash(5,4)
    p=c.beginPath(); p.moveTo(*pts[0]);
    for pnt in pts[1:]: p.lineTo(*pnt)
    c.drawPath(p,stroke=1,fill=0); c.setDash()
    for j,pnt in enumerate(pts): dot(c,*pnt, MINT if j==3 else CYAN,5)
    icon(c,'truck',x+w*.51,y+h*.44,.5,WHITE)

def browser(c,x,y,w,h,title='SAMIR PORTAL'):
    rr(c,x,y,w,h,17,Color(.96,.985,1,1))
    c.setFillColor(NAVY2); c.roundRect(x,y+h-35,w,35,17,fill=1,stroke=0); c.rect(x,y+h-18,w,18,fill=1,stroke=0)
    dot(c,x+16,y+h-18,RED,3); dot(c,x+26,y+h-18,GOLD,3); dot(c,x+36,y+h-18,MINT,3)
    txt(c,title,x+55,y+h-22,8,WHITE,True)
    c.setFillColor(SOFT); c.rect(x+15,y+16,w*.24,h-65,fill=1,stroke=0)
    c.setFillColor(HexColor('#C7E5FA')); c.roundRect(x+w*.31,y+h*.42,w*.59,h*.32,12,fill=1,stroke=0)
    c.setFillColor(BLUE); c.circle(x+w*.58,y+h*.58,18,fill=1,stroke=0); c.setFillColor(CYAN); c.circle(x+w*.73,y+h*.5,10,fill=1,stroke=0)
    for i in range(3): rr(c,x+w*.31,y+25+i*35,w*.18,24,7,WHITE); rr(c,x+w*.54,y+25+i*35,w*.36,24,7,WHITE)

def partner_logo(c, name, cx, cy, width, height):
    """Place supplied logo assets inside the partner cards without altering them."""
    if name == 'cargus':
        rr(c, cx-width/2, cy-height/2, width, height, 8, white)
        c.drawImage(CARGUS_LOGO, cx-width/2+2, cy-height/2+2, width-4, height-4,
                    preserveAspectRatio=True, anchor='c', mask='auto')
    elif name == 'auto_total':
        c.drawImage(AUTO_TOTAL_LOGO, cx-width/2, cy-height/2, width, height,
                    preserveAspectRatio=True, anchor='c', mask='auto')

def phone(c,x,y,w,h):
    rr(c,x,y,w,h,27,HexColor('#020A14'),HexColor('#385B85'),1.3)
    rr(c,x+9,y+10,w-18,h-20,20,Color(.08,.18,.31,1))
    rr(c,x+w*.38,y+h-15,w*.24,4,2,HexColor('#506782'))

def cover(c):
    c.setFillColor(NAVY); c.rect(0,0,W,H,fill=1,stroke=0)
    # crop cover art to bleed right and bottom
    im=Image.open(ASSET); iw,ih=im.size
    target_w,target_h=W*.83,H*.82
    ratio=max(target_w/iw,target_h/ih); nw,nh=iw*ratio,ih*ratio
    ox=W-nw+50; oy=-5
    c.drawImage(ASSET,ox,oy,nw,nh,mask='auto')
    c.setFillColor(Color(.02,.07,.14,.86)); c.rect(0,0,W*.70,H,fill=1,stroke=0)
    c.setFillColor(Color(.02,.07,.14,.52)); c.rect(W*.45,0,W*.55,H,fill=1,stroke=0)
    c.setFillColor(Color(.1,.65,1,.22)); c.circle(W-15,H-75,170,fill=1,stroke=0)
    pill(c,'PREZENTARE CONCEPT',42,H-85,Color(.1,.4,.65,.48),CYAN)
    txt(c,'Transformare',42,H-166,33,WHITE,True)
    txt(c,'digitală pentru',42,H-207,33,WHITE,True)
    txt(c,'Samir One Logistic',42,H-248,33,CYAN,True)
    wrap(c,'Mai mult control. Mai puțină muncă. Decizii mai bune.',42,H-292,260,14,19,SOFT)
    c.setFillColor(Color(.05,.13,.24,.75)); c.roundRect(42,105,238,72,15,fill=1,stroke=0)
    txt(c,'CONTROL / VIZIBILITATE / DECIZII',58,150,8,CYAN,True)
    txt(c,'O operațiune clară, într-un singur loc.',58,127,11,WHITE,True)
    txt(c,'SAMIR ONE LOGISTIC',42,42,8,MUTED,True)
    txt(c,'01',W-42,42,8,WHITE,True,'right')

def p2(c):
    page(c,2); title(c,'Totul într-un singur loc','Comenzile intră. Samir le gestionează. Totul este vizibil.')
    sources=[('cargus',86,H-218),('auto_total',W-86,H-218),('direct',W/2,H-294)]
    for label,x,y in sources:
        card_w = 144 if label == 'direct' else 112
        card_h = 44 if label == 'direct' else 40
        rr(c,x-card_w/2,y-card_h/2,card_w,card_h,14,Color(.07,.18,.31,.96),Color(.23,.55,.85,.35))
        if label == 'cargus':
            partner_logo(c, 'cargus', x, y, 92, 34)
        elif label == 'auto_total':
            partner_logo(c, 'auto_total', x, y, 90, 34)
        else:
            c.setStrokeColor(CYAN); c.setLineWidth(1.4); c.circle(x-47,y,6,fill=0,stroke=1)
            c.line(x-50,y,x-44,y); c.line(x-47,y-3,x-47,y+3)
            txt(c,'COMENZI DIRECTE',x+7,y-3,8.5,WHITE,True,'center')
        line_arrow(c,x,y-card_h/2,W/2,H-376,CYAN,1.4)
    rr(c,58,H-480,W-116,86,22,Color(.08,.30,.51,.98),CYAN,1.2)
    txt(c,'SAMIR CENTRU DE CONTROL',W/2,H-440,18,WHITE,True,'center'); txt(c,'un singur ecran pentru operațiune',W/2,H-462,9,SOFT,False,'center')
    line_arrow(c,W/2,H-480,W/2,H-530,CYAN,2)
    items=[('Curse','truck'),('Șoferi','user'),('Tracking','pin'),('Documente','doc'),('Costuri','chart')]
    for i,(lab,ic) in enumerate(items):
        x=34+i*106; rr(c,x,150,92,95,16,Color(.06,.17,.30,.96)); icon(c,ic,x+29,193,.85,CYAN); txt(c,lab,x+46,167,9,WHITE,True,'center')
    txt(c,'O singură imagine. Toată operațiunea.',W/2,100,14,WHITE,True,'center')

def p3(c):
    page(c,3); title(c,'Comenzile intră automat','Mai puțină introducere manuală. Mai mult timp pentru operațiune.')
    chain=[('cargus',64,''),('auto_total',141,''),('Comenzi directe',218,'+'),('SAMIR',295,'S')]
    for i,(lab,x,sym) in enumerate(chain):
        rr(c,x-31,H-285,62,62,18,Color(.08,.22,.38,.96),CYAN if i==3 else Color(.28,.55,.82,.6))
        if lab == 'cargus':
            partner_logo(c, 'cargus', x, H-254, 54, 29)
        elif lab == 'auto_total':
            partner_logo(c, 'auto_total', x, H-254, 53, 29)
        else:
            txt(c,sym,x,H-262,18,CYAN if i!=3 else WHITE,True,'center')
            txt(c,lab,x,H-304,8,WHITE,True,'center')
        if i<3: line_arrow(c,x+34,H-254,chain[i+1][1]-34,H-254,CYAN,1.5)
    rr(c,55,H-434,W-110,90,18,Color(.06,.18,.32,.98),Color(.25,.68,1,.35))
    icon(c,'truck',78,H-391,.9,MINT); txt(c,'Cursă creată',128,H-380,19,WHITE,True); txt(c,'gata de urmărit și gestionat',128,H-405,10,MUTED)
    note='Integrare prin API, email, fișiere sau alte metode disponibile.'
    txt(c,note,W/2,220,8,MUTED,False,'center')
    for i,(a,b,col) in enumerate([('Mai rapid','fără pași repetați',MINT),('Mai puține greșeli','date mai clare',CYAN),('Totul centralizat','într-un singur flux',BLUE)]):
        x=42+i*176; rr(c,x,112,158,76,14,Color(.06,.17,.30,.97)); dot(c,x+18,163,col,5); txt(c,a,x+31,158,10,WHITE,True); txt(c,b,x+18,132,8,MUTED)

def p4(c):
    page(c,4); title(c,'Vedem toate cursele','Un singur ecran. Toată operațiunea.'); mock_map(c,42,337,W-84,195)
    info_card(c,'CURSE ACTIVE','32',42,555,120,80,CYAN,'truck'); info_card(c,'ÎN TRANZIT','18',175,555,120,80,MINT,'pin'); info_card(c,'DOCUMENTE','24',308,555,120,80,BLUE,'doc')
    rows=[('București  →  Berlin','În tranzit','Azi 19:10',MINT),('Craiova  →  Cluj','La încărcare','Azi 16:45',GOLD),('Timișoara  →  Milano','Livrat','Finalizat',MINT)]
    for i,(route,stat,eta,col) in enumerate(rows):
        y=255-i*56; rr(c,42,y,W-84,43,10,Color(.06,.17,.30,.96)); icon(c,'truck',57,y+13,.47,WHITE); txt(c,route,88,y+25,10,WHITE,True); status(c,stat,236,y+12,col); txt(c,eta,W-58,y+20,8,MUTED,False,'right')
    pill(c,'CONCEPT DEMONSTRATIV',42,87,Color(.1,.25,.42),MUTED)

def p5(c):
    page(c,5); title(c,'Șoferul folosește telefonul','Mai puține telefoane. Mai puține întrebări.')
    phone(c,92,145,165,370)
    txt(c,'Cursa de azi',174,468,11,WHITE,True,'center'); txt(c,'București → Berlin',174,447,8,MUTED,False,'center')
    acts=[('Am ajuns',MINT),('Am încărcat',CYAN),('Am plecat',BLUE),('Am livrat',MINT)]
    for i,(lab,col) in enumerate(acts):
        y=395-i*54; rr(c,112,y,125,37,11,Color(col.red,col.green,col.blue,.16),col); icon(c,'check',127,y+10,.55,col); txt(c,lab,157,y+14,9,WHITE,True)
    rr(c,112,171,125,39,11,Color(.18,.5,.75,.2),CYAN); icon(c,'doc',128,178,.45,CYAN); txt(c,'Încarcă CMR',157,185,8,WHITE,True)
    for i,(num,head,body,ic) in enumerate([('01','Status instant','dispeceratul vede', 'pin'),('02','CMR în cursă','documentul urcă', 'doc'),('03','Mai puține apeluri','informația circulă', 'phone')]):
        y=430-i*108; rr(c,296,y,240,84,15,Color(.06,.17,.30,.96)); txt(c,num,314,y+53,11,CYAN,True); icon(c,ic,352,y+39,.57,MINT); txt(c,head,393,y+51,10,WHITE,True); txt(c,body,393,y+30,8,MUTED)

def p6(c):
    page(c,6); title(c,'Documentele ajung unde trebuie','Fără căutări inutile. Fără documente rătăcite.')
    steps=[('Șoferul fotografiază CMR','phone'),('Document identificat','doc'),('Atașat cursei','truck'),('Pregătit pentru facturare','check')]
    for i,(lab,ic) in enumerate(steps):
        y=525-i*98; rr(c,64,y,280,62,17,Color(.06,.17,.30,.97)); icon(c,ic,88,y+21,.7,CYAN if i<3 else MINT); txt(c,lab,138,y+28,11,WHITE,True)
        if i<3: line_arrow(c,204,y,204,y-32,CYAN,1.5)
    rr(c,375,250,160,282,19,Color(.94,.98,1,1)); txt(c,'CMR',455,495,12,NAVY,True,'center'); c.setStrokeColor(HexColor('#A9C6DF')); c.rect(397,297,116,168,fill=0,stroke=1); c.setStrokeColor(HexColor('#C8DDEC'))
    for i in range(6): c.line(412,438-i*21,498,438-i*21)
    c.setFillColor(MINT); c.circle(478,324,18,fill=1,stroke=0); icon(c,'check',469,316,.55,NAVY)
    benefits=[('CMR găsit rapid',MINT),('Mai puține documente pierdute',CYAN),('Mai puțină muncă administrativă',BLUE)]
    for i,(s,col) in enumerate(benefits):
        x=42+i*176; dot(c,x+5,138,col,5); wrap(c,s,x+18,142,145,9,12,WHITE,True)

def p7(c):
    page(c,7); title(c,'Vedem unde se fac banii','Vedem ce curse și ce parteneri sunt cei mai profitabili.')
    routes=[('București → Berlin','+ 520 €',MINT),('Craiova → Milano','+ 740 €',MINT),('București → Cluj','+ 180 €',GOLD)]
    for i,(r,v,col) in enumerate(routes):
        y=490-i*92; rr(c,42,y,300,72,17,Color(.06,.17,.30,.96)); txt(c,r,63,y+44,10,WHITE,True); txt(c,v,63,y+20,17,col,True); c.setFillColor(Color(col.red,col.green,col.blue,.15)); c.circle(308,y+35,20,fill=1,stroke=0); icon(c,'chart',296,y+25,.55,col)
    rr(c,366,308,170,254,19,Color(.06,.17,.30,.96)); txt(c,'Profit / cursă',451,529,10,MUTED,True,'center'); c.setStrokeColor(Color(.3,.65,1,.35)); c.line(394,363,510,363); c.line(394,363,394,492)
    bars=[(410,35,BLUE),(442,78,MINT),(474,55,CYAN)]
    for x,h,col in bars: c.setFillColor(col); c.roundRect(x,363,18,h,6,fill=1,stroke=0)
    txt(c,'Profit per:',42,220,13,WHITE,True)
    labs=[('camion','truck'),('rută','pin'),('cargus',None),('auto_total',None)]
    for i,(lab,ic) in enumerate(labs):
        x=42+i*125; rr(c,x,133,111,62,13,Color(.06,.17,.30,.96))
        if lab == 'cargus':
            partner_logo(c, 'cargus', x+55, 164, 92, 40)
        elif lab == 'auto_total':
            partner_logo(c, 'auto_total', x+55, 164, 91, 40)
        else:
            icon(c,ic,x+20,155,.5,CYAN); txt(c,lab,x+52,156,9,WHITE,True,'center')
    txt(c,'și alți clienți',W/2,107,8,MUTED,False,'center')
    pill(c,'DATE DEMONSTRATIVE',42,90,Color(.1,.25,.42),MUTED)

def p8(c):
    page(c,8); title(c,'Vedem unde se pierd bani','Mai puțini kilometri inutili. Mai mult control asupra costurilor.')
    kpis=[('Consum','8.2 l/100 km','chart',CYAN),('Km goi','14%','pin',GOLD),('Cost / km','0.91 €','truck',MINT),('Staționare','3.4 h','chart',BLUE),('Mentenanță','Planificată','gear',CYAN)]
    for i,(lab,val,ic,col) in enumerate(kpis):
        x=42+(i%2)*180; y=510-(i//2)*104
        if i==4: x=132; y=198
        info_card(c,lab,val,x,y,160,82,col,ic,small=True)
    rr(c,332,185,204,242,19,Color(.06,.17,.30,.97)); txt(c,'KM GOI',354,392,9,MUTED,True); txt(c,'18%',354,348,31,WHITE,True); line_arrow(c,420,356,466,356,MINT,2); txt(c,'14%',482,348,31,MINT,True)
    c.setStrokeColor(Color(.3,.7,1,.35)); c.setLineWidth(2); c.line(354,275,512,275)
    for i,h in enumerate([34,60,42,72,49]): c.setFillColor(CYAN if i<3 else MINT); c.roundRect(363+i*29,275,16,h,5,fill=1,stroke=0)
    pill(c,'EXEMPLU',354,225,Color(.1,.25,.42),MUTED)

def p9(c):
    page(c,9); title(c,'Sistemul face munca repetitivă','Mai puțină muncă manuală. Mai mult timp pentru decizii.')
    flow=[('Comandă','doc'),('Date extrase','gear'),('Cursă creată','truck'),('Transport','pin'),('CMR','doc'),('Factură','check')]
    for i,(lab,ic) in enumerate(flow):
        x=38+(i%3)*174; y=490-(i//3)*115; rr(c,x,y,142,76,16,Color(.06,.17,.30,.96)); icon(c,ic,x+23,y+30,.65,CYAN if i<4 else MINT); txt(c,lab,x+80,y+34,9,WHITE,True,'center')
        if i in (0,1,3,4): line_arrow(c,x+145,y+38,x+168,y+38,CYAN,1.4)
    line_arrow(c,290,490,290,451,CYAN,1.4)
    for i,(head,body,col) in enumerate([('CMR lipsă','alertă simplă',GOLD),('Cursa întârzie','status vizibil',RED),('Client notificat','când este cazul',MINT)]):
        x=42+i*176; rr(c,x,198,158,86,15,Color(.06,.17,.30,.96)); dot(c,x+18,252,col,5); txt(c,head,x+31,247,10,WHITE,True); txt(c,body,x+18,222,8,MUTED)
    pill(c,'AUTOMATIZĂRI SIMPLE',42,129,Color(.1,.25,.42),CYAN)

def p10(c):
    page(c,10); title(c,'Clientul vede singur unde este marfa','Mai puține telefoane către dispecerat.')
    browser(c,42,340,494,202,'SAMIR PORTAL CLIENT'); phone(c,336,145,140,240)
    txt(c,'Livrare în tranzit',406,343,9,WHITE,True,'center'); mock_map(c,353,240,106,73); status(c,'ETA 16:45',355,210,MINT)
    vals=[('Tracking','pin'),('ETA','chart'),('Status','truck'),('CMR','doc'),('Factură','doc')]
    for i,(lab,ic) in enumerate(vals):
        x=44+i*98; rr(c,x,112,84,65,13,Color(.06,.17,.30,.96)); icon(c,ic,x+31,139,.48,CYAN); txt(c,lab,x+42,121,8,WHITE,True,'center')
    txt(c,'Opțional: cerere de ofertă online',W/2,80,9,MUTED,False,'center')

def p11(c):
    page(c,11); title(c,'O imagine digitală mai puternică','Website-ul susține încrederea, cererile noi și imaginea profesională.')
    browser(c,42,252,494,290,'SAMIR ONE LOGISTIC')
    # website content overlay
    txt(c,'Transport',85,460,23,NAVY,True); txt(c,'simplificat.',85,432,23,BLUE,True)
    rr(c,85,380,118,28,9,BLUE); txt(c,'Solicită ofertă',144,390,8,WHITE,True,'center')
    c.setFillColor(NAVY2); c.roundRect(309,355,174,112,14,fill=1,stroke=0); icon(c,'truck',332,396,1.5,CYAN)
    labels=['Transport național','Transport internațional','Flotă','Portal client']
    for i,l in enumerate(labels): txt(c,l,84+(i%2)*195,315-(i//2)*25,9,NAVY,True)
    for i,(h,b,col) in enumerate([('Mai multă încredere','o prezență clară',MINT),('Mai multe cereri','un pas simplu',CYAN),('Imagine profesională','prima impresie contează',BLUE)]):
        x=42+i*176; rr(c,x,122,158,83,14,Color(.06,.17,.30,.96)); dot(c,x+18,178,col,5); txt(c,h,x+30,173,10,WHITE,True); txt(c,b,x+18,147,8,MUTED)

def p12(c):
    page(c,12); title(c,'Înainte → După','Un model tradițional comparat cu un model digital.')
    rr(c,42,180,232,365,20,Color(.1,.14,.21,.96)); rr(c,321,180,232,365,20,Color(.06,.26,.39,.96),Color(.25,.75,1,.35))
    txt(c,'MODEL TRADIȚIONAL',158,510,10,MUTED,True,'center'); txt(c,'MODEL DIGITAL',437,510,10,CYAN,True,'center')
    left=[('Comenzi separate','doc'),('Multe verificări','phone'),('Documente manuale','doc'),('Informație răspândită','pin')]
    right=[('Centru de control','chart'),('Urmărire transport','pin'),('Documente digitale','doc'),('Automatizări','gear'),('Profitabilitate','chart')]
    for i,(s,ic) in enumerate(left):
        y=447-i*62; icon(c,ic,68,y,.55,MUTED); txt(c,s,104,y+6,10,WHITE,True)
    for i,(s,ic) in enumerate(right):
        y=447-i*52; icon(c,ic,348,y,.55,MINT if i in (0,3) else CYAN); txt(c,s,384,y+6,10,WHITE,True)
    txt(c,'Mai puțină muncă.',W/2,122,18,WHITE,True,'center'); txt(c,'Mai mult control.',W/2,96,18,CYAN,True,'center')

def p13(c):
    page(c,13); title(c,'Un ecosistem conectat','Componente simple. O singură imagine a operațiunii.')
    cx,cy=W/2,365
    c.setFillColor(Color(.06,.32,.55,.95)); c.circle(cx,cy,75,fill=1,stroke=0); c.setStrokeColor(CYAN); c.setLineWidth(1.2); c.circle(cx,cy,75,fill=0,stroke=1)
    txt(c,'SAMIR ONE',cx,374,13,WHITE,True,'center'); txt(c,'LOGISTIC',cx,355,13,WHITE,True,'center')
    vals=[('01','Hub comenzi','doc',cx-175,cy+136),('02','Centru control','chart',cx+175,cy+136),('03','Aplicație șofer','phone',cx-190,cy+22),('04','Documente','doc',cx+190,cy+22),('05','Analiză flotă','truck',cx-175,cy-120),('06','Profitabilitate','chart',cx+175,cy-120),('07','Portal client','user',cx-78,cy-186),('08','Automatizare AI','gear',cx+78,cy-186)]
    for num,lab,ic,x,y in vals:
        line_arrow(c,cx+(x-cx)*.43,cy+(y-cy)*.43,x-(x-cx)*.17,y-(y-cy)*.17,Color(.25,.7,1,.45),.9)
        rr(c,x-62,y-23,124,46,13,Color(.06,.17,.30,.98)); txt(c,num,x-47,y+7,8,CYAN,True); icon(c,ic,x-22,y-8,.42,MINT); txt(c,lab,x+5,y-3,7.5,WHITE,True)

def p14(c):
    page(c,14); title(c,'Începem simplu','Nu trebuie construit totul din prima zi.')
    steps=[('01','Înțelegem procesele','vedem ce contează'),('02','Construim centrul de control','facem operațiunea vizibilă'),('03','Conectăm documentele și comenzile','aducem informația împreună'),('04','Adăugăm automatizări și AI','eliminăm pașii repetați')]
    for i,(n,h,b) in enumerate(steps):
        y=510-i*104; c.setFillColor(CYAN if i<2 else MINT); c.circle(76,y+23,24,fill=1,stroke=0); txt(c,n,76,y+18,11,NAVY,True,'center')
        rr(c,122,y-10,390,66,15,Color(.06,.17,.30,.96)); txt(c,h,148,y+28,11,WHITE,True); txt(c,b,148,y+9,8,MUTED)
        if i<3: line_arrow(c,76,y-2,76,y-42,CYAN,1.4)
    pill(c,'PAS CU PAS',42,84,Color(.1,.25,.42),CYAN)

def p15(c):
    c.setFillColor(NAVY); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(Color(.1,.5,1,.12)); c.circle(W/2,H/2,190,fill=1,stroke=0)
    c.setStrokeColor(Color(.3,.8,1,.28)); c.setLineWidth(1); c.circle(W/2,H/2,144,fill=0,stroke=1); c.circle(W/2,H/2,177,fill=0,stroke=1)
    txt(c,'Mai mult control',W/2,536,27,WHITE,True,'center'); txt(c,'asupra fiecărei curse.',W/2,501,27,CYAN,True,'center')
    wrap(c,'Software construit în jurul modului în care lucrează Samir One Logistic.',82,445,W-164,12,16,MUTED,False)
    vals=[('MAI PUȚIN','LUCRU MANUAL',MINT),('MAI MULT','CONTROL',CYAN),('DECIZII','MAI BUNE',BLUE)]
    for i,(a,b,col) in enumerate(vals):
        x=42+i*176; rr(c,x,265,158,86,15,Color(.06,.17,.30,.96)); c.setFillColor(col); c.rect(x+20,320,24,3,fill=1,stroke=0); txt(c,a,x+20,298,10,WHITE,True); txt(c,b,x+20,278,10,WHITE,True)
    rr(c,65,125,W-130,55,15,Color(.1,.34,.55,.96),CYAN,1)
    txt(c,'Următorul pas  →  Sesiune de descoperire digitală',W/2,147,12,WHITE,True,'center')
    txt(c,'SAMIR ONE LOGISTIC',W/2,60,8,MUTED,True,'center')

def build():
    os.makedirs(os.path.dirname(OUT),exist_ok=True)
    c=canvas.Canvas(OUT,pagesize=A4,pageCompression=1)
    for f in (cover,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15):
        f(c); c.showPage()
    c.save()

if __name__=='__main__': build()
