import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import docx
# st.set_page_config(page_title="Rad Report Cleaner",
#                    layout='wide',
#                    initial_sidebar_state='expanded',
#                    page_icon='ultrasound.png')

header = st.container()
data = st.container()
interactive = st.container()
flow = st.container()


with header:
    st.markdown('## Cardiac MRI Reporting Portal (CMRP)')

    st.subheader('Patient Information:')
    fn, ln, c2, g = st.columns([1, 1, 1, 1])
    with fn:
        name = st.text_input('First Name:')
    with ln:
        name = st.text_input('Last Name:')
    with g:
        gender = st.selectbox('Gender:', ['Male', 'Female'])
    with c2:
        mrn = st.text_input('MRN:')

    c3, c4, c5 = st.columns([1, 1, 1])
    with c3:
        age = st.number_input('Age:', min_value=0.0, step=1.0)
    with c4:
        wt = st.number_input('Weight (kg):', min_value=1.0, step=0.5)
    with c5:
        ht = st.number_input('Height (cm)', min_value=1.0, step=1.0)


bsa = round(((wt*ht)/3600)**0.5, 2)

with data:
    lv1, lv2, lv3 = st.columns([2, 2, 2])
    with lv1:
        ledv = st.number_input('LV-EDV', min_value=1.0, step=1.0)
    with lv2:
        lesv = st.number_input('LV-ESV', min_value=1.0, step=1.0)
    with lv3:
        lmm = st.number_input('Muscle Mass', min_value=1.0, step=1.0)

    rv1, rv2 = st.columns([2, 2])
    with rv1:
        redv = st.number_input('RV-EDV', min_value=1.0, step=1.0)
    with rv2:
        resv = st.number_input('RV-ESV', min_value=1.0, step=1.0)


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

lv = [
    ['LV Ejection Fraction (LVEF) %', '58-76/58-75', lvef],
    ['End diastolic Volume (EDV) ml', '88-168/115-198', ledv],
    ['End Diastolic Volume Indexed (EDVI) ml/m2', '57-92/63-98', ledvi],
    ['End Systolic Volume (ESV) ml', '23-60/30-75', lesv],
    ['End Systolic Volume Indexed (ESVI) ml/m2', '15-34/16-38', lesvi],
    ['Stroke Volume (SV) ml', '58-114/76-132', lsv],
    ['Stroke Volume Indexed (SVI) ml/m2', '38-63/41-65', lsvi],
    ['Myocardial Mass (ED) g', '72-144/108-184', lmm],
    ['Myocardial Mass Indexed (ED) g/m2', '48-77/58-91', lmmi],

]

rv = [
    ['RV Ejection Fraction (RVEF) %', '58-76/58-75', rvef],
    ['End diastolic Volume (EDV) ml', '88-168/115-198', redv],
    ['End Diastolic Volume Indexed (EDVI) ml/m2', '57-92/63-98', redvi],
    ['End Systolic Volume (ESV) ml', '23-60/30-75', resv],
    ['End Systolic Volume Indexed (ESVI) ml/m2', '15-34/16-38', resvi],
    ['Stroke Volume (SV) ml', '58-114/76-132', rsv],
    ['Stroke Volume Indexed (SVI) ml/m2', '38-63/41-65', rsvi],
]

df = pd.DataFrame(lv, columns=['Left_Ventricle',
                  'Normal_Female_Male', 'Results'])

dfr = pd.DataFrame(rv, columns=['Right_Ventricle',
                                'Normal_Female_Male', 'Results'])

with interactive:
    st.subheader('LV Functional Analysis')
    col = [['<b>Left_Ventricle</b>'],
           ['<b>Normal_Female_Male</b>'], ['<b>Results</b>']]

    cel = [df.Left_Ventricle, df.Normal_Female_Male, df.Results]

    fig = go.Figure(data=go.Table(columnwidth=[3, 1, 1], header=dict(
        values=col, fill_color='#FD8E72', align='left'), cells=dict(values=cel, fill_color='#E5ECF6', align='left')))
    fig.update_layout(
        height=220,
        margin=dict(l=0, r=0, b=0, t=0))
    fig.update_traces(cells_font=dict(family='Courier', size=14))
    st.write(fig)

# RV
    st.subheader('RV Functional Analysis')
    colr = [['<b>Right_Ventricle</b>'],
            ['<b>Normal_Female_Male</b>'], ['<b>Results</b>']]

    celr = [dfr.Right_Ventricle, dfr.Normal_Female_Male, dfr.Results]

    figr = go.Figure(data=go.Table(columnwidth=[3, 1, 1], header=dict(
        values=colr, fill_color='#FD8E72', align='left'), cells=dict(values=celr, fill_color='#E5ECF6', align='left')))
    figr.update_layout(
        height=220,
        margin=dict(l=0, r=0, b=0, t=0))
    figr.update_traces(cells_font=dict(family='Courier', size=14))

    st.write(figr)
    st.write('Reference values according to Maceira et al., 2006')

with flow:
    if st.checkbox('Flow measurements'):
        st.markdown('#### Aortic Valve')
        ao1, ao2, ao3 = st.columns([1, 1, 1])

        with ao1:
            aovf = st.number_input('Forward flow:')
        with ao2:
            aovp = st.number_input('Backward flow:')
        with ao3:
            aopsv = st.number_input('Peak systolic velocity:')


# -----------------
#   SAVE DOC FILE
# -----------------
    save = st.button('Save to Word Document')

    if save:
        doc = docx.Document()
        table_rtf = doc.add_table(rows=1, cols=3)

        # Adding heading in the 1st row of the table
        row = table_rtf.rows[0].cells
        row[0].text = 'Left Ventricle'
        row[1].text = 'Normal Female/Male'
        row[2].text = 'Results'

        for satr in lv:
            # Adding a row and then adding data in it.
            row = table_rtf.add_row().cells

            row[0].text = satr[0]
            row[1].text = satr[1]
            row[2].text = str(satr[2])
        table_rtf.style = 'Table Grid'
        doc.save('document.rtf')
