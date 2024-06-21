import pickle
import torch
import torchtuples as tt
from pycox.models import DeepHitSingle
from cancer import in_features, out_features, batch_norm, dropout, num_nodes, labtrans, x_mapper, HE_columns


def uselightgbm(df):
    df = df.astype(float)
    with open('./model/HD_lightgbm.pkl', 'rb') as f:
        clf_load = pickle.load(f)  # 将模型存储在变量clf_load中

    # 使用加载的模型进行预测
    test_pred = clf_load.predict(df)
    return test_pred


def usedeephit(df):
    # 网络架构
    net = tt.practical.MLPVanilla(in_features, num_nodes, out_features, batch_norm, dropout)
    # 模型
    model = DeepHitSingle(net, duration_index=labtrans.cuts)
    model.net.load_state_dict(torch.load("./model/BC_deephit_model.pth"))
    surv = x_mapper.transform(df).astype('float32')
    surv = model.interpolate(10).predict_surv_df(surv)
    return surv


def userandomforest(df):
    df.columns = HE_columns
    df = df.astype(float)
    with open('./model/HE_RandomForest.pkl', 'rb') as f:
        clf_load = pickle.load(f)  # 将模型存储在变量clf_load中

    # 使用加载的模型进行预测
    test_pred = clf_load.predict(df)
    return test_pred


if __name__ == "__main__":
    import pandas as pd
    from cancer import new_columns
    import seaborn as sns
    import matplotlib.pyplot as plt
    import matplotlib

    data_values = [
        75.65, 22, 10, 2, 16, 6.04, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0,
        0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
        0, 1, 0, 0, 0
    ]
    df = pd.DataFrame([data_values], columns=new_columns)
    df = usedeephit(df)
    print(df)
    print(type(df))
    df.index = df.index / 24
    sns.set_theme(style="whitegrid")
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号无法显示的问题
    plt.figure(figsize=(20, 10))
    plot = sns.lineplot(data=df, markers=True, dashes=False, linewidth=3, marker='o', markersize=10, color='cyan')

    plt.xlim(0, 365)  # 设置X轴的视觉范围
    plt.xticks(range(0, 366, 30))  # 从0到365，每30天一个刻度

    plt.xlabel('天数', fontsize=16)
    plt.ylabel('生存概率', fontsize=16)
    plt.title('患者未来一年的生存概率', fontsize=20)

    plt.tick_params(labelsize=14)
    plt.legend(labels=['生存概率'], fontsize=16)

    sns.despine()

    # Show the plot
    plt.show()
