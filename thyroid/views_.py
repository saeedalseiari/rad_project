from django.shortcuts import render

from .forms import NoduleForm

nodules = []
gland = []

nod = 0


# Create your views here.


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

                if lobe != 'ishmus':
                    location = f"<br>A nodule in the {lobe} lobe, {aspect} aspect {position}, measuring {length} x {width} x {height} cm, and has the following features:"
                else:
                    location = f"A nodule is seen in the isthmus, measuring {length} x {width} x {height} cm, and has the following features:"
                
                nod += 1
                nodule_chr = f"Nodule #{nod}:<br>{location}<br>-Composition: {composition}.<br>-Echogenicity: {echogenicity}.<br>-Shape: {shape}.<br>-Margins: {margins}.<br>-Echogenic foci: {foci}.<br>"
                                
                g = f"The right thyroid lobe volume: {rt_vol} cc.<br>The left thyroid lobe volume: {lt_vol} cc.<br>Thyroid parenchyma is {parenchyma}.<br>The isthmus measures {isthmus} cm in AP diameter."
                
                if gland == []:
                    gland.append(g)
                form = NoduleForm(initial={
                                            'parenchyma': parenchyma,
                                            'isthmus': isthmus,
                                            'rt_vol': rt_vol,
                                            'lt_vol': lt_vol, 
                                            'composition': 'Completely or almost completely cysti (0)',
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

                nodules.append(nodule_chr)
                return render(request, "thyroid/thyroid.html", context={'form':form})
            else:
                
                # print(form.errors.as_data())
                form = NoduleForm()
                return render(request, "thyroid/thyroid.html", context={'form':form})
        elif "show_report" in request.POST:
            # form = NoduleForm()

            
            return render(request, "thyroid/thyroid.html", context={
                                                                    'form':form, 
                                                                    'gland':gland[0],
                                                                    'nodules': nodules,
                                                                    'submitted': True

                                                                    })
    else:
        form = NoduleForm()

    return render(request, "thyroid/thyroid.html", context={'form':form})


