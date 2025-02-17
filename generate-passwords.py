# 生成固定8位数的纯数字密码本(所有组合) 生成后的文本文件有一亿行数据，大约占磁盘900MB~1GB不等，依赖设备CPU性能，谨慎操作。
def generate_password_file(filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for i in range(10**8):  # 生成 00000000 到 99999999
            password = f"{i:08}"  # 格式化为 8 位数，不足补零
            file.write(password + '\n')

if __name__ == "__main__":
    generate_password_file("password_list.txt")
    print("密码本生成完成！")