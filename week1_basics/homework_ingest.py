import pandas as pd
from sqlalchemy import create_engine

def main():
    # 1. 建立数据库连接
    # 确保用户名密码是 root:root，端口是 5432，数据库是 ny_taxi
    engine = create_engine('postgresql://root:rootroot@localhost:5433/ny_taxi')
    
    print("🚀 开始执行作业脚本...")

    # ==========================================
    # 任务 A: 加载 2025年11月 的绿色出租车数据
    # ==========================================
    # 这就是你刚才发的链接
    url_taxi = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
    
    print(f"1. 正在读取 Parquet 文件: {url_taxi} ...")
    
    # Pandas 直接读取远程 Parquet
    df_taxi = pd.read_parquet(url_taxi)

    print(f"   读取成功！数据量: {len(df_taxi)} 行")
    print("   正在写入数据库表: green_taxi_2025 ... (可能需要几秒钟)")
    
    # 写入表名为 'green_taxi_2025'
    df_taxi.to_sql(name='green_taxi_2025', con=engine, if_exists='replace', chunksize=10000)
    print("✅ 出租车数据入库完成！")

    # ==========================================
    # 任务 B: 加载区域 (Zone) 数据
    # ==========================================
    url_zones = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
    
    print(f"2. 正在读取 Zone CSV: {url_zones} ...")
    df_zones = pd.read_csv(url_zones)
    
    print("   正在写入数据库表: zones ...")
    df_zones.to_sql(name='zones', con=engine, if_exists='replace')
    print("✅ 区域数据入库完成！")

if __name__ == '__main__':
    main()
