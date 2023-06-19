# 设置页面样式
st.set_page_config(page_title='Heart Disease Prediction', page_icon=':heart:', layout='wide')

# 设置边栏样式
st.markdown("""
<style>
.sidebar .sidebar-content {
    background-image: linear-gradient(#2e7bcf,#2e7bcf);
    color: white;
}
</style>
""", unsafe_allow_html=True)

# 设置主页面样式
st.markdown("""
<style>
.big-font {
    font-size:40px !important;
    color: black;
}
</style>
""", unsafe_allow_html=True)


import streamlit as st
import pickle

# 添加标题
st.title('Heart Disease Prediction')

# 创建模型选择下拉框
model_names = ['决策树模型', '随机森林模型']  # 模型的名称列表
model_selectbox = st.sidebar.selectbox('Select Model', model_names)

# 根据模型名称加载对应的模型文件
model_file = f'{model_selectbox}.pkl'
with open(model_file, 'rb') as file:
    model = pickle.load(file)

# 创建用户输入表单
st.header('Heart Disease Prediction')
age = float(st.number_input('Age 年龄'))
sex = st.selectbox('Sex 性别 ', ['Male 男', 'Female 女'])
chest_pain_type = st.selectbox('Chest Pain Type 胸痛类型', ['Typical Angina 典型心绞痛', 'Atypical Angina 非典型心绞痛', 'Non-anginal Pain 非神经疼痛', 'Asymptomatic 无症状'])
resting_bp = float(st.number_input('Resting Blood Pressure 休息血压'))
cholesterol = float(st.number_input('Cholesterol 血清胆固醇'))
fasting_bs = st.selectbox('Fasting Blood Sugar 禁食血糖', ['Lower than 120mg/dl 低于 120mg/dl', 'Greater than 120mg/dl 高于 120mg/dl'])
resting_ecg = st.selectbox('Resting ECG 静息心电图结果', ['Normal 正常', 'ST-T wave abnormality 有ST-T波异常', 'Left ventricular hypertrophy 左心室肥大'])
max_hr = float(st.number_input('Maximum Heart Rate 最大心率'))
exercise_angina = st.selectbox('Exercise Induced Angina 运动引起心绞痛', ['No 无', 'Yes 是'])
old_peak = float(st.number_input('ST Depression induced by exercise relative to rest 相对于休息来说运动引起的ST段抑制'))
st_slope = st.selectbox('ST Slope 峰运动ST段的坡度', ['Upsloping 向上倾斜', 'Flat 平', 'Downsloping 向下倾斜'])

# 处理用户输入数据
sex = 0 if sex == 'Male 男' else 1
chest_pain_mapping = {'Typical Angina 典型心绞痛': 4, 'Atypical Angina 非典型心绞痛': 3, 'Non-anginal Pain 非神经疼痛': 2, 'Asymptomatic 无症状': 1}
chest_pain_type = chest_pain_mapping[chest_pain_type]
resting_ecg_mapping = {'Normal 正常': 0, 'ST-T wave abnormality 有ST-T波异常': 2, 'Left ventricular hypertrophy 左心室肥大': 1}
resting_ecg = resting_ecg_mapping[resting_ecg]
exercise_angina = 1 if exercise_angina == 'Yes 是' else 0
st_slope_mapping = {'Upsloping 向上倾斜': 1, 'Flat 平': 0, 'Downsloping 向下倾斜': 2}
st_slope = st_slope_mapping[st_slope]
fasting_bs = 1 if fasting_bs == 'Greater than 120mg/dl 高于 120mg/dl' else 0

def divide_Age(age):
    if age<=35:
        return 0
    elif age>35 and age<=65:
        return 1
    else:
        return 2


def divide_RestingBP(resting_bp):
    if resting_bp<90:
        return 0
    elif resting_bp>140:
        return 2
    else:
        return 1


#小于110，返回0，大于230，返回2，中间为1
def divide_Cholesterol(cholesterol):
    if cholesterol<110:
        return 0
    elif cholesterol>230:
        return 2
    else:
        return 1


#小于110，返回0，大于180，返回2，中间为1
def divide_MaxHR(max_hr):
    if max_hr<110:
        return 0
    elif max_hr>180:
        return 2
    else:
        return 1


#1及以下为0，1到2之间为1，2到3之间为2,其他为3
def divide_Oldpeak(old_peak):
    if old_peak<=1:
        return 0
    elif old_peak>1 and old_peak:
        return 1
    elif old_peak>2 and old_peak<=3:
        return 2
    else: return 3



age = divide_Age(age)
resting_bp = divide_RestingBP(resting_bp)
cholesterol = divide_Cholesterol(cholesterol)
max_hr = divide_MaxHR(max_hr)
old_peak = divide_Oldpeak(old_peak)


# 定义预测函数
def predict(model, age, sex, chest_pain_type, resting_bp, cholesterol, fasting_bs, resting_ecg, max_hr, exercise_angina, old_peak, st_slope):
    # 进行预测
    features = [[age, sex, chest_pain_type, resting_bp, cholesterol, fasting_bs, resting_ecg, max_hr, exercise_angina, old_peak, st_slope]]
    prediction = model.predict(features)[0]
    prediction_proba = model.predict_proba(features)[0]
    return prediction, prediction_proba


# 创建预测按钮
if st.button('Predict 预测'):
    # 调用预测函数
    prediction, prediction_proba = predict(model, age, sex, chest_pain_type, resting_bp, cholesterol, fasting_bs, resting_ecg, max_hr, exercise_angina, old_peak, st_slope)

    # 显示预测结果
    st.subheader('Prediction 预测结果')
    if prediction == 0:
        st.write('Congratulations! You are not at risk of heart disease.恭喜！您没有心脏病的风险。')
    else:
        st.write('You are at risk of heart disease. Please consult a doctor.您有患心脏病的风险，请咨询医生。')

    st.subheader('Prediction Probability 预测概率')
    st.write(f"Not at risk 无风险: {prediction_proba[0] * 100:.2f}%")
    st.write(f"At risk 有风险: {prediction_proba[1] * 100:.2f}%")

# 添加页面底部的版权信息
st.markdown("""
        <style>
        .container {
            display: flex;
        }
        .logo-text {
            font-size:20px;
            padding-top: 5px;
            color: #f9a01b;
        }
        </style>
        """, unsafe_allow_html=True)
footer = """
        <div class='container'>
        <img src='https://avatars.githubusercontent.com/u/76982031?s=200&v=4' width="50" height="50">
        <div class='logo-text'>
        Made by ChatMind AI
        </div>
        </div>
        """
st.markdown(footer,unsafe_allow_html=True)
