import pandas as pd
from sqlalchemy import create_engine

# 1. 建立数据库连接
# 格式: postgresql://用户名:密码@主机地址:端口/数据库名
# 注意：因为 Python 是在 WSL 里跑，而数据库在 Docker 里，
# Docker Desktop 把端口映射到了 localhost，所以这里用 localhost 是能通的。
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

try:
    # 2. 连接测试
    print("正在尝试连接数据库...")
    engine.connect()
    print("✅ 数据库连接成功！")

    # 3. 读取 CSV 文件 (为了测试，我们只读前 100 行)
    print("正在读取 CSV 文件...")
    df = pd.read_csv('yellow_tripdata_2021-01.csv', nrows=100)
    
    # 修复日期格式 (把字符串变成真正的日期时间格式)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # 4. 写入数据库
    # name='yellow_taxi_data' 是我们将要在数据库里创建的表名
    print("正在把数据写入表格 yellow_taxi_data ...")
    df.to_sql(name='yellow_taxi_data', con=engine, if_exists='replace', index=False)
    
    print("🎉 成功！数据已写入。请去 pgAdmin 查看！")

except Exception as e:
    print("❌ 出错了：")
    print(e)
