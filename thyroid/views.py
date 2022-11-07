from django.shortcuts import render
from .forms import NoduleForm
from django.http.response import HttpResponseRedirect


# Create your views here.


nodules = []

# Create your views here.

def tr_recommendation(dimensions, scores):

    trsum = sum(scores)
    if trsum < 2:
        TR = 'TR1'
    elif trsum == 2:
        TR = 'TR2'
    elif trsum == 3:
        TR = 'TR3'
    elif 4 <= trsum <= 6:
        TR = 'TR4'
    elif trsum > 6:
        TR = 'TR5'

    size = max(dimensions)

    if TR == 'TR1' or TR == 'TR2':
        recommendation = 'No FNA or imaging follow up recommended.'
    elif TR == 'TR3':
        if size < 1.5:
            recommendation = 'No specific recommendations.'
        if size > 1.4:
            recommendation = 'Follow up in 2-5 years is recommended.'
        if size > 2.4:
            recommendation = 'FNA biopsy is recommended.'
    elif TR == 'TR4':
        if size > 0.9:
            recommendation = 'Follow up in 1-3 years is recommended'
        if size > 1.4:
            recommendation = 'FNA biopsy is recommended.'
    elif TR == 'TR5':
        if size > 0.9:
            recommendation = 'FNA biopsy is recommended.'
        else:
            recommendation = 'Follow up in 1 year.'

    if size < 1:
        recommendation = 'No specific recommendations due to small size.'

    return TR, recommendation


def home(request):
    nodules.clear()
    return HttpResponseRedirect('../')


def tirads(request):
    
    if request.method == "POST":
        form = NoduleForm(request.POST)

        if "add_nodule" in request.POST:         
            if form.is_valid():
                
                thyroid_results = form.cleaned_data

                parenchyma = thyroid_results['parenchyma']
                isthmus = thyroid_results['isthmus']
                rt_vol = thyroid_results['rt_vol']
                lt_vol = thyroid_results['lt_vol']

                composition = thyroid_results['composition']
                echogenicity = thyroid_results['echogenicity']
                shape = thyroid_results['shape']
                margins = thyroid_results['margins']
                foci = thyroid_results['foci']

                lobe = thyroid_results['lobe']
                aspect = thyroid_results['aspect']
                position = thyroid_results['position']

                length = thyroid_results['length']
                width = thyroid_results['width']
                height = thyroid_results['height']


                if lobe != 'isthmus':
                    location = f"<br>A nodule in the {lobe} lobe, {aspect} aspect {position}, measuring {length} x {width} x {height} cm, and has the following features:"
                else:
                    location = f"<br>A nodule is seen in the isthmus, measuring {length} x {width} x {height} cm, and has the following features:"


                dimensions = [length, width, height]
                scores = [int(composition[-2]), int(echogenicity[-2]), int(shape[-2]), int(margins[-2]), int(foci[-2])]
                
                tr, recommendation = tr_recommendation(dimensions, scores)

                if composition in ['Spongiform, no points for other features (0)', 'Possibly, but not definitely spongiform (0)']:
                    nodule_chr = f"<br>Nodule #{len(nodules)+1}:{location}<br>-Composition: {composition}.<br>"
                else:
                    nodule_chr = f"<br>Nodule #{len(nodules)+1}:{location}<br>-Composition: {composition}.<br>-Echogenicity: {echogenicity}.<br>-Shape: {shape}.<br>-Margins: {margins}.<br>-Echogenic foci: {foci}.<br>{tr}: {recommendation}<br>"
                                
                gland = f"The right thyroid lobe volume: {rt_vol} cc.<br>The left thyroid lobe volume: {lt_vol} cc.<br>Thyroid parenchyma is {parenchyma}.<br>The isthmus measures {isthmus} cm in AP diameter."
     
                nodules.append(nodule_chr)
                
                form = NoduleForm(initial={
                                            'parenchyma': parenchyma,
                                            'isthmus': isthmus,
                                            'rt_vol': rt_vol,
                                            'lt_vol': lt_vol, 
                                            'composition': 'Completely or almost completely cystic (0)',
                                            'echogenicity': 'Hyperechoic (1)',
                                            'shape': 'Wider than tall (0)',
                                            'margins': 'Smooth (0)',
                                            'foci': 'No echogenic foci (0)',
                                            'lobe': 'right',
                                            'aspect': 'upper',
                                            'position': 'anteriorly',
                                            'length': 0,
                                            'width': 0,
                                            'height': 0,
                                            })
                return render(request, "thyroid/thyroid.html", context={
                                                                    'form':form, 
                                                                    'gland':gland,
                                                                    'nodules': nodules,
                                                                    'submitted': True,
                                                                    

                                                                    })
            else:
                
                form = NoduleForm()
                return render(request, "thyroid/thyroid.html", context={'form':form})
        elif "modify_nodule" in request.POST:
            if form.is_valid():
                thyroid_results = form.cleaned_data
                invalid_selection = False
                if isinstance(form.cleaned_data['nodule_num'], int):
                    nodule_num = thyroid_results['nodule_num']
                    if nodule_num == 0:
                        nodule_num = 1
                        invalid_selection = True
                else: 
                    nodule_num = 1
                    invalid_selection = True
                    
                thyroid_results = form.cleaned_data

                parenchyma = thyroid_results['parenchyma']
                isthmus = thyroid_results['isthmus']
                rt_vol = thyroid_results['rt_vol']
                lt_vol = thyroid_results['lt_vol']

                composition = thyroid_results['composition']
                echogenicity = thyroid_results['echogenicity']
                shape = thyroid_results['shape']
                margins = thyroid_results['margins']
                foci = thyroid_results['foci']

                lobe = thyroid_results['lobe']
                aspect = thyroid_results['aspect']
                position = thyroid_results['position']

                length = thyroid_results['length']
                width = thyroid_results['width']
                height = thyroid_results['height']

                

                if lobe != 'isthmus':
                    location = f"<br>A nodule in the {lobe} lobe, {aspect} aspect {position}, measuring {length} x {width} x {height} cm, and has the following features:"
                else:
                    location = f"<br>A nodule is seen in the isthmus, measuring {length} x {width} x {height} cm, and has the following features:"
                
                dimensions = [length, width, height]
                scores = [int(composition[-2]), int(echogenicity[-2]), int(shape[-2]), int(margins[-2]), int(foci[-2])]
                
                tr, recommendation = tr_recommendation(dimensions, scores)

                if composition in ['Spongiform, no points for other features (0)', 'Possibly, but not definitely spongiform (0)']:
                    nodule_chr = f"<br>Nodule #{int(nodule_num)}:{location}<br>-Composition: {composition}.<br>"
                else:
                    nodule_chr = f"<br>Nodule #{int(nodule_num)}:{location}<br>-Composition: {composition}.<br>-Echogenicity: {echogenicity}.<br>-Shape: {shape}.<br>-Margins: {margins}.<br>-Echogenic foci: {foci}.<br>{tr}: {recommendation}<br>"
                                
                gland = f"The right thyroid lobe volume: {rt_vol} cc.<br>The left thyroid lobe volume: {lt_vol} cc.<br>Thyroid parenchyma is {parenchyma}.<br>The isthmus measures {isthmus} cm in AP diameter."
                
                try:
                    nodules[(int(nodule_num)-1)] = nodule_chr
                    # nodules.insert(int(nodule_num)-1, nodule_chr)
                except:
                    # if int(nodule_num)>len(nodules):
                    invalid_selection = True
                    pass
                form = NoduleForm(initial={
                                            'parenchyma': parenchyma,
                                            'isthmus': isthmus,
                                            'rt_vol': rt_vol,
                                            'lt_vol': lt_vol, 
                                            'composition': 'Completely or almost completely cystic (0)',
                                            'echogenicity': 'Hyperechoic (1)',
                                            'shape': 'Wider than tall (0)',
                                            'margins': 'Smooth (0)',
                                            'foci': 'No echogenic foci (0)',
                                            'lobe': 'right',
                                            'aspect': 'upper',
                                            'position': 'anteriorly',
                                            'length': 0,
                                            'width': 0,
                                            'height': 0,
                                            })
                return render(request, "thyroid/thyroid.html", context={
                                                                    'form':form, 
                                                                    'gland':gland,
                                                                    'nodules': nodules,
                                                                    'submitted': True,
                                                                    'invalid_selection': invalid_selection,
                                                                    })
            else:
                
                form = NoduleForm()
                return render(request, "thyroid/thyroid.html", context={'form':form})


        elif "reset_form" in request.POST:

            nodules.clear()
            form = NoduleForm()
            return render(request, "thyroid/thyroid.html", context={'form':form})

    else:
        
        form = NoduleForm()

    return render(request, "thyroid/thyroid.html", context={'form':form})


