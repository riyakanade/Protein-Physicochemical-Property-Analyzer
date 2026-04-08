import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import numpy as np


st.set_page_config(page_title="Protein Analyzer", layout="wide")

# -------- BACKGROUND IMAGE (LIGHTER) --------
bg = Image.open("background_1.png")

# crop shorter header
width, height = bg.size
bg = bg.crop((0, 0, width, int(height*0.35)))

# draw text
draw = ImageDraw.Draw(bg)

title = "Protein Physicochemical Property Analyzer"

# try large font
try:
    font = ImageFont.truetype("arial.ttf", 60)
except:
    font = ImageFont.load_default()

draw.text((40,40), title, fill="black", font=font)

st.image(bg, use_container_width=True)

# SESSION STATE
if "sequence" not in st.session_state:
    st.session_state.sequence=""

if "run_analysis" not in st.session_state:
    st.session_state.run_analysis=False

if "page" not in st.session_state:
    st.session_state.page="Home"


# -------- TABS NAVIGATION ----------
tab1, tab2, tab3, tab4 = st.tabs(["Home","About","Tool","Team"])

# ---------- HOME ----------
with tab1:

    st.title("Protein Physicochemical Property Analyzer")

    st.write("""
    Welcome to the Protein Physicochemical Property Analyzer. 
    This tool analyzes protein amino acid sequences and computes key 
    physicochemical properties to help understand protein stability 
    and behavior.
    """)

    st.subheader("Features")
    st.write("""
    • Accepts protein sequence or FASTA file  
    • Calculates physicochemical properties  
    • Generates plots and interpretation
    • Downloadable report    
    """)
	
# ---------- ABOUT ----------
with tab2:
    st.title("About This Tool")

    subtab1, subtab2, subtab3 = st.tabs(["Overview","Working","Future"])

    # ---------- OVERVIEW ----------
    with subtab1:

        st.subheader("Project Overview")

        st.markdown("""
The Protein Physicochemical Property Analyzer is a bioinformatics-based 
web application designed to analyze amino acid sequences and compute 
important physicochemical properties of proteins.

This tool performs sequence-based analysis to evaluate protein stability, 
hydrophobicity, charge distribution, thermostability, and solubility. 
The application also generates graphical visualization and provides 
interpretation describing protein characteristics.

The analyzer helps researchers understand structural and functional 
behavior of proteins using only primary sequence information.
""")

        st.subheader("Properties Calculated")

        st.write("""
• Amino acid composition  
• Molecular weight  
• Aromaticity  
• GRAVY  
• Hydropathy profile  
• Aliphatic index  
• Net charge  
• Isoelectric point  
• Instability index  
• Extinction coefficient  
• Hydrophobic percentage  
""")


    # ---------- WORKING ----------
    with subtab2:

        st.subheader("How It Works")

        with st.expander("Step 1: Sequence Input"):
            st.write("""
User enters amino acid sequence manually or uploads FASTA file.
Header lines are removed and sequence is processed.
""")

        with st.expander("Step 2: Composition Analysis"):
            st.write("""
Tool calculates amino acid frequency and protein length.
This helps determine residue distribution.
""")

        with st.expander("Step 3: Physicochemical Calculations"):
            st.write("""
Molecular weight, GRAVY, aromaticity, aliphatic index,
instability index and isoelectric point are computed.
""")

        with st.expander("Step 4: Graph Generation"):
            st.write("""
Amino acid composition graph, hydropathy plot,
and polar vs nonpolar pie chart are generated.
""")

        with st.expander("Step 5: Interpretation"):
            st.write("""
All calculated properties are combined to predict
protein stability, solubility, and structural nature.
""")


    # ---------- FUTURE ----------
    with subtab3:

        st.subheader("Future Scope")

        st.write("""
• Secondary structure prediction integration  
• Protein domain identification  
• Transmembrane helix prediction  
• Subcellular localization prediction  
• Structure prediction integration  
• AI-based property prediction  
• Multiple sequence comparison  
• Batch sequence analysis  
""")

        st.warning("""
Results are prediction-based and depend on sequence input.
Experimental validation is recommended.
""")

# ---------- TOOL (UNCHANGED CODE) ----------
with tab3:

    st.title("Protein Physicochemical Property Analyzer")

    st.write("Example sequence:")
    st.code("MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQANL")

    sequence_input = st.text_area("Paste protein sequence")

    uploaded_file = st.file_uploader("Upload FASTA file", type=["fasta","fa"])

    sequence = ""

    # FASTA reading
    if uploaded_file is not None:

        content = uploaded_file.readlines()
        d = []

        for k in range(0,len(content)):
            line = content[k].decode().strip()

            if not line.startswith(">"):
                d.append(line)

        sequence = "".join(d)

    elif sequence_input:

        lines = sequence_input.split("\n")
        d = []

        for line in lines:
            line = line.strip()

            if not line.startswith(">"):
                d.append(line)

        sequence = "".join(d)

    if st.button("Analyze Protein"):
        if sequence!="":
            st.session_state.sequence = sequence
            st.session_state.run_analysis = True
            st.rerun()
        else:
            st.error("Enter sequence")


# ---------- RESULTS DIRECT (NO NAV PAGE) ----------
if st.session_state.run_analysis:

    sequence = st.session_state.sequence

    # ---------- YOUR FUNCTION (UNCHANGED) ----------
    def analyze_protein(sequence):

        sequence = sequence.upper()
        length = len(sequence)

        st.header("Basic Information")
        st.write("Protein Length:", length)

        aa_list = "ACDEFGHIKLMNPQRSTVWY"

        aa_count = {}
        for aa in aa_list:
            aa_count[aa] = sequence.count(aa)

        st.subheader("Amino Acid Composition")

        aa_line=""
        for aa in aa_list:
            aa_line += aa+":"+str(aa_count[aa])+"  "

        st.write(aa_line)

        fig1, ax1 = plt.subplots(figsize=(5,3))
        ax1.bar(aa_count.keys(), aa_count.values())
        ax1.set_title("Amino Acid Composition")
        st.pyplot(fig1, use_container_width=False)

        st.info("Shows amino acid distribution. Hydrophobic-rich proteins suggest membrane localization, while polar-rich proteins indicate soluble proteins.")


        aa_weights={
        "A":89.09,"C":121.15,"D":133.10,"E":147.13,
        "F":165.19,"G":75.07,"H":155.16,"I":131.17,
        "K":146.19,"L":131.17,"M":149.21,"N":132.12,
        "P":115.13,"Q":146.15,"R":174.20,"S":105.09,
        "T":119.12,"V":117.15,"W":204.23,"Y":181.19
        }

        molecular_weight=sum(aa_weights.get(aa,0) for aa in sequence)
        molecular_weight-=18.015*(length-1)

        st.subheader("Molecular Weight")
        st.write(molecular_weight)

        if molecular_weight > 100000:
            st.info("Large protein — may contain multiple domains")
        elif molecular_weight > 50000:
            st.info("Medium sized protein")
        else:
            st.info("Small protein — suitable for structural studies")


        aromatic=sequence.count("F")+sequence.count("W")+sequence.count("Y")
        aromaticity=aromatic/length

        st.subheader("Aromaticity")
        st.write(aromaticity)

        if aromaticity > 0.1:
            st.info("Aromatic residue rich protein — strong UV absorbance")
        else:
            st.info("Low aromatic content")


        hydropathy={
        "A":1.8,"C":2.5,"D":-3.5,"E":-3.5,
        "F":2.8,"G":-0.4,"H":-3.2,"I":4.5,
        "K":-3.9,"L":3.8,"M":1.9,"N":-3.5,
        "P":-1.6,"Q":-3.5,"R":-4.5,"S":-0.8,
        "T":-0.7,"V":4.2,"W":-0.9,"Y":-1.3
        }

        gravy=sum(hydropathy.get(aa,0) for aa in sequence)/length

        st.subheader("GRAVY")
        st.write(gravy)

        if gravy > 0:
            st.info("Hydrophobic protein — possible membrane protein")
        else:
            st.info("Hydrophilic protein — likely soluble")


        hydro_values=[hydropathy.get(a,0) for a in sequence]

        fig2, ax2 = plt.subplots(figsize=(5,3))
        ax2.plot(hydro_values)
        ax2.set_title("Hydropathy Plot")
        st.pyplot(fig2, use_container_width=False)

        st.info("Positive peaks indicate hydrophobic transmembrane regions. Negative values indicate hydrophilic solvent-exposed regions.")


        A=aa_count["A"]*100/length
        V=aa_count["V"]*100/length
        I=aa_count["I"]*100/length
        L=aa_count["L"]*100/length

        aliphatic_index=A+2.9*V+3.9*(I+L)

        st.subheader("Aliphatic Index")
        st.write(aliphatic_index)

        if aliphatic_index > 100:
            st.info("Highly thermostable protein")
        elif aliphatic_index > 70:
            st.info("Moderately thermostable protein")
        else:
            st.info("Low thermostability")


        positive=sequence.count("K")+sequence.count("R")+sequence.count("H")
        negative=sequence.count("D")+sequence.count("E")

        net_charge=positive-negative

        st.subheader("Net Charge")
        st.write(net_charge)

        if net_charge > 0:
            st.info("Positively charged protein")
        elif net_charge < 0:
            st.info("Negatively charged protein")
        else:
            st.info("Neutral protein")


        pI=7+(net_charge*0.1)

        st.subheader("Isoelectric Point")
        st.write(pI)

        if pI < 7:
            st.info("Acidic protein")
        else:
            st.info("Basic protein")


        instability=(sequence.count("G")+
                     sequence.count("P")+
                     sequence.count("S")+
                     sequence.count("E"))/length*100

        st.subheader("Instability Index")
        st.write(instability)

        if instability < 40:
            st.info("Stable protein")
        else:
            st.info("Unstable protein")


        W=sequence.count("W")
        Y=sequence.count("Y")
        C=sequence.count("C")

        extinction=(5500*W)+(1490*Y)+(125*C)

        st.subheader("Extinction Coefficient")
        st.write(extinction)

        if extinction > 50000:
            st.info("Strong UV absorbing protein")
        else:
            st.info("Weak UV absorption")


        polar="STNQYC"
        nonpolar="AVLIPFWMG"

        polar_count=sum(sequence.count(aa) for aa in polar)
        nonpolar_count=sum(sequence.count(aa) for aa in nonpolar)

        fig3, ax3 = plt.subplots(figsize=(4,4))
        ax3.pie([polar_count,nonpolar_count],
                labels=["Polar","Nonpolar"],
                autopct="%1.1f%%")
        st.pyplot(fig3, use_container_width=False)

        st.info("Polar-rich proteins are soluble, nonpolar-rich proteins suggest membrane association.")


        hydrophobic="AVILMFWY"
        hydrophobic_count=sum(sequence.count(aa) for aa in hydrophobic)
        hydrophobic_percent=hydrophobic_count*100/length

        st.subheader("Hydrophobic %")
        st.write(hydrophobic_percent)

        if hydrophobic_percent > 50:
            st.info("Highly hydrophobic — membrane protein candidate")
        elif hydrophobic_percent > 30:
            st.info("Moderately hydrophobic")
        else:
            st.info("Hydrophilic protein")


        if gravy>0:
            nature="hydrophobic"
        else:
            nature="hydrophilic"

        if instability<40:
            stability="stable"
        else:
            stability="unstable"

        if pI>7:
            charge_type="basic"
        else:
            charge_type="acidic"

        if hydrophobic_percent>50:
            solubility="likely membrane associated"
        else:
            solubility="likely soluble"

        if aliphatic_index>85:
            thermo="highly thermostable"
        elif aliphatic_index>70:
            thermo="moderately thermostable"
        else:
            thermo="low thermostability"


        st.header("Overall Protein Interpretation")

        final_comment=f"""
Based on physicochemical properties, the protein is predicted to be {nature} in nature 
and {stability} under physiological conditions. The theoretical pI indicates the 
protein is {charge_type}. Hydrophobic residue distribution suggests the protein is 
{solubility}. The aliphatic index indicates {thermo}. 

Overall, this protein is predicted to be a {stability}, {nature}, {charge_type} protein 
that is {solubility}. These properties provide insight into protein behavior, 
stability, and possible functional environment.
"""

        st.info(final_comment)


        report=f"""
Protein Physicochemical Analysis Report

Length : {length}
Molecular weight : {molecular_weight}
Aromaticity : {aromaticity}
GRAVY : {gravy}
Aliphatic index : {aliphatic_index}
Net charge : {net_charge}
Isoelectric point : {pI}
Instability index : {instability}
Extinction coefficient : {extinction}
Hydrophobic % : {hydrophobic_percent}

FINAL INTERPRETATION

{final_comment}
"""

        st.download_button(
        "Download Conclusive Report",
        report,
        file_name="Protein_Report.txt"
        )


    analyze_protein(sequence)
	
# ---------- TEAM ----------	
with tab4:

    st.title("Team")

    st.subheader("Project By ")
    st.write("Riya Kanade")
    st.write("MSc Bioinformatics")

    st.write("Email: riyakanade68@gmail.com")

    st.markdown("[LinkedIn Profile](https://www.linkedin.com/in/riya-kanade-920738359?utm_source=share_via&utm_content=profile&utm_medium=member_android)", unsafe_allow_html=True)

    st.divider()

    st.subheader("Guide")
    st.write("Dr Kushagra Kashyap")
    st.write("DES Pune University")