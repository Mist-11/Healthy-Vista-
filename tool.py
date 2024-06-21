import numpy as np
from random import Random
from django.core.mail import send_mail
from users.models import EmailVerifyRecord
from django.conf import settings  # 邮箱配置
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import warnings
warnings.filterwarnings("ignore")


def danger(df):
    # 计算生存函数的对数差分，近似风险函数
    risk_function = -np.diff(np.log(df[0])) / np.diff(df.index / 24)
    # 计算生存概率密度
    surv_probs_mid = (df[0].values[:-1] + df[0].values[1:]) / 2  # 使用中点近似
    prob_density = risk_function * surv_probs_mid
    return round(df.index.values[:-1][np.argmax(prob_density)] / 24)  # 寻找概率密度最大的时间点


def random_str(randomlength=8):
    """
    随机字符串
    :param randomlength: 字符串长度
    :return: String 类型字符串
    """
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_code_email(email, send_type="register"):
    """
    发送电子邮件
    :param email: 要发送的邮箱
    :param send_type: 邮箱类型
    :return: True/False
    """
    email = email.encode("ascii").decode("ascii")
    email_record = EmailVerifyRecord()
    # 将给用户发的信息保存在数据库中
    code = random_str(6)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.send_time = datetime.datetime.now()
    email_record.save()

    # 如果为注册类型
    if send_type == "register":
        email_title = "Registration Activation"
        email_body = ("Your registration verification code is: {0}, this code is valid for 2 minutes, "
                      "please verify it in time.").format(code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if not send_status:
            return False
    if send_type == "retrieve":
        email_title = "Password Recovery"
        email_body = ("Your email registration verification code is: {0}, this code is valid for 2 minutes, "
                      "please verify it in time.").format(code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if not send_status:
            return False
    return True


def draw_BC(df, user, time):
    df.index = df.index / 24
    sns.set_theme(style="whitegrid")
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号无法显示的问题
    plt.figure(figsize=(20, 10))
    sns.lineplot(data=df, markers=True, dashes=False, linewidth=3, marker='o', markersize=10, color='cyan')

    plt.xlim(0, 365)  # 设置X轴的视觉范围
    plt.xticks(range(0, 366, 30))  # 从0到365，每30天一个刻度

    plt.xlabel('天数', fontsize=30)
    plt.ylabel('生存概率', fontsize=30)
    plt.title('患者未来一年的生存概率', fontsize=40)

    plt.tick_params(labelsize=30)
    plt.legend(labels=['生存概率'], fontsize=30)

    sns.despine()
    image_path = f"./rubbish/{time}_{user}.png"
    plt.savefig(image_path, format='PNG')
    return image_path

