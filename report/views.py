from django.shortcuts import render
from . forms import ReportForm
import re



def clean_text(text):
    text = text.replace("<", " less than ")
    text = text.replace(">", " more than ")

    temp = []
    final = []
    replacement_box = [('intra hepatic', 'intrahepatic'),
                       ('focal abnormality', 'focal lesions'),
                       ('Hepaticveins', 'hepatic veins'),
                       ('tree:Normal', 'tree: Normal'),
                       ('Free fluid/Collections: ', ''), ('(cm)','cm'), ('(cc)', 'cc'),
                       ('&', 'and'), (':', ': '), (':  ', ': '),
                       (' .', '.'), (',.\n', '.\n'), (' .', '.'),
                       ('##', ''), ('( ', '('), ('cbd', 'CBD'), (' )', ')'),
                       ('ivc', 'IVC'), ('echopattern', 'echotexture'),
                       ('inhomogeneous', 'heterogenous')
                       ]

    letters = "a b c d e f g h i j k l m n o p q r s t u v w x y z 1 2 3 4 5 6 7 8 9 0 \n . , = - + & ? ' ’ : ( ) / ; #"

    text2 = [x for x in text if x.lower() in letters]
    text2 = "".join(text2)
    text3 = text2.split("\n")
    for i in text3:
        i = " ".join(i.split())
        temp.append(i)

    text3 = [x.strip() + "\n" for x in temp if len(x) > 0]
    filter_chars = {".", ":", "?"}
    for x in text3:

        if x[len(x) - 2] not in filter_chars and len(x) > 3:
            x = x.strip() + ".\n"

        final.append(x)

    report = "".join(final)

    for a, b in replacement_box:
        report = report.replace(a, b)

    final_report = ""

    rep1 = []

    for x in report:
        l = [x.lstrip() for x in report.split(":\n")]

    for line in l:
        if len(line) > 0:
            rep1.append((line[0].upper() + line[1:]))
            
    rep = ": ".join(rep1)

    # -------------

    repfin = rep.splitlines()

    for line in repfin:
        if len(line) > 0:
            final_report += line[0].upper() + line[1:] + "\n"
        else:
            final_report += "\n"

    return final_report



hedging = [
    "density",
    "opacity",
    "apparent",
    "appears",
    "possible",
    "possibly",
    "unlikely",
    "borderline",
    "could",
    "doubtful",
    "suspected",
    "suspecion",
    "indeterminate",
    "identified",
    "seen",
    "no_definite",
    "no_gross",
    "no_obvious",
    "no_overt",
    "no_evidence",
    "no_significant",
    "probable",
    "probably",
    "suggusted",
    "suggesting",
    "suspicious_for",
    "vague",
    "clinical_correlation",
    "equivocal",
]


normal = [
    "unremarkable",
    "essentially_normal",
    "relatively_normal",
    "grossly_normal",
    "nonspecific",
]

vocabs = ["there", "bony", "inhomogeneous", "in_shape", "mass_lesion"]

v = {
    "there": "consider removing",
    "bony": "osseous",
    "inhomogeneous": "heterogeneous",
    "in_shape": "consider removing",
    "mass lesion": "mass",
}


# def report_score():
def tokenize(text):
    tokens = re.split(r"([.,;:!^ ])", text)
    return tokens


def process_report(txt):
    # The text is split into sentences to know the number of sentences
    sents = txt.split(".")
    number_of_sents = len(sents)
    """ 
    hm: number of hedging terms
    sent_list: list of sentences in the text

    """
    hm = 0  # hedging meter
    ni = 0  # normal impostor
    voc = 0  # vocabulary
    sent_list = tokenize(txt)

    processed_txt = []
    mid_step = ""
    """
    Variables
    """
    new_txt = []
    items_index = []
    length = len(sent_list)
    """
    Word processing
    The terms with no... are combined into one term, example:
    no obvious --> no_obvious
    essentially normal --> essentially_normal
    """
    bigrams_combiner = ["no", "essentially", "relatively", "grossly", "in"]

    for i in range(length):
        if sent_list[i].lower().lstrip("\n") in bigrams_combiner:
            new_txt.append(sent_list[i] + "_" + sent_list[i + 2])
            items_index.append(i)

        else:
            new_txt.append(sent_list[i])

    items_index.reverse()
    for x in items_index:
        new_txt.pop(x + 2)
        new_txt.pop(x + 1)

    for s in new_txt:
        original_word = s
        word = original_word.lower().lstrip("\n")
        if word in hedging:
            processed_txt.append(
                '<span id="hedging"> '
                + s
                + " <small><sup>HEDGING</sup></small></span>",
            )
            mid_step = ""
            hm += 1
        elif word in vocabs:
            processed_txt.append(
                '<span id="vocab">'
                + s
                + "<small><sup>"
                + v[word].upper()
                + "</sup></small></span>",
            )
            mid_step = ""
            voc += 1
        elif word in normal:
            processed_txt.append(
                '<span id="imposter">'
                + s
                + "<small><sup>NORMAL IMPOSTER</sup></small></span>",
            )
            mid_step = ""
            ni += 1
            hm += 0.33
        else:
            processed_txt.append(s)

    processed_txt.append(mid_step)
    h_score = int((hm / number_of_sents) * 100)
    ni_score = int((ni / number_of_sents) * 100)
    voc_score = int((voc / number_of_sents) * 100)
    report = "".join(processed_txt)
    report = report.replace("_", " ")
    report = report.replace("\n", "<br>")

    return report, h_score, ni_score, voc_score

def c_select(num):
    if num > 40:
        c = '<span class="mb-2 bg-danger text-white">'
    elif num < 15:
        c = '<span class="mb-2 bg-success text-white">'
    else:
        c = '<span class="mb-2 bg-warning text-dark">'
    return c


# Create your views here.
def report_cleaner(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            submitted = True
            primary_report = form.cleaned_data['dirty_report']
            clean_report = clean_text(primary_report)
            final_report = process_report(clean_report)
            report = final_report[0]
            h = final_report[1]
            ni = final_report[2]
            voc = final_report[3]
            h_score = c_select(h) + f" Hedging Score: {100-h}% </span>"
            ni_score = c_select(ni) + f" Normal Imposters Score: {100-ni}% </span>"
            voc_score = c_select(voc) + f" Vocabulary Score: {100-voc}% </span>"
            q = int(sum([h * 3, ni, voc]) / 3)
            q_score = c_select(h) + f" Quality Score: {100-q}% </span>"

            # print(form.cleaned_data['dirty_report'].capitalize())
            form = ReportForm(initial={'dirty_report':clean_report})
            return render(request, 'report/report.html', context = {'form': form, 
                            'report': report,
                            'clean_report': clean_report,
                            'h_score': h_score,
                            'ni_score' : ni_score,
                            'voc_score': voc_score,
                            'q_score': q_score,
                            'submitted': submitted})

        return render(request, 'report/report.html', context = {'form': form})
    else:
        form = ReportForm()
    return render(request, 'report/report.html', context = {'form': form})
