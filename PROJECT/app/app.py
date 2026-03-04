
import os
import sqlite3
import streamlit as st
import numpy as np
import joblib
import smtplib
from email.mime.text import MIMEText

# ---------------- DATABASE ----------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR,"database","health.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

conn=get_connection()
cursor=conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS reports(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_email TEXT,
condition TEXT,
risk_score REAL,
risk_level TEXT,
doctor_comment TEXT,
precautions TEXT
)
""")

conn.commit()
conn.close()

# ---------------- EMAIL FUNCTION ----------------

def send_email(receiver, precautions):

    sender_email="reddysaipriya2727@gmail.com"
    sender_password="xnbx jqts eush zewl"

    body=f"""
Hello,

Thank you for using the AI Clinical Screening System.

Doctor Recommendations:

{precautions}

Stay healthy.
"""

    msg=MIMEText(body)
    msg["Subject"]="Health Screening Advice"
    msg["From"]=sender_email
    msg["To"]=receiver

    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(sender_email,sender_password)
    server.sendmail(sender_email,receiver,msg.as_string())
    server.quit()

# ---------------- PAGE ----------------

st.set_page_config(page_title="AI Clinical Screening",layout="wide")

st.markdown("""
<style>

.stApp{
background:linear-gradient(to right,#dbeafe,#fce7f3);
}

/* Sidebar color */
section[data-testid="stSidebar"]{
background:#1e293b;
color:white;
}

/* Buttons styling */
.stButton>button {
background-color:#2563eb;
color:white;
border-radius:8px;
height:40px;
width:100%;
font-size:16px;
font-weight:bold;
border:none;
}

.stButton>button:hover {
background-color:#1d4ed8;
color:white;
}

/* Result box */
.result-box{
padding:20px;
border-radius:15px;
font-size:22px;
text-align:center;
font-weight:bold;
}

.high{
background:#dc2626;
color:white;
}

.low{
background:#16a34a;
color:white;
}

</style>
""",unsafe_allow_html=True)

# ---------------- SESSION ----------------

if "user" not in st.session_state:
    st.session_state.user=None
    st.session_state.role=None

# ---------------- SIDEBAR ----------------

st.sidebar.title("Account")

option=st.sidebar.selectbox(
"Login As",
["Patient Login","Doctor Login","Patient Signup"]
)

# ---------------- SIGNUP ----------------


if option=="Patient Signup":

    st.sidebar.subheader("Create Account")

    name = st.sidebar.text_input(
        "Name",
        placeholder="Enter your full name"
    )

    email = st.sidebar.text_input(
        "Email",
        placeholder="Enter your email ID"
    )

    password = st.sidebar.text_input(
        "Password",
        type="password",
        placeholder="Create your password"
    )

    if st.sidebar.button("Register"):

        conn=get_connection()
        cursor=conn.cursor()

        cursor.execute(
        "INSERT INTO users(name,email,password) VALUES(?,?,?)",
        (name,email,password)
        )

        conn.commit()
        conn.close()

        st.sidebar.success("Registration Successful. Please login.")

# ---------------- PATIENT LOGIN ----------------
# ---------------- PATIENT LOGIN ----------------

if option=="Patient Login":

    st.sidebar.subheader("Patient Login")

    email = st.sidebar.text_input(
        "Email",
        placeholder="Enter your email ID"
    )

    password = st.sidebar.text_input(
        "Password",
        type="password",
        placeholder="Enter your password"
    )

    if st.sidebar.button("Login"):

        conn=get_connection()
        cursor=conn.cursor()

        cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email,password)
        )

        user=cursor.fetchone()

        if user:
            st.session_state.user=email
            st.session_state.role="patient"
            st.sidebar.success("Login Successful")

        else:
            st.sidebar.error("Invalid Credentials")

        conn.close()

# ---------------- DOCTOR LOGIN ----------------
# ---------------- DOCTOR LOGIN ----------------

if option=="Doctor Login":

    st.sidebar.subheader("Doctor Login")

    email = st.sidebar.text_input(
        "Doctor Email",
        placeholder="Enter doctor email ID"
    )

    password = st.sidebar.text_input(
        "Password",
        type="password",
        placeholder="Enter doctor password"
    )

    if st.sidebar.button("Login"):

        if email=="doctor@hospital.com" and password=="doctor123":

            st.session_state.user=email
            st.session_state.role="doctor"
            st.sidebar.success("Doctor Login Successful")

        else:
            st.sidebar.error("Invalid Doctor Login")

# ---------------- MAIN APP ----------------

if st.session_state.user:

    st.title("🧠 AI Clinical Screening System")

    st.info("Main risk factor considered: **Obesity (BMI & Waist Circumference)**")

    pcos_model=joblib.load("models/pcos_model.pkl")
    pcos_scaler=joblib.load("models/pcos_scaler.pkl")

    mets_model=joblib.load("models/mets_model.pkl")
    mets_scaler=joblib.load("models/mets_scaler.pkl")

# ---------------- PATIENT PANEL ----------------

    if st.session_state.role=="patient":

        st.subheader("Enter Medical Details")

        condition=st.selectbox(
        "Select Screening",
        ["PCOS (Female)","Metabolic Syndrome (Male)"]
        )

        if condition=="PCOS (Female)":

            bmi=st.number_input("BMI",10.0,60.0,25.0)
            waist=st.number_input("Waist Circumference",20.0,60.0,30.0)
            whr=st.number_input("Waist Hip Ratio",0.5,2.0,0.9)
            weight=st.number_input("Weight",30.0,150.0,60.0)

            sys_bp=st.number_input("Systolic BP",80.0,200.0,120.0)
            dia_bp=st.number_input("Diastolic BP",40.0,150.0,80.0)
            rbs=st.number_input("Blood Sugar",60.0,300.0,100.0)

            lh=st.number_input("LH",0.0,50.0,5.0)
            fsh=st.number_input("FSH",0.0,50.0,5.0)
            fsh_lh=st.number_input("FSH/LH Ratio",0.0,5.0,1.0)

            amh=st.number_input("AMH",0.0,20.0,2.0)
            tsh=st.number_input("TSH",0.0,10.0,2.5)
            prl=st.number_input("PRL",0.0,100.0,10.0)

            input_data=np.array([[bmi,waist,whr,weight,
                                  sys_bp,dia_bp,rbs,
                                  lh,fsh,fsh_lh,
                                  amh,tsh,prl]])

            model=pcos_model
            scaler=pcos_scaler

        else:

            waist=st.number_input("Waist Circumference",50.0,150.0,85.0)
            bmi=st.number_input("BMI",15.0,60.0,25.0)
            glucose=st.number_input("Blood Glucose",60.0,300.0,100.0)

            triglycerides=st.number_input("Triglycerides",50.0,500.0,150.0)
            hdl=st.number_input("HDL",10.0,100.0,50.0)
            age=st.number_input("Age",18,80,30)

            input_data=np.array([[waist,bmi,glucose,triglycerides,hdl,age]])

            model=mets_model
            scaler=mets_scaler

        if st.button("Predict Risk"):

            input_scaled=scaler.transform(input_data)

            pred=model.predict(input_scaled)[0]
            prob=model.predict_proba(input_scaled)[0][1]

            risk="High Risk" if pred==1 else "Low Risk"

            if pred==1:
                st.markdown(f"<div class='result-box high'>⚠ HIGH RISK<br>{round(prob*100,2)}%</div>",unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='result-box low'>✅ LOW RISK<br>{round(prob*100,2)}%</div>",unsafe_allow_html=True)

            conn=get_connection()
            cursor=conn.cursor()

            cursor.execute("""
            DELETE FROM reports
            WHERE user_email=? AND condition=?
            """,(st.session_state.user,condition))

            cursor.execute("""
            INSERT INTO reports(user_email,condition,risk_score,risk_level)
            VALUES(?,?,?,?)
            """,(st.session_state.user,condition,float(prob),risk))

            conn.commit()
            conn.close()

        # show report
        conn=get_connection()
        cursor=conn.cursor()

        cursor.execute("""
        SELECT risk_score,risk_level,doctor_comment,precautions
        FROM reports WHERE user_email=?
        """,(st.session_state.user,))

        report=cursor.fetchone()

        if report:

            score,level,comment,precautions=report

            st.subheader("Your Report")

            st.write("Risk Score:",round(float(score)*100,2),"%")
            st.write("Risk Level:",level)

            if comment:
                st.write("Doctor Comment:",comment)

            if precautions:
                st.write("Precautions:",precautions)

        conn.close()

# ---------------- DOCTOR DASHBOARD ----------------

    if st.session_state.role=="doctor":

        st.subheader("Doctor Dashboard")

        conn=get_connection()
        cursor=conn.cursor()

        cursor.execute("SELECT * FROM reports")

        patients=cursor.fetchall()

        for p in patients:

            id,email,cond,score,level,comment,precautions=p

            st.write("Patient:",email)
            st.write("Condition:",cond)
            st.write("Risk:",round(float(score)*100,2),"%")
            st.write("Level:",level)

            comment_input=st.text_area("Doctor Comment",key=f"c{id}")
            precaution_input=st.text_area("Precautions",key=f"p{id}")

            if st.button("Save Advice",key=f"s{id}"):

                cursor.execute("""
                UPDATE reports
                SET doctor_comment=?,precautions=?
                WHERE id=?
                """,(comment_input,precaution_input,id))

                conn.commit()

                send_email(email,precaution_input)

                st.success("Advice saved and email sent")

            st.markdown("---")

        conn.close()

else:

    st.title("Please Login to Continue")

