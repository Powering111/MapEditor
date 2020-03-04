import tkinter
import tkinter.font
import os
from tkinter.simpledialog import askstring
from tkinter.simpledialog import askinteger
import tkinter.messagebox
import tkinter.colorchooser
import tkinter.ttk
import tkinter.filedialog
import queue
import webbrowser
import shutil
import game
# initialize
window = tkinter.Tk()
window.title("[Aroid] Map Editor")
window.geometry("1024x768+0+0")
window.resizable(False,False)
window.iconbitmap('./icon.ico')
saved=True

def close(event=None):
    print("hihi")
    if saved==False:
        print("...")
        choice = tkinter.messagebox.askquestion("종료 전 저장","저장하고 종료하시겠습니까?",icon='warning')
        if(choice=="yes"):
            print("saving before close")
            save()
            window.destroy()
        elif choice=="no":
            window.destroy()
        else:
            return
    window.destroy()
lvlname=askstring('맵 이름','맵 이름 입력(없으면 새로 만들어짐)')
if lvlname is None:
    window.destroy()
level=[]
nowTick=1
lvltime=1
nowev=0
arrowColors=["white","red","green","purple","yellow","blue","orange","pink","black","gray"]
# functions
def loadlevel():
    print("====LOAD====")
    global level,lvltime,lvlname2,lvlauthor,lvldifficulty,lvlname
    if not os.path.exists('levels/'+lvlname): #make path
        os.makedirs('levels/'+lvlname)
    if not os.path.isfile('./levels/'+lvlname+'/level'): # new file
        file=open('./levels/'+lvlname+'/level','w')
        file.write(askstring("맵 이름 2","플레이 시에 보여지는 맵 이름 입력")+'\n')
        file.write(askstring("만든이","만든 이의 이름")+'\n')
        file.write(askstring("난이도","난이도를 정수로 입력(1~7)")+'\n')
        file.write('1\n')
        file.write('0')
        file.close()

    file=open('./levels/'+lvlname+'/level','r') # load
    lvlname2=file.readline().strip()
    lvlauthor=file.readline().strip()
    lvldifficulty=int(file.readline().strip())
    lvltime=int(file.readline().strip())
    data=file.readlines() # data is all lines of data
    q=queue.Queue()
    for x in data:
        x=x.strip().split()
        for y in range(len(x)):
            q.put(int(x[y]))
    for x in range(lvltime):# in 1 tick
        dat=[]
        a=q.get()
        dat.append(a)
        for y in range(a):
            b=q.get()
            dat.append(b)
            if b==1 or b==2:
                for j in range(3):
                    dat.append(q.get())
            elif b==3:
                for j in range(2):
                    dat.append(q.get())
        level.append(dat)
        print(dat)
    file.close()
    print("loaded")
def save(event=None):
    global saved
    print("====SAVE====")
    file=open('./levels/'+lvlname+'/level','w') # save
    print("saving level : "+lvlname+" ("+lvlname2+") BY" + lvlauthor+" , Difficulty is "+str(lvldifficulty) + " , time - "+str(lvltime))
    file.write(str(lvlname2)+'\n')
    file.write(str(lvlauthor)+'\n')
    file.write(str(lvldifficulty-1)+'\n')
    file.write(str(lvltime)+'\n')
    for x in range(lvltime):
        dat=""
        for y in level[x]:
            dat+=str(y)
            dat+=" "
        file.write(dat)
        if x%10==9:
            file.write("\n")
    saved=True
    print("saved")
eventTypes=["플레이어 모드 ","데미지 ","실드 값 설정 : ","DEF ","DEF 값 설정 : ","IDEF ","IDEF 값 설정 : ","HP ","HP 값 설정 : ","SPEED ","SPEED 값 설정 : ","MHP ","MHP 값 설정 : "]
nowEvents=[]
def refreshTick():
    global nowTick,lvltime,level,nowEvents
    # TODO: set things to this tick
    nowTicktxt.config(text="현재 틱 : "+str(nowTick)+" / "+str(lvltime))
    # 레벨 해석 부분
    # eventslistbox 설정
    eventslistbox.delete(0,"end")
    a=0
    nowEvents=[]
    for x in range(level[nowTick-1][0]):
        a+=1
        dat=level[nowTick-1][a]
        if dat==1:
            a+=1
            R=level[nowTick-1][a]
            a+=1
            G=level[nowTick-1][a]
            a+=1
            B=level[nowTick-1][a]
            eventslistbox.insert(x,"BG [ {} , {} , {} ]".format(R,G,B))
            nowEvents.append([1,R,G,B])
        elif dat==2:
            a+=1
            ty=level[nowTick-1][a]
            a+=1
            pos=level[nowTick-1][a]
            a+=1
            spd=level[nowTick-1][a]
            eventslistbox.insert(x,"{} arrow({}) at {}".format(arrowColors[ty],spd,pos))
            if ty!=6:
                eventslistbox.itemconfig(x,bg="orange",fg=arrowColors[ty])
            else:
                eventslistbox.itemconfig(x,bg="orange",fg="red")
            nowEvents.append([2,ty,pos,spd])
        elif dat==3:
            a+=1
            et=level[nowTick-1][a]
            a+=1
            val=level[nowTick-1][a]
            eventslistbox.insert(x,"이벤트 - {}{}".format(eventTypes[et-1],val))
            eventslistbox.itemconfig(x,bg="aqua")
            nowEvents.append([3,et,val])
def arUpdate(event=None):
    AR_P=AR_Poss.get()
    AR_Pos.delete("all")
    AR_Pos.create_polygon(10,10,10,210,210,210,210,10,fill="white")
    a=10
    b=10
    pos=AR_P
    if pos>=0 and pos<100:
        a=10+2*pos
        b=10
    elif pos>=100 and pos<200:
        a=210
        b=10+2*(pos-100)
    elif pos>=200 and pos<300:
        a=210-2*(pos-200)
        b=210
    elif pos>=300 and pos<400:
        a=10
        b=210-2*(pos-300)
    AR_Pos.create_oval(a-2,b-2,a+2,b+2,fill="red")
def refreshnow(event=None):
    global AR_P
    try:
        selected=nowev
        ne=nowEvents[selected][0]
        print(ne)
        if ne==1:
            BGbtn.config(bg="green")
            ARbtn.config(bg="aqua")
            EVbtn.config(bg="aqua")
            desctxt.config(text="색 선택 또는 RGB 입력 후 OK 누르기")
            BG_R.delete(0,100)
            BG_G.delete(0,100)
            BG_B.delete(0,100)
            BG_R.insert(0,nowEvents[selected][1])
            BG_G.insert(0,nowEvents[selected][2])
            BG_B.insert(0,nowEvents[selected][3])
            BG_R.place(x=50,y=150)
            BG_G.place(x=50,y=180)
            BG_B.place(x=50,y=210)
            BG_OK.place(x=230,y=150)
            BG_Pick.place(x=20,y=150)
            AR_Type.place_forget()
            AR_Pos.place_forget()
            AR_Speed.place_forget()
            AR_OK.place_forget()
            AR_Poss.place_forget()
            EV_Type.place_forget()
            EV_Value.place_forget()
            EV_OK.place_forget()
            print("1234")
        elif ne==2:
            BGbtn.config(bg="aqua")
            ARbtn.config(bg="green")
            EVbtn.config(bg="aqua")
            desctxt.config(text="화살 종류, 화살 위치 ,속도 정한 후 OK 누르기")
            BG_R.place_forget()
            BG_G.place_forget()
            BG_B.place_forget()
            BG_OK.place_forget()
            BG_Pick.place_forget()
            AR_Type.current(nowEvents[selected][1])
            AR_P=nowEvents[selected][2]
            AR_Speed.set(nowEvents[selected][3])
            AR_Type.place(x=20,y=170)
            AR_Poss.set(AR_P)
            arUpdate()
            AR_Pos.place(x=10,y=200)
            AR_Poss.place(x=5,y=420)
            AR_Speed.place(x=250,y=180)
            AR_OK.place(x=300,y=300)
            EV_Type.place_forget()
            EV_Value.place_forget()
            EV_OK.place_forget()
        elif ne==3:
            BGbtn.config(bg="aqua")
            ARbtn.config(bg="aqua")
            EVbtn.config(bg="green")
            BG_R.place_forget()
            BG_G.place_forget()
            BG_B.place_forget()
            BG_OK.place_forget()
            BG_Pick.place_forget()
            AR_Type.place_forget()
            AR_Pos.place_forget()
            AR_Speed.place_forget()
            AR_OK.place_forget()
            AR_Poss.place_forget()
            EV_Type.set(eventTypes[nowEvents[selected][1]-1])
            EV_Value.delete(0,100)
            EV_Value.insert(0,str(nowEvents[selected][2]))
            EV_Type.place(x=10,y=250)
            EV_Value.place(x=10,y=300)
            EV_OK.place(x=300,y=300)
    except IndexError:
        BG_R.place_forget()
        BG_G.place_forget()
        BG_B.place_forget()
        BG_OK.place_forget()
        BG_Pick.place_forget()
        AR_Type.place_forget()
        AR_Pos.place_forget()
        AR_Speed.place_forget()
        AR_OK.place_forget()
        AR_Poss.place_forget()
        EV_Type.place_forget()
        EV_Value.place_forget()
        EV_OK.place_forget()
def btnColReset():
    BGbtn.config(bg="aqua")
    ARbtn.config(bg="aqua")
    EVbtn.config(bg="aqua")
    desctxt.config(text="")
def apply():
    global level
    e=[len(nowEvents)]
    print(nowEvents)
    for x in nowEvents:
        for y in x:
            e.append(y)
    level[nowTick-1]=e
    refreshTick()
    refreshnow()
    print("applied Events")
def setTick(a):
    global nowTick,lvltime,saved,level
    if a<1:
        a=1
    nowTick=a
    if nowTick>lvltime:
        lvltime=nowTick
        level.append([0])
        saved=False
    print(str(nowTick)+" / "+str(lvltime))
    refreshTick()
    btnColReset()
def questionTick(event=None):
    a=askinteger("Type Tick","이동할 틱 입력",minvalue=1,maxvalue=lvltime)
    if a is not None and a!=nowTick:
        setTick(a)
def nextTick(event=None):
    setTick(nowTick+1)
    refreshnow()
def prevTick(event=None):
    setTick(nowTick-1)
    refreshnow()
def delTick(event=None):
    global level,lvltime,nowTick
    if lvltime==1:
        return
    del level[lvltime-1]
    if nowTick==lvltime:
        nowTick-=1
    lvltime-=1
    saved=False
    refreshTick()
    btnColReset()
def delnowTick(event=None):
    global level,lvltime,nowTick
    if lvltime==1:
        return
    del level[nowTick-1]
    lvltime-=1
    saved=False
    refreshTick()
    btnColReset()
def insertTick(event=None):
    global level,nowTick,lvltime
    level.insert(nowTick,[0])
    nowTick+=1
    lvltime+=1
    saved=False
    refreshTick()
    btnColReset()
def newBG(event=None):
    global level
    level[nowTick-1][0]+=1
    level[nowTick-1].append(1)
    level[nowTick-1].append(255)
    level[nowTick-1].append(255)
    level[nowTick-1].append(255)
    saved=False
    refreshTick()
def newAR(event=None):
    global level
    level[nowTick-1][0]+=1
    level[nowTick-1].append(2)
    level[nowTick-1].append(0)
    level[nowTick-1].append(0)
    level[nowTick-1].append(10)
    saved=False
    refreshTick()
def newEV(event=None):
    global level
    level[nowTick-1][0]+=1
    level[nowTick-1].append(3)
    level[nowTick-1].append(1)
    level[nowTick-1].append(0)
    saved=False
    refreshTick()
def bgok():
    global nowEvents
    k=nowev
    try:
        r=int(BG_R.get())
        g=int(BG_G.get())
        b=int(BG_B.get())
        if r<0 or g<0 or b<0 or r>255 or g>255 or b>255:
            BG_R.delete(0,100)
            BG_G.delete(0,100)
            BG_B.delete(0,100)
        else:
            nowEvents[k]=[1,r,g,b]
            BG_R.delete(0,100)
            BG_G.delete(0,100)
            BG_B.delete(0,100)
            apply()
            btnColReset()
    except TypeError:
        BG_R.delete(0,100)
        BG_G.delete(0,100)
        BG_B.delete(0,100)
    except ValueError:
        BG_R.delete(0,100)
        BG_G.delete(0,100)
        BG_B.delete(0,100)
def bgsel():
    try:
        color=tkinter.colorchooser.askcolor()
        c=color[0]
        print(c)
        BG_R.delete(0,100)
        BG_G.delete(0,100)
        BG_B.delete(0,100)
        BG_R.insert(0,str(int(c[0])))
        BG_G.insert(0,str(int(c[1])))
        BG_B.insert(0,str(int(c[2])))
        bgok()
    except IndexError:
        print("color sel error")
        return
def arok(event=None):
    global nowEvents
    k=nowev
    ty=arrowColors.index(AR_Type.get())
    pos=AR_Poss.get()
    spd=AR_Speed.get()
    nowEvents[k]=[2,ty,pos,spd]
    apply()
def evcheck(event=None):
    global nowev
    try:
        nowev=eventslistbox.curselection()[0]
        refreshnow()
    except IndexError:
        pass
    
def evok(event=None):
    global nowEvents
    k=nowev
    ty=eventTypes.index(EV_Type.get())+1
    val=EV_Value.get()
    nowEvents[k]=[3,ty,val]
    apply()
def delnow(event=None):
    global nowEvents,nowev
    try:
        del nowEvents[nowev]
        nowev=100
        apply()
    except IndexError:
        return
def ahelp(event=None):
    try:
        webbrowser.open("info\\info.html",new=0,autoraise=True)
    except webbrowser.Error:
        tkinter.messagebox.showerror('오류 발생','웹 페이지를 여는 데에 오류가 발생했습니다.')
def settingOK(name,author,difficulty,music):
    global lvlname,lvlauthor,lvldifficulty
    if name!="":
        lvlname2=name
    if author!="":
        lvlauthor=author
    if difficulty!="":
        try:
            lvldifficulty=int(difficulty)
        except ValueError:
            try:
                ld=['TUTORIAL','EASY','MEDIUM','HARD','INSANE','EXTREME','CHAOS']
                lvldifficulty=ld.index(difficulty)
            except ValueError:
                pass
    save()
    if music!="":
        shutil.copy(music,'./levels/{}/music.wav'.format(lvlname))
    lvlnametxt.config(text=str("맵 이름 : "+lvlname+" ("+lvlname2+")"))
    lvlauthortxt.config(text=str("만든 이 : "+lvlauthor+" , 난이도 : "+str(lvldifficulty)))
    s.destroy()
def settingmusic(event=None):
    global smusicpath
    
    smusicpath = tkinter.filedialog.askopenfilename(title = "음악 파일 선택",filetypes = (("wav files","*.wav"),("All files","*.*")))
    s.lift()
def mapsetting(event=None):
    global smusicpath,s
    s=tkinter.Tk()
    s.geometry("600x600+0+0")
    s.title("맵 설정 : "+lvlname)
    snametxt=tkinter.Label(s,text="인게임에서 보여지는 맵 이름",font=font2)
    sauthortxt=tkinter.Label(s,text="만든 이",font=font2)
    sdifficultytxt=tkinter.Label(s,text="난이도",font=font2)
    snametextbox=tkinter.Entry(s,font=font2)
    sauthortextbox=tkinter.Entry(s,font=font2)
    sdifficultytextbox=tkinter.Entry(s,font=font2)
    snametextbox.insert(0,lvlname2)
    sauthortextbox.insert(0,lvlauthor)
    sdifficultytextbox.insert(0,str(lvldifficulty))
    smusicpath=""
    smusicpathbtn=tkinter.Button(s,text="음악 불러오기",width=10,height=5,command=settingmusic)
    sokbtn=tkinter.Button(s,text="확인",width=10,height=3,command=lambda _=None : settingOK(snametextbox.get(),sauthortextbox.get(),sdifficultytextbox.get(),smusicpath))
    snametxt.place(x=10,y=50)
    sauthortxt.place(x=10,y=100)
    sdifficultytxt.place(x=10,y=150)
    snametextbox.place(x=300,y=50)
    sauthortextbox.place(x=300,y=100)
    sdifficultytextbox.place(x=300,y=150)
    sokbtn.place(x=300,y=300)
    smusicpathbtn.place(x=50,y=200)
    s.mainloop()
def runmap(e=None):
    save()
    game.run(lvlname,False)
def runmapI(e=None):
    save()
    game.run(lvlname,True)
loadlevel()

# menu bar
menubar=tkinter.Menu(window)
# file menu
filemenu=tkinter.Menu(menubar,tearoff=0)
filemenu.add_command(label="저장",command=save,accelerator="Ctrl+S")

filemenu.add_separator()
filemenu.add_command(label="종료",command=close,accelerator="Ctrl+Q")
# edit menu
editmenu=tkinter.Menu(menubar,tearoff=0)
editmenu.add_command(label="다음 틱",command=nextTick,accelerator="->")
editmenu.add_command(label="이전 틱",command=prevTick,accelerator="<-")
editmenu.add_command(label="틱 이동",command=questionTick,accelerator="Alt+G")
editmenu.add_separator()
editmenu.add_command(label="현재 위치에 틱 추가",command=insertTick,accelerator="Ctrl+F")
editmenu.add_command(label="마지막 틱 삭제",command=delTick,accelerator="Ctrl+W")
editmenu.add_command(label="현재 틱 삭제",command=delnowTick,accelerator="Ctrl+E")
editmenu.add_separator()
newEventmenu=tkinter.Menu(editmenu,tearoff=0)
newEventmenu.add_command(label="배경색 변경",command=newBG,accelerator="Ctrl+1")
newEventmenu.add_command(label="화살 발사",command=newAR,accelerator="Ctrl+2")
newEventmenu.add_command(label="이벤트 실행",command=newEV,accelerator="Ctrl+3")
editmenu.add_cascade(label="새 이벤트",menu=newEventmenu)
editmenu.add_command(label="선택된 이벤트 삭제",command=delnow,accelerator="Shift+D")
toolmenu=tkinter.Menu(menubar,tearoff=0)
toolmenu.add_command(label="맵 설정",command=mapsetting)
toolmenu.add_command(label="도움말",command=ahelp)
# menu apply
menubar.add_cascade(label="파일",menu=filemenu)
menubar.add_cascade(label="편집",menu=editmenu)
menubar.add_cascade(label="도구",menu=toolmenu)
window.bind("<Control-s>",save)
window.bind("<Control-q>",close)
window.bind("<Control-w>",delTick)
window.bind("<Control-e>",delnowTick)
window.bind("<Control-f>",insertTick)
window.bind("<Control-Key-1>",newBG)
window.bind("<Control-Key-2>",newAR)
window.bind("<Control-Key-3>",newEV)
window.bind("<Alt-g>",questionTick)
window.bind("<Right>",nextTick)
window.bind("<Left>",prevTick)
window.bind("<Control-d>",delnow)
window.bind("<Delete>",delnow)
window.bind("<F5>",runmap)
window.bind("<F3>",runmapI)
window.bind("<F1>",ahelp)
# make objects
#    font
font1 = tkinter.font.Font(family="맑은 고딕",size=20)
font2 = tkinter.font.Font(family="맑은 고딕",size=12)
font3 = tkinter.font.Font(family="맑은 고딕",size=16)

window.title("[Aroid] Map Editor - "+lvlname+" BY "+lvlauthor)
titletxt=tkinter.Label(window,text="Aroid 맵 에디터",font=font1)
lvlnametxt=tkinter.Label(window,text=str("맵 이름 : "+lvlname+" ("+lvlname2+")"),font=font1)
lvlauthortxt=tkinter.Label(window,text=str("만든 이 : "+lvlauthor+" , 난이도 : "+str(lvldifficulty)),font=font3)
eventslistbox=tkinter.Listbox(window,selectmode="single",font=font2,width=30,height=20,selectbackground="yellow",selectforeground="purple",activestyle="none")
nowTicktxt=tkinter.Label(window,text="현재 틱 : 1 / 1",font=font3)
eventslistbox.bind('<<ListboxSelect>>',evcheck)
nextTickbtn=tkinter.Button(window,command=nextTick,text=">",width=4,height=2,bg="yellow")
prevTickbtn=tkinter.Button(window,command=prevTick,text="<",width=4,height=2,bg="yellow")
editFrame=tkinter.Frame(window,width=400,height=450,relief="solid",bd=2)
BGbtn=tkinter.Button(editFrame,command=newBG,text="배경색 변경",width=10,height=5,bg="aqua")
ARbtn=tkinter.Button(editFrame,command=newAR,text="화살 발사",width=10,height=5,bg="aqua")
EVbtn=tkinter.Button(editFrame,command=newEV,text="이벤트 실행",width=10,height=5,bg="aqua")
desctxt=tkinter.Label(editFrame,text="",font=font2)
BG_R=tkinter.Entry(editFrame)
BG_G=tkinter.Entry(editFrame)
BG_B=tkinter.Entry(editFrame)
BG_Pick=tkinter.Button(editFrame,text="/",command=bgsel,width=2,height=1)
BG_OK=tkinter.Button(editFrame,text="OK",command=bgok,width=10,height=5)
AR_Type=tkinter.ttk.Combobox(editFrame,values=arrowColors)
AR_Pos=tkinter.Canvas(editFrame,width=240,height=240)
AR_Poss=tkinter.Scale(editFrame,orient="horizontal",from_=0,to=399,width=10,length=390,showvalue=False,command=arUpdate)
AR_Speed=tkinter.Scale(editFrame,orient="horizontal",from_=5,to=20,width=15,label="속도")
AR_OK=tkinter.Button(editFrame,text="OK",command=arok,width=10,height=5)
EV_Type=tkinter.ttk.Combobox(editFrame,values=eventTypes)
EV_Value=tkinter.Entry(editFrame)
EV_OK=tkinter.Button(editFrame,text="OK",command=evok,width=10,height=5)
delBtn=tkinter.Button(window,text="X",command=delnow,width=4,height=2)
# place objects
window.config(menu=menubar)
titletxt.place(x=10,y=10)
lvlnametxt.place(x=250,y=10)
lvlauthortxt.place(x=250,y=50)
eventslistbox.place(x=50,y=200)
nowTicktxt.place(x=50,y=160)
nextTickbtn.place(x=270,y=150)
prevTickbtn.place(x=220,y=150)
editFrame.place(x=400,y=200)
BGbtn.place(x=20,y=20)
ARbtn.place(x=120,y=20)
EVbtn.place(x=220,y=20)
desctxt.place(x=10,y=120)
delBtn.place(x=50,y=650)
refreshTick()
window.protocol("WM_DELETE_WINDOW", close)

# mainloop
window.mainloop()
