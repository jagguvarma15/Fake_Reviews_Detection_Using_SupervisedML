from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import HttpResponse
from django.contrib import messages
import pandas as pd
import nltk
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


global df
global X_train,X_test,y_train,y_test


def index(request):
    return render(request,'index.html')

def register(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        psw=request.POST['psw']
        cpsw=request.POST['cpsw']
        print(name)
        print(email)
        print(psw)
        print(cpsw)
        if psw==cpsw:
            if User.objects.filter(email=email,username=name).exists():
                print('User Already Registered')
                messages.info(request,"User Already Exists")
                return render(request,'signup.html')

            else:
                user=User.objects.create_user(username=name,password=psw,email=email)
                user.save();
                print('User Created')
                messages.info(request,"Registration Successful")
                return render(request,'login.html')
        else:
            messages.info(request,"Password Miss Match")
            return render(request,'signup.html')

    return render(request,'signup.html')

def login(request):
    if request.method=="POST":
        name=request.POST['username']
        psw=request.POST['psw']
        # print(email)
        print(psw)
        user=auth.authenticate(username=name,password=psw)
        print(user)
        if user is not None:
            auth.login(request,user)
            messages.info(request,"Login Succesful")
            return render(request,'loghome.html')
        else:
            messages.info(request,"Invalid Credentials")
            return render(request,'login.html')


    return render(request,'login.html')

def loghome(request):
    return render(request,"loghome.html")

def upload(request):
    if request.method=="POST":
        file=request.FILES['file']
        global df
        df=pd.read_csv(file)
        messages.info(request,"Data Uploaded Successfully")

    return render(request,"upload.html")
def viewdata(request):
    col=df.to_html
    dummy=df.head(100)
    # print(col)
    # return HttpResponse(col)
    col=dummy.columns
    rows=dummy.values.tolist()
    return render(request, 'viewdata.html',{'col':col,'rows':rows})

def models(request):
    ps = PorterStemmer()
    corpus = []
    print('abcdefghh')
    df1 = df[:10000]
    df1.rename(columns={'text_': 'text'}, inplace=True)
    print(df1.head())
    for i in range(len(df1['text'])):
        words = re.sub(',', '', df1['text'][i])
        words = words.lower()
        words = nltk.sent_tokenize(df1['text'][i])
        word = [ps.stem(word) for word in words if not word in stopwords.words('english')]
        words = ''.join(words)
        corpus.append(words)
    global cv
    cv = TfidfVectorizer()
    X = cv.fit_transform(corpus).toarray()
    y = df1['label']
    print(y.head())
    y.replace({'OR': 0, 'CG': 1}, inplace=True)
    global X_train, X_test, y_train, y_test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=52)
    if request.method=="POST":


        model = request.POST['algo']
        if model=="0":
            knn = KNeighborsClassifier(n_neighbors=7)
            knn.fit(X_train,y_train)
            pred = knn.predict(X_test)
            acs=accuracy_score(y_test, pred)
            ac="Accuracy Obtained for KNN is "+str(acs)
            messages.info(request,ac)
        elif model=="1":
            print('bbbbbbbbbbbbbbbbbbbb')
            gb = GaussianNB()
            gb.fit(X_train, y_train)
            gpred = gb.predict(X_test)
            acs2=accuracy_score(y_test, gpred)
            acs2 = "Accuracy Obtained for Naive Bayes is " + str(acs2)
            messages.info(request, acs2)
        else:
            print('ccccccccccccccccccc')
            # from sklearn.preprocessing import StandardScaler
            # scalar = StandardScaler()
            # # fitting
            # scalar.fit(X)
            # scaled_data = scalar.transform(X)
            # # Importing PCA
            # from sklearn.decomposition import PCA
            # # Let's say, components = 2
            # pca = PCA(n_components=500)
            # pca.fit(scaled_data)
            # x_pca = pca.transform(scaled_data)
            # x_pca.shape
            # X_train, X_test, y_train, y_test = train_test_split(x_pca, y, test_size=0.4, random_state=52)
            lr=LogisticRegression()
            lr.fit(X_train,y_train)
            spred=lr.predict(X_test)
            acs3=accuracy_score(y_test,spred)
            acs3 = "Accuracy Obtained for Logistic Regession is " + str(acs3)
            messages.info(request, acs3)
        return render(request,'model.html')
    return render(request,'model.html')

def prediction(request):
    if request.method=="POST":
        print('pred')
        lr = LogisticRegression()
        lr.fit(X_train, y_train)
        print('done')
        a=request.POST['name']
        print(a)
        new = cv.transform([a]).toarray()
        output=lr.predict(new)
        print(output)
        if output==[0]:
            val="The Review is Original"
        else:
            val="The Review is Computer Generated"
        messages.info(request,val)
        return render(request,'prediction.html')
    return render(request, 'prediction.html')

def about(request):
    return render(request,'about.html')


