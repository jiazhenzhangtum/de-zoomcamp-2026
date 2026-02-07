import pandas as pd
import requests
import io
import gzip


def get_data_info(taxi_type, year, month):
    # 构造下载链接
    base_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"
    file_name = f"{taxi_type}_tripdata_{year}-{month:02d}.csv.gz"
    url = f"{base_url}/{taxi_type}/{file_name}"

    print(f"正在处理: {url} ...")

    try:
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            print(f"❌ 下载失败: {url}")
            return None, 0

        content = response.content

        # Q1: Uncompressed file size (解压后大小)
        with gzip.open(io.BytesIO(content), 'rb') as f_in:
            uncompressed_content = f_in.read()
            file_size_mb = len(uncompressed_content) / (1024 * 1024)

        # Q3-Q5: Row count (行数)
        df = pd.read_csv(io.BytesIO(uncompressed_content))
        row_count = len(df)

        return file_size_mb, row_count

    except Exception as e:
        print(f"发生错误: {e}")
        return None, 0


# --- 把下面这些粘贴到文件的末尾 ---

def solve_homework():
    print("----- 🚀 开始计算作业答案 -----")

    # Q1: Yellow Taxi, 2020-12, 大小
    print("\n[Q1 计算中] 正在下载 Yellow 2020-12 ...")
    size_mb, _ = get_data_info('yellow', 2020, 12)
    if size_mb:
        print(f"✅ [Q1 答案] Yellow 2020-12 解压后大小: {size_mb:.2f} MiB")

    # Q3: Yellow Taxi 2020 全年行数
    total_rows_yellow_2020 = 0
    print("\n[Q3 计算中] 正在计算 Yellow 2020 全年行数 (需下载12个文件)...")
    for m in range(1, 13):
        _, rows = get_data_info('yellow', 2020, m)
        total_rows_yellow_2020 += rows
    print(f"✅ [Q3 答案] Yellow 2020 全年总行数: {total_rows_yellow_2020:,}")

    # Q4: Green Taxi 2020 全年行数
    total_rows_green_2020 = 0
    print("\n[Q4 计算中] 正在计算 Green 2020 全年行数...")
    for m in range(1, 13):
        _, rows = get_data_info('green', 2020, m)
        total_rows_green_2020 += rows
    print(f"✅ [Q4 答案] Green 2020 全年总行数: {total_rows_green_2020:,}")

    # Q5: Yellow Taxi 2021-03 行数
    print("\n[Q5 计算中] 正在计算 Yellow 2021-03 行数...")
    _, rows_yellow_2021_03 = get_data_info('yellow', 2021, 3)
    print(f"✅ [Q5 答案] Yellow 2021-03 总行数: {rows_yellow_2021_03:,}")



if __name__ == "__main__":
    solve_homework()