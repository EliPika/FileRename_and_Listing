#ふぁいるをリネームしてlistを作成する
import os
import sys
import pandas as pd
import codecs

def Path():
    Path="/Users/hoge"
    os.chdir(Path)
    return Path

def NowDir(p):
    Nowls=os.listdir(path=p)
    Fls = [f for f in Nowls if os.path.isdir(os.path.join(p, f))]
    #ファイルが無ければ実行しない
    #違ったらシステム終了
    if len(Fls)==0:
        print("File Not Found!!")
        print("Exit Program")
        sys.exit()
    return Fls

def REname(p):
    REfl = NowDir(p)
    i=0
    try:
        print("Renameing...")
        for name in REfl:
            tmp = name[:8]+name[10:-31]
            NameSplit = tmp.split()
            #print(tmp)        
            NewName=NameSplit[0]+" "+NameSplit[1]+NameSplit[2]
            #print(NewName)
            i+=1
            os.rename(name,NewName)
    except:
        print("Rename　Error!!")
    #print('count:',i)
    return 0

def form(p):
    l =list()
    i=0
    for folder, subfolders, files in os.walk(p):
        if i == 0:
            i=1
        else:
            #print('folder: {}'.format(folder))
            #print('subfolders: {}'.format(subfolders))
            tmp=files[0]
            tmp=tmp[-4:]
            l.append(tmp)
    #print(l)
    return l

def make(p):
    print("making...")
    #col=['学籍番号','名前',評価','備考']
    col=['学籍番号','形式','評価']
    Ndf = pd.DataFrame(columns=col)
    #print(df)
    fl = NowDir(p)
    kata = form(p)
    deap=0
    for  Fname in fl:        
        sp =Fname.split()
        number = sp[0]
        #正規化されていればsp[1]は存在する
        try:
            sp[1]
        except:
            print("Format Error!!")
            print("Exit Program")
            sys.exit()
        #形式
        k =kata[deap]
        deap+=1
        #評価
        if k != ".pdf":
            grad="B"
        else:
            grad = "*"
        series = pd.Series([number,k,grad], index=Ndf.columns)
        Ndf = Ndf.append(series,ignore_index = True)
    #Ndf['形式']=form(p)
    Ndf = Ndf.set_index('学籍番号')
    #print(Ndf)ß
    mtag ="../nowlist.csv"
    Ndf.to_csv(mtag,index=True, header=True,sep="\t", encoding="utf-16", mode='w')
    return 0

def load(ltag,utf):
    with codecs.open(ltag, "r",utf , "ignore") as file:
        #print("loading...")
        Ldf = pd.read_table(file,sep="\t")
        Ldf = Ldf.set_index('学籍番号')
        #print(Ldf)
        return Ldf

def check():
    print("checking...")
    tag1="../list.csv"
    tag2="../nowlist.csv"
    df1=pd.DataFrame(load(tag1,"utf-8"))
    df2=pd.DataFrame(load(tag2,"utf-16"))
    df = pd.concat([df1, df2], axis=1, join='outer',sort=True)
    #df.loc[df['評価'].isnull()]
    df=df.fillna({'評価':'C', '形式':'###'})
    #print(df)
    df['備考']=""
    df.to_csv("../★lise.csv",index=True, header=True,sep="\t", encoding="utf-16", mode='w')

p=Path()
REname(p)
make(p)
check()
print("compleat!!")
