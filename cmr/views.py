from django.shortcuts import render
from .forms import CardiacForm
import docx

# Create your views here.
def cmr(request):
    if request.method == "POST":
        form = CardiacForm(request.POST)
        if form.is_valid():
            cmr_results = form.cleaned_data
            first_name = cmr_results['first_name']
            last_name = cmr_results['last_name']
            gender = cmr_results['gender']
            mrn = cmr_results['mrn']
            age = cmr_results['age']
            height = cmr_results['height']
            weight = cmr_results['weight']
            lmm = cmr_results['lmm']
            ledv = cmr_results['ledv']
            lesv = cmr_results['lesv']
            redv = cmr_results['redv']
            resv = cmr_results['resv']

            bsa = round(((weight*height)/3600)**0.5, 2)

            # Indexed values

            lsv = ledv - lesv
            ledvi = int(round(ledv/bsa, 0))
            lesvi = int(round(lesv/bsa, 0))
            lsvi = int(round(lsv/bsa, 0))
            lmmi = int(round(lmm/bsa, 0))
            lvef = int(round(100*lsv/ledv, 0))

            rsv = redv - resv
            redvi = int(round(redv/bsa, 0))
            resvi = int(round(resv/bsa, 0))
            rsvi = int(round(rsv/bsa, 0))
            rvef = int(round(100*rsv/redv, 0))


            form = CardiacForm(initial={
                            
                'first_name':first_name,
                'last_name':last_name,
                'gender':gender,
                'mrn':mrn,
                'age':age,
                'height':height,
                'weight':weight,
                'lmm':lmm,
                'ledv':ledv,
                'lesv':lesv,
                'redv':redv,
                'resv':resv,
            })
    
            return render(request, "cmr/cmr.html", context={
                                                    'form':form, 
                                                    'submitted':True,
                                                    'first_name':first_name,
                                                    'last_name':last_name,
                                                    'gender':gender,
                                                    'mrn':mrn,
                                                    'age':age,
                                                    'height':height,
                                                    'weight':weight,
                                                    'lmm':lmm,
                                                    'ledv':ledv,
                                                    'lesv':lesv,
                                                    'redv':redv,
                                                    'resv':resv,
                                                    'bsa':bsa,
                                                    'lsv': lsv,
                                                    'ledvi': ledvi,
                                                    'lesvi': lesvi,
                                                    'lsvi': lsvi,
                                                    'lmmi': lmmi,
                                                    'lvef': lvef,

                                                    'rsv': rsv,
                                                    'redvi': redvi,
                                                    'resvi': resvi,
                                                    'rsvi' : rsvi,
                                                    'rvef' : rvef,

                                                    })

        else:
            form = CardiacForm()
            return render(request, "cmr/cmr.html", context={'form':form})

    else:
        form = CardiacForm()

    return render(request, "cmr/cmr.html", context={'form':form})