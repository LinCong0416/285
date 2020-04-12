from django.shortcuts import render

# Create your views here.
def index(request):
     return render(request,'index.html')

def calPage(request):
    value_A = request.POST['symbol']
    value_B = request.POST['allotment']
    value_C = request.POST['sPrice']
    value_D = request.POST['cPrice1']
    value_E = request.POST['iPrice']
    value_F = request.POST['cPrice2']
    value_G = request.POST['rate']

    resA = float(value_B) * float(value_C)
    resBB = float(value_B) * float(value_C) - float(value_B)*float(value_E) - float(value_D) - float(value_F)
    resB = float(value_B) * float(value_E) + float(value_F) + float(value_D) + resBB * float(value_G) / 100
    resC = resBB * (1 - float(value_G) / 100)
    resD = resC / resB
    resE = (float(value_E) * float(value_B) + float(value_D) + float(value_F)) / float(value_B)

    return render(request,'index.html',context={'data1':resA,'data2':resB,'data3':resC,
                                                'data4':resD,'data5':resE})
