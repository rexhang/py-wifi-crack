# WiFi 密码破解工具

这是一个简单的 WiFi 密码破解工具，使用 Python 编写，基于 `pywifi` 库实现。该工具可以扫描附近的 WiFi 网络，并尝试使用密码本中的密码进行暴力破解。此外，项目还提供了一个生成固定 8 位纯数字密码本的脚本。

## 项目结构

```
crack-wifi/
├── crack-wifi.py           # 主程序，用于扫描 WiFi 并尝试破解密码
├── generate-passwords.py   # 生成固定8位纯数字密码本(./password_list.txt)的脚本 密码本包含8位数字的所有组合 生成后的文本文件有一亿行数据，大约占磁盘900MB~1GB不等，依赖设备CPU性能，谨慎操作。
├── passwords.txt           # 密码本，包含待尝试的密码列表
├── password_list.txt       # 生成的8位纯数字密码本
├── requirements.txt        # 项目依赖库
└── README.md               # 项目说明文档
```

## 依赖库

本项目依赖于 `pywifi` 库，您可以通过以下命令安装所需的依赖库：

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 安装依赖

确保已安装 Python 3.x，并安装所需的依赖库。

```bash
pip install -r requirements.txt
```

### 2. 生成密码本

运行 `generate-passwords.py` 脚本，生成一个包含所有8位纯数字组合的密码本(./password_list.txt)，生成后可以用来替换替换 `passwords.txt`

```bash
python generate-passwords.py
```

生成的密码本将保存为 `password_list.txt`，包含从 `00000000` 到 `99999999` 的所有 8 位数字组合。

### 3. 准备密码本

将可能的 WiFi 密码按行写入 `passwords.txt` 文件中，每个密码占一行。您可以直接使用生成的 `password_list.txt` 作为密码本。

### 4. 运行程序

运行 `crack-wifi.py` 脚本。

```bash
python crack-wifi.py
```

### 5. 扫描 WiFi 网络

程序将扫描附近的 WiFi 网络，并显示它们的 SSID 和信号强度。

### 6. 选择目标 WiFi

输入目标 WiFi 的序号（根据信号强度排序），程序将开始尝试破解密码。

### 7. 查看结果

如果密码本中包含正确的密码，程序将输出破解成功的密码；否则，程序将提示破解失败。

## 示例

### 生成密码本

运行 `generate-passwords.py` 后，您将看到类似以下的输出：

```
密码本生成完成！
```

生成的 `password_list.txt` 文件将包含从 `00000000` 到 `99999999` 的所有 8 位数字组合。

### 扫描 WiFi 网络

运行 `crack-wifi.py` 后，您将看到类似以下的输出：

```
当前设备使用的无线网卡为: wlan0
开始扫描附近的Wi-Fi网络，请等待8秒...
扫描Wi-Fi网络完成！
--- Wi-Fi按扫描得到的顺序进行排列 ---
SSID: Home-WiFi, 信号强度: -45
SSID: Office-WiFi, 信号强度: -60
--- Wi-Fi按信号强度的顺序进行排列（由强到弱 1 ~ N） ---
1: SSID: Home-WiFi, 信号强度: -45
2: SSID: Office-WiFi, 信号强度: -60
```

### 选择目标 WiFi

输入目标 WiFi 的序号（例如 `1`），程序将开始尝试破解密码：

```
请输入需要破解的wifi序号(信号强度值越大，信号越好)：1
开始破解Wi-Fi(SSID)： Home-WiFi
正在尝试密码: 12345678
密码 12345678 连接失败！
正在尝试密码: 87654321
密码 87654321 成功连接！
破解成功！Wi-Fi(SSID) <Home-WiFi> 的密码是： 87654321
```

## 注意事项

- **合法性**：请确保您仅在合法授权的范围内使用此工具。未经授权的 WiFi 破解行为是非法的。
- **密码本**：密码本的质量直接影响破解的成功率。建议使用常见的密码组合或字典文件。
- **网络接口**：程序默认使用第一个无线网卡接口。如果您的设备有多个无线网卡，请确保选择正确的接口。
- **生成密码本**：生成的 `password_list.txt` 文件较大（大约占磁盘900MB~1GB不等），请确保磁盘空间充足。

## 许可证

本项目基于 MIT 许可证开源。详情请参阅 [LICENSE](LICENSE) 文件。

## 免责声明

本工具仅供学习和研究使用，请勿用于非法用途。使用者应对自己的行为负责，作者不对任何滥用行为承担责任。

---

如有任何问题或建议，欢迎提交 Issue 或 Pull Request。
