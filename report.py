from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import cm

import pandas as pd
from datetime import datetime

# 获取默认样式表并添加中文字体样式
pdfmetrics.registerFont(TTFont('simfang', 'simfang.ttf'))
pdfmetrics.registerFont(TTFont('simkai', 'simkai.ttf'))
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='ChineseBigTitle', fontName='simkai', fontSize=27, leading=40, bold=True, alignment=1))
styles.add(ParagraphStyle(name='ChineseTitle', fontName='simfang', fontSize=12, leading=15, bold=True))
styles.add(ParagraphStyle(name='ChineseNormal', fontName='simfang', fontSize=12, leading=15))
styles.add(ParagraphStyle(name='ChineseNote', fontName='simfang', fontSize=8, leading=10))

page_width, page_height = letter
table_width = page_width * 0.7  # 假设希望表格宽度为页面宽度的70%
four_widths = [table_width * 0.3, table_width * 0.2, table_width * 0.3, table_width * 0.2]  # 四列表格宽度
six_widths = [table_width * 0.25, table_width * 0.1, table_width * 0.15, table_width * 0.25, table_width * 0.1,
              table_width * 0.15]  # 六列表格宽度


# 是/否变量还原
def HEconvert_to_yes_no(*args):
    # 使用列表推导式来生成转换后的值列表
    return tuple("是" if x == 2 else "否" for x in args)


def HDconvert_to_yes_no(*args):
    # 使用列表推导式来生成转换后的值列表
    return tuple("是" if x == 1 else "否" for x in args)


def format_notes(notes):
    if not notes:
        return "没有内容"
    notes_formatted = []  # 初始化结果列表
    # 处理除最后一个元素外的所有元素
    for i in range(len(notes) - 1):
        notes_formatted.append(f"{i + 1}.{notes[i]}<br/>")
    # 处理最后一个元素，添加特殊前缀
    notes_formatted.append(f"结论：<br/>{notes[-1]}")
    return "".join(notes_formatted)  # 将列表合并成一个字符串


# 页脚批注
def footer(canvas, doc):
    width, height = A4
    canvas.saveState()
    canvas.setStrokeColorRGB(0, 0, 0)
    canvas.setLineWidth(1)
    line_y = 2.5 * cm
    canvas.line(2 * cm, 2 * cm, width - 2 * cm, 2 * cm)
    footer_text = "*上述结果仅供参考，具体请结合临床医生意见。"
    style = styles['ChineseNote']
    p = Paragraph(footer_text, styles['ChineseNote'])
    w, h = p.wrap(doc.width, doc.bottomMargin)
    p.drawOn(canvas, doc.leftMargin, line_y - 1 * cm)  # 根据需要调整位置
    canvas.restoreState()


def logo_title(reportname):
    img = Image("./static/image/logo2.png")
    img.drawWidth = img.drawWidth * 0.12
    img.drawHeight = img.drawHeight * 0.12
    title = Paragraph(reportname, styles['ChineseBigTitle'])  # 大标题
    table_data = [[img, title]]
    table = Table(table_data)
    table_style = TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        ('ALIGN', (1, 0), (1, 0), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 所有单元格垂直居中
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),  # 背景颜色
        ('TOPPADDING', (0, 0), (-1, -1), -30),  # 删除上边距
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),  # 删除下边距
        ('LEFTPADDING', (0, 0), (-1, -1), -90),  # 设置左边距为负值以左移表格
    ])
    table.setStyle(table_style)
    return table


def userinfo(user, sex, age, time):
    time = datetime.strptime(time, "%Y%m%d%H%M%S")
    time = time.strftime("%Y-%m-%d %H:%M:%S")  # 格式化一下时间
    patient_data = [['用户:', user, '  ', '性别:', sex, '  ', '年龄:', age, '  ', '预测时间:', time]]
    patient_table_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'simfang'),  # 使用simfang字体
        ('FONTSIZE', (0, 0), (-1, -1), 12),  # 字体大小为12
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 所有单元格居中对齐
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 所有单元格垂直居中
    ])

    patient_table = Table(patient_data)
    patient_table.setStyle(patient_table_style)
    return patient_table


def threelinetable(cols):
    table_style = 0
    if cols == 4:
        table_style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0, colors.white),
            ('LINEABOVE', (0, 0), (-1, 0), 1.5, colors.black),  # 表头上方粗线
            ('LINEBELOW', (0, 0), (-1, 0), 0.75, colors.black),  # 表头下方的粗线
            ('LINEBELOW', (0, -1), (-1, -1), 1.5, colors.black),  # 表位下方的粗线线
            ('LINEAFTER', (1, 0), (1, -1), 0.75, colors.black),  # 中间竖线
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),  # 表头背景设为白色
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),  # 2、4居中对齐
            ('ALIGN', (3, 0), (3, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),  # 第一、三列左对齐
            ('ALIGN', (2, 0), (2, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'simfang'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
    if cols == 6:
        table_style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0, colors.white),
            ('LINEABOVE', (0, 0), (-1, 0), 1.5, colors.black),  # 表头上方粗线
            ('LINEBELOW', (0, 0), (-1, 0), 0.75, colors.black),  # 表头下方的粗线
            ('LINEBELOW', (0, -1), (-1, -1), 1.5, colors.black),  # 表位下方的粗线线
            ('LINEAFTER', (2, 0), (2, -1), 0.75, colors.black),  # 中间竖线
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),  # 表头背景设为白色
            ('ALIGN', (1, 0), (2, -1), 'CENTER'),  # 2、3、5、6居中对齐
            ('ALIGN', (4, 0), (5, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),  # 第一、四列左对齐
            ('ALIGN', (3, 0), (3, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'simfang'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
    return table_style


def BC_Report(image_path, parameters, user, sex, time, time_point):
    df = pd.DataFrame()
    for key, value in parameters.items():
        if isinstance(value, list):  # 如果值是列表
            df[f'{key}'] = [value.index(1)]  # 以键的名称和序号作为列名
        else:  # 如果值不是列表
            df[key] = [value]  # 直接添加到DataFrame
    # print(df.columns)
    age = df['age_at_diagnosis'].iloc[0]
    size = df['size'].iloc[0]
    lymph_nodes_positive = df['lymph_nodes_positive'].iloc[0]
    stage = df['stage'].iloc[0]
    lymph_nodes_removed = df['lymph_nodes_removed'].iloc[0]
    NPI = df['NPI'].iloc[0]
    grade = df['grade'].iloc[0]
    histological = df['histological'].iloc[0]
    ER_IHC_status = df['ER_IHC_status'].iloc[0]
    ER_Expr = df['ER_Expr'].iloc[0]
    PR_Expz = df['PR_Expz'].iloc[0]
    HER2_IHC_status = df['HER2_IHC_status'].iloc[0]
    HER2_SNP6_state = df['HER2_SNP6_state'].iloc[0]
    Her2_Expr = df['Her2_Expr'].iloc[0]
    Treatment = df['Treatment'].iloc[0]
    inf_men_status = df['inf_men_status'].iloc[0]
    group = df['group'].iloc[0]
    cellularity = df['cellularity'].iloc[0]
    Pam50_Subtype = df['Pam50_Subtype'].iloc[0]
    int_clust_memb = df['int_clust_memb'].iloc[0]
    site = df['site'].iloc[0]
    Genefu = df['Genefu'].iloc[0]
    stage = ["0期", "Ⅰ期", "Ⅱ期", "Ⅲ期", "Ⅳ期"][int(stage)]
    grade = ["1级", "2级", "3级"][grade]
    histological = \
        ["浸润性导管癌", "导管原位癌", "浸润性小叶癌", "小叶原位癌", "髓样癌", "黏液癌", "管内乳头状癌", "乳头状癌",
         "管状癌", "隐匿性癌", "乳腺癌特异性炎性癌", "乳腺佩吉特癌"][histological]
    ER_IHC_status = ["阳性", "阴性"][ER_IHC_status]
    ER_Expr = ["阴性", "阳性"][ER_Expr]
    PR_Expz = ["阴性", "阳性"][PR_Expz]
    HER2_IHC_status = ["0", "1+", "2+", "3+"][HER2_IHC_status]
    HER2_SNP6_state = ["阴性", "弱阳性", "阳性"][HER2_SNP6_state]
    Her2_Expr = ["阴性", "阳性"][Her2_Expr - 1]
    Treatment = ["手术治疗", "化疗", "放射治疗", "激素治疗", "靶向治疗", "免疫治疗", "内分泌治疗", "生物治疗"][
        Treatment]
    inf_men_status = ["右乳", "左乳"][inf_men_status]
    group = ["第1类", "第2类", "第3类", "第4类", "第5类"][group]
    cellularity = ["高", "温和", "低"][cellularity]
    Pam50_Subtype = \
        ["LumA管腔A型", "LumB管腔B型", "HER2过表达型", "Base基底样型", "Normal正常乳腺组织", "Basal三阴性乳腺癌"][
            Pam50_Subtype]
    int_clust_memb = ["4ER", "3", "9", "7", "5", "8", "10", "1", "2", "6"][int_clust_memb]
    site = ["乳头", "乳晕", "导管", "小叶", "其他结构"][site]
    Genefu = ["第1类", "第2类", "第3类", "第4类"][Genefu]

    # PDF生成
    pdf_path = f"./AllPDF/{time}_{user}.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    story = [logo_title('乳腺癌生存分析报告单'), Spacer(1, 10)]  # 标题+logo

    # 用户基本信息
    patient_table = userinfo(user, sex, age, time)
    story.append(patient_table)
    story.append(Spacer(1, 10))  # 表间空隙

    # 输入信息
    data = [
        ["项目", "结果", "项目", "结果"],
        ["患者年龄", age, "肿瘤大小（cm）", size],
        ["样本中含癌细胞的淋巴结数量", lymph_nodes_positive, "乳腺癌所处阶段", stage],
        ["手术移除淋巴结总数", lymph_nodes_removed, "NPI指数", NPI],
        ["组织学分级", grade, "乳腺癌类型", histological],
        ["IHC检测下雌激素受体", ER_IHC_status, "雌激素对癌细胞受体", ER_Expr],
        ["孕激素对癌细胞受体", PR_Expz, "IHC检测HER2蛋白的表达水平", HER2_IHC_status],
        ["SNP6评估HER2", HER2_SNP6_state, "癌症对HER2表达", Her2_Expr],
        ["患者接受的治疗", Treatment, "肿瘤位于哪侧", inf_men_status],
        ["患者所属类特征", group, "化疗后癌细胞量", cellularity],
        ["PAM50测试结果", Pam50_Subtype, "癌症分子亚型的基因表达", int_clust_memb],
        ["主要分布区域", site, "Genefu分类", Genefu]
    ]
    table = Table(data, colWidths=four_widths)
    table.setStyle(threelinetable(4))
    story.append(table)
    story.append(Spacer(1, 12))

    # 生存预测图片
    img = Image(image_path)
    img_width = page_width * 0.8
    img_height = img.drawHeight * (img_width / img.drawWidth)
    img.drawWidth, img.drawHeight = img_width, img_height
    img.hAlign = 'CENTER'
    story.append(img)
    story.append(Spacer(1, 12))

    # 较大风险点
    notes = Paragraph(f"该患者可能在第{time_point}天后存在较大风险，请多多注意。", styles['ChineseNormal'])
    story.append(notes)
    story.append(Spacer(1, 12))

    # 生成PDF
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return pdf_path


def HD_Report(surv, data, user, time):
    # print(surv)
    age = int(data['age'])
    anaemia = int(data['anaemia'])
    creatinine_phosphokinase = int(data['creatinine_phosphokinase'])
    diabetes = int(data['diabetes'])
    ejection_fraction = int(data['ejection_fraction'])
    high_blood_pressure = int(data['high_blood_pressure'])
    platelets = int(data['platelets'])
    serum_creatinine = float(data['serum_creatinine'])
    serum_sodium = int(data['serum_sodium'])
    sex = int(data['sex'])
    smoking = int(data['smoking'])
    durtime = int(data['time'])

    # 作息检查
    keys_to_check = [anaemia, diabetes, high_blood_pressure, smoking]
    count = sum(int(data[key]) for key in keys_to_check if key in data)
    if count >= 2:
        note1 = "预测用户的身体处于亚健康状况，请在平时多注意作息规律。"
    else:
        note1 = "预测用户的身体状态良好，请继续保持。"

    # 血样检查
    if creatinine_phosphokinase > 170:
        num = (creatinine_phosphokinase - 200) / creatinine_phosphokinase * 100
        note2 = f"血液CPK酶水平较高,超出正常水平{str(round(num))}%。请注意调节作息，避免高强度运动和熬夜等行为，避免暴饮暴食。"
    else:
        note2 = "血液CPK酶水平正常，请继续保持。"

    if 50 < ejection_fraction < 65:
        note3 = "心脏的供血功能较为正常，请继续保持。"
    elif 40 < ejection_fraction <= 50:
        note3 = "心脏的供血功能较弱，请加强锻炼并且及时就医。"
    elif ejection_fraction <= 40:
        note3 = "射血分数过低，可能会出现心力衰竭，发生心源性猝死的几率也会大大增加，请马上就医！"
    elif 70 > ejection_fraction >= 65:
        note3 = "心脏的供血功能较强，请避免高强度锻炼并且及时就医。"
    else:
        note3 = "射血分数过高，心脏收缩功能可能出现问题，请避免饮酒，避免剧烈运动，不要熬夜、过度劳累，及时去医院就诊。"

    if 0.5 < serum_creatinine < 1.2:
        note4 = "血肌酐水平正常，请继续保持。"
    elif serum_creatinine <= 0.5:
        note4 = "血肌酐水平较高，如果不进行治疗，可能会发展为严重的肾衰竭，请及时就医。"
    else:
        note4 = "血肌酐水平较低，请注意规律生活，加强锻炼。"

    if 135 < serum_sodium < 145:
        note5 = "血清钠水平正常，请继续保持。"
    else:
        note5 = "血清纳水平异常，可能出现头晕、恶心，严重时可导致意识混乱、抽搐和昏迷。请及时就医。"

    if 100000 < platelets < 300000:
        note6 = "血小板水平正常，请继续保持。"
    elif platelets >= 300000:
        note6 = "血小板水平过高，将导致血液过于粘稠，增加血栓形成的风险，请及时就医。"
    else:
        note6 = "血小板水平过低，血液凝固能力下降，导致易出血的情况。可能会急剧降低血容量，影响心脏功能，导致心脏应激反应。请多食用含有维生素B12、叶酸和铁的食物，例如动物肝脏、牛奶、鸡蛋、菠菜、紫甘蓝等等。"

    # 结论
    if surv[0] == 1:
        note7 = "预测对象存在较大致命风险，请及时去医院查看治疗。"
    else:
        note7 = "预测对象暂无致命风险，请继续保持。"

    # 还原类别数据
    anaemia, diabetes, high_blood_pressure, smoking = HDconvert_to_yes_no(anaemia, diabetes, high_blood_pressure,
                                                                          smoking)
    sex = ['男', "女"][sex]

    # PDF生成
    pdf_path = f"./AllPDF/{time}_{user}.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    story = [logo_title('心脏病生存分析报告单'), Spacer(1, 10)]  # 标题+logo
    # 用户基本信息
    patient_table = userinfo(user, sex, age, time)
    story.append(patient_table)
    story.append(Spacer(1, 10))  # 表间空隙

    # 输入信息
    # 二元指标
    title = Paragraph('一.二元指标', styles['ChineseTitle'])
    story.append(title)
    story.append(Spacer(1, 10))

    data = [
        ["项目", "结果", "项目", "结果"],
        ["血红蛋白是否减少", anaemia, "是否抽烟", smoking],
        ["是否有糖尿病", diabetes, "是否有高血压", high_blood_pressure]
    ]
    table = Table(data, colWidths=four_widths)
    table.setStyle(threelinetable(4))
    story.append(table)
    story.append(Spacer(1, 10))

    # 数值指标
    title = Paragraph('二.数值指标', styles['ChineseTitle'])
    story.append(title)
    story.append(Spacer(1, 10))

    data = [
        ["项目", "结果", "参考范围", "项目", "结果", "参考范围"],
        ["血肌酐水平(mg/dL)", serum_creatinine, "0.5-1.2", "血液CPK酶水平(mcg/L)", creatinine_phosphokinase, "24-170"],
        ["血小板水平(k/ml)", platelets, "10^6-3×10^6", "射血分数", ejection_fraction, "50-65"],
        ["血清纳(Mmol/L)", serum_sodium, "135-145", "患病时长(天)", durtime, ""]
    ]
    table = Table(data, colWidths=six_widths)
    table.setStyle(threelinetable(6))
    story.append(table)
    story.append(Spacer(1, 10))
    # 分析情况
    title = Paragraph('三.分析情况', styles['ChineseTitle'])
    story.append(title)
    story.append(Spacer(1, 10))
    notes_text = f"1.{note1}<br/>2.{note2}<br/>3.{note3}<br/>4.{note4}<br/>5.{note5}<br/>6.{note6}<br/>结论：<br/>{note7}"
    notes = Paragraph(notes_text, styles['ChineseNormal'])
    story.append(notes)

    # 生成报告
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return pdf_path


def HE_report(surv, data, user, time):
    Age = int(data['Age'])
    Sex = int(data['Sex'])
    Steroid = int(data['Steroid'])
    Antivirals = int(data['Antivirals'])
    Fatigue = int(data['Fatigue'])
    Malaise = int(data['Malaise'])
    Anorexia = int(data['Anorexia'])
    Liver_Big = float(data['Liver_Big'])
    Liver_Firm = int(data['Liver_Firm'])
    Spleen_Palpable = int(data['Spleen_Palpable'])
    Spiders = int(data['Spiders'])
    Ascites = int(data['Ascites'])
    Varices = int(data['Varices'])
    Bilirubin = float(data['Bilirubin'])
    Alk_Phosphate = int(data['Alk_Phosphate'])
    Sgot = int(data['Sgot'])
    Albumin = float(data['Albumin'])
    Protime = int(data['Protime'])
    Histology = int(data['Histology'])

    note = []
    # 作息检查
    keys_to_check = [Fatigue, Malaise, Anorexia]
    count = sum(int(data[key]) for key in keys_to_check if key in data)
    if count >= 2:
        note.append("预测用户的总体健康状态较差，请在平时生活中多注意规律生活。")
    else:
        note.append("预测用户的身体状态较良好，请继续保持。")

    keys_to_check = [Liver_Big, Liver_Firm]
    count = sum(int(data[key]) for key in keys_to_check if key in data)
    if count >= 1:
        note.append("用户可能存在肝硬化或其他严重肝病的迹象，请及时就医。")
    else:
        note.append("用户的肝状态比较良好，请继续保持。")

    if Spleen_Palpable == 0:
        note.append('脾脏较正常，无明显并发症。')
    else:
        if Liver_Firm == 0:
            note.append('脾脏肿大过度，请及时就医。')
        else:
            note.append('脾脏肿大过度，可能是由肝硬化引起的门脉高压，血液流动阻力增加造成的。')

    if Spiders == 1:
        note.append(
            '用户存在蜘蛛痣，可能由于肝脏不能有效地处理激素导致的血管增生。肝功能减退导致雌激素代谢减少，雌激素水平升高刺激血管扩张形成')

    if Ascites == 1 and Varices == 1:
        note.append('由于肝硬化引起的门脉高压，液体积聚在腹腔中，而低白蛋白血症减少了血浆胶体渗透压。同时使得正常通过肝脏的血液流找到其他途径绕行，'
                    '导致血管过度充血、扩张，形成静脉曲张。腹水和静脉曲张都是肝硬化常见的并发症之一，可以通过药物治疗和可能的内镜手术干预，以防止'
                    '病情进一步恶化。')
    elif Ascites == 0 and Varices == 1:
        note.append('由于肝硬化引起的门脉高压，使得正常通过肝脏的血液流找到其他途径绕行，导致血管过度充血、扩张，形成静脉曲张。可以通过药物治疗和'
                    '可能的手术干预，以防止内出血。')
    elif Ascites == 1 and Varices == 0:
        note.append('由于肝硬化引起的门脉高压，液体积聚在腹腔中，而低白蛋白血症减少了血浆胶体渗透压。肝硬化常见的并发症之一。可以通过药物治疗干预'
                    '，改善积液情况。')

    if Bilirubin > 1.0:
        note.append('肝脏代谢异常导致胆红素过高，易诱发进而发生溶血性黄疸，对细胞有毒害作用。')
    elif Bilirubin <= 1.0:
        note.append('胆红素水平正常，请继续保持。')

    if Alk_Phosphate > 500:
        note.append('胆管可能发生堵塞，请及时就医！')
    elif 135 < Alk_Phosphate <= 500:
        note.append('碱性磷酸酶水平较高，请配合医院其他检查排查病因。')
    else:
        note.append('碱性磷酸酶水平正常，请继续保持。')

    if Sgot > 40:
        note.append('谷草转氨酶水平较高，疑似病毒性肝炎或肝硬化，心肌细胞和肝细胞线粒体可能发生损伤。')
    else:
        note.append('谷草转氨酶水平正常，请继续保持。')

    if Albumin > 35:
        note.append('白蛋白水平较高，疑似患有慢性肝脏疾病，请及时去医院排查。')
    elif Albumin < 25:
        note.append('白蛋白水平较低，疑似患有亚急性重症肝炎、慢性中度以上持续性肝炎、肝硬化、肝癌等。请及时就医！')

    if Protime > 46:
        note.append('活化部分凝血活酶时间延长，可能患有严重的凝血酶原（因子 Ⅱ）、因子 Ⅴ、Ⅹ 和纤维蛋白原缺乏。如肝脏疾病、阻塞性黄疸，'
                    '请及时就医。')
    elif Protime < 14:
        note.append('活化部分凝血活酶时间缩短，处于高凝状态，可能患有血栓性疾病，请及时就医。')
    else:
        note.append('活化部分凝血活酶时间正常，请继续保持。')

    if surv[0] == 1:
        note.append('用户目前较无重大风险，请继续保持。')
    else:
        note.append('预测对象存在较大致命风险，请及时去医院查看治疗。')

    # 还原类别变量
    (Steroid, Antivirals, Fatigue, Malaise, Anorexia, Liver_Big, Liver_Firm, Spleen_Palpable, Spiders, Ascites, Varices,
     Histology) = (HEconvert_to_yes_no(Steroid, Antivirals, Fatigue, Malaise, Anorexia, Liver_Big, Liver_Firm,
                                       Spleen_Palpable, Spiders, Ascites, Varices, Histology))
    Sex = ['男', '女'][Sex - 1]

    # PDF生成
    pdf_path = f"./AllPDF/{time}_{user}.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    story = [logo_title('肝炎生存分析报告单'), Spacer(1, 10)]  # 标题+logo
    # 用户基本信息
    patient_table = userinfo(user, Sex, Age, time)
    story.append(patient_table)
    story.append(Spacer(1, 10))  # 表间空隙

    # 输入信息
    # 二元指标
    title = Paragraph('一.二元指标', styles['ChineseTitle'])
    story.append(title)
    story.append(Spacer(1, 10))

    data = [
        ["项目", "结果", "项目", "结果"],
        ["是否使用类固醇药物", Steroid, "是否使用抗病毒药物", Antivirals],
        ["是否疲劳", Fatigue, "是否感到不适", Malaise],
        ["是否厌食", Anorexia, "是否肝脏肿大", Liver_Big],
        ["是否肝脏硬化", Liver_Firm, "脾脏是否可触及", Spleen_Palpable],
        ["是否出现蜘蛛痣", Spiders, "是否出现腹水", Ascites],
        ["是否出现静脉曲张", Varices, "组织学检查是否异常", Histology],
    ]

    table = Table(data, colWidths=four_widths)
    table.setStyle(threelinetable(4))
    story.append(table)
    story.append(Spacer(1, 10))

    # 数值指标
    title = Paragraph('二.数值指标', styles['ChineseTitle'])
    story.append(title)
    story.append(Spacer(1, 10))

    data = [
        ["项目", "结果", "参考范围", "项目", "结果", "参考范围"],
        ["胆红素水平(mg/dL)", Bilirubin, "0.1-1.0", "碱性磷酸酶水平(U/L)", Alk_Phosphate, "45-135"],
        ["谷草转氨酶水平(μ/L)", Sgot, "0-40", "白蛋白水平(g/dL)", Albumin, "3.5-5.5"],
        ["凝血时间(s)", Protime, "24-36", "", "", ""]
    ]
    table = Table(data, colWidths=[table_width * 0.25, table_width * 0.1, table_width * 0.15, table_width * 0.25,
                                   table_width * 0.1, table_width * 0.15])
    table.setStyle(threelinetable(6))
    story.append(table)
    story.append(Spacer(1, 10))
    # 分析情况
    title = Paragraph('三.分析情况', styles['ChineseTitle'])
    story.append(title)
    story.append(Spacer(1, 10))
    notes = Paragraph(format_notes(note), styles['ChineseNormal'])
    story.append(notes)
    # 生成报告
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return pdf_path
