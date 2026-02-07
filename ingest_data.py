import pandas as pd
from sqlalchemy import create_engine
from time import time

def main():
    # 1. 配置数据库连接
    # 格式: postgresql://用户:密码@主机:端口/数据库名
    # 注意：端口是 5432，因为我们是通过 localhost 访问
    engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
    
    # 2. 定义分块读取器 (Iterator)
    # chunksize=100000 意味着每次只把 10 万行载入内存，而不是 130 万行
    df_iter = pd.read_csv('yellow_tripdata_2021-01.csv', iterator=True, chunksize=100000)

    # 3. 准备第一块数据 (用来建表)
    print("正在获取第一块数据以初始化表格...")
    df = next(df_iter)

    # 数据清洗：把字符串格式的日期转换成真正的 datetime 对象
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # 4. 创建表结构 (只传表头，不传数据)
    # n=0 表示只取表头。if_exists='replace' 表示如果表存在就删了重建
    df.head(0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')

    # 5. 插入第一块数据
    df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')
    print("✅ 第一块数据 (10万行) 插入完毕！")

    # 6. 循环插入剩余的所有数据
    while True: 
        try:
            t_start = time()
            
            # 获取下一块 (如果没有数据了，这里会报错 StopIteration，跳到 except)
            df = next(df_iter)

            # 数据清洗 (每一块都要做！)
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            # 插入数据 (注意这里必须是 append，追加模式)
            df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

            t_end = time()
            print(f'插入了一块数据... 花费时间: {t_end - t_start:.3f} 秒')

        except StopIteration:
            print("🎉 所有数据已成功写入数据库！")
            break

if __name__ == '__main__':
    main()
