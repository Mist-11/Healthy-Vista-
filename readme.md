## 1. 准备工作

在开始之前，请确保已经按照 `requirements.txt` 安装了相应的第三方库和包。

## 2. 数据库以及邮箱配置

### 数据库配置
首先，在 MySQL 中创建一个名为 "Survival prediction system" 的数据库，然后在 `./Survivalpredictionsystem/settings.py`
文件中配置数据库连接信息。示例如下：

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'NAME': 'Survival prediction system',  # 数据库名称
        'HOST': '127.0.0.1',  # MySQL 数据库的 IP 地址
        'PORT': 3306,  # MySQL 运行的端口
        'USER': 'root',  # 数据库用户名
        'PASSWORD': '123456'  # 数据库密码
    }
}
```
### 邮箱配置
在 `./Survivalpredictionsystem/settings.py`文件中配置邮箱连接信息。示例如下：
```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 发送邮件配置
EMAIL_HOST = 'smtp.qq.com'  # 您的邮箱服务器名称
EMAIL_PORT = 465  # 你的邮件服务商的服务端口
EMAIL_HOST_USER = '111@qq.com'  # 填写自己邮箱
EMAIL_HOST_PASSWORD = '123456'  # 在邮箱中设置的客户端授权密码
EMAIL_FROM = '111@qq.com'  # 收件人看到的发件人
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_SSL = True  # 使用SSL加密
EMAIL_USE_TLS = False
```
请根据您的实际情况修改这些配置参数。

## 3. 数据库迁移

在命令行中进入项目文件夹，并执行以下命令以完成数据库的迁移：

```
python manage.py makemigrations
python manage.py migrate
```

## 4. 创建管理员账户

```
python manage.py createsuperuser
```

根据提示创建一个系统管理员账户。

## 5. 运行服务

最后，在命令行中进入项目文件夹，并执行以下命令启动服务：

```
python manage.py runserver

```

命令行会出现如下结果：

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
June 21, 2024 - 00:17:10
Django version 3.2.25, using settings 'Survivalpredictionsystem.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

```

现在可以通过访问本机地址 http://127.0.0.1:8000/ 来访问本服务系统。

## 6.源代码说明

### 目录结构详细说明

- **ALLPDF**: 存储所有预测结果的 PDF 文件。
- **users**: 用户模块，处理用户相关的功能。
- **backstage**: 后台管理模块，提供系统后台管理功能。
- **cancer**: 疾病预测模块，包含针对癌症的预测功能。
- **model**: 存储人工智能训练好的模型。
- **rubbish**: 临时存放中间文件的目录。
- **Survivalpredictionsystem**: 系统的基本设置。
- **static**: 存储 JS、CSS、Image 等静态资源。
- **templates**: 前端页面的 HTML 模板。
- **manage.py**: 系统启动文件，用于启动整个系统。
- **report.py**: 生成预测报告的模块。
- **requirements.txt**: 系统安装所需的第三方包与环境配置文件。
- **tool.py**: 各个模块常用的函数、方法和对象等。


