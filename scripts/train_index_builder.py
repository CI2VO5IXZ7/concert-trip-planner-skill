#!/usr/bin/env python3
"""
train_index_builder.py - 下载12306 train_list.js 并建"车站→车次"倒排索引
用法:
    python3 train_index_builder.py [--force] [--data-dir DIR]
    
    --force      强制重建索引（忽略缓存）
    --data-dir   数据目录（默认 scripts同目录下的 data/）
    
输出文件:
    data/train_list.js          原始数据
    data/train_index.json       倒排索引: {站名: [{车次, 起点, 终点, train_no, 类型}...]}
    data/train_by_no.json       正向索引: {车次号: {起点, 终点, train_no, 类型}}
    data/metadata.json          元数据: {last_modified, file_hash, train_count, station_count}
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import URLError

TRAIN_LIST_URL = "https://kyfw.12306.cn/otn/resources/js/query/train_list.js"
CACHE_MAX_AGE = 86400 * 7  # 7天内不重新下载（调图频率低）

def download_train_list(data_dir: str, force: bool = False) -> tuple[str, bool]:
    """下载 train_list.js，返回 (文件路径, 是否有更新)"""
    js_path = os.path.join(data_dir, "train_list.js")
    meta_path = os.path.join(data_dir, "metadata.json")
    
    # 检查缓存
    if not force and os.path.exists(js_path) and os.path.exists(meta_path):
        age = time.time() - os.path.getmtime(js_path)
        if age < CACHE_MAX_AGE:
            print(f"缓存有效（{age/3600:.0f}小时前），跳过下载", file=sys.stderr)
            return js_path, False
    
    print("正在下载 train_list.js ...", file=sys.stderr)
    req = Request(TRAIN_LIST_URL, headers={"User-Agent": "Mozilla/5.0"})
    
    try:
        with urlopen(req, timeout=120) as resp:
            # 检查 Last-Modified
            last_modified = resp.headers.get("Last-Modified", "")
            new_hash = hashlib.md5(resp.read()).hexdigest()
            
            # 检查是否真的有更新
            if not force and os.path.exists(meta_path):
                with open(meta_path) as f:
                    meta = json.load(f)
                if meta.get("file_hash") == new_hash:
                    print("数据无变化，跳过重建", file=sys.stderr)
                    # 更新访问时间
                    os.utime(js_path)
                    return js_path, False
            
            # 重新下载（刚才read消耗了流）
            resp2 = urlopen(req, timeout=120)
            data = resp2.read()
            
            os.makedirs(data_dir, exist_ok=True)
            with open(js_path, "wb") as f:
                f.write(data)
            
            # 保存元数据
            meta = {
                "last_modified": last_modified,
                "file_hash": new_hash,
                "download_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "file_size": len(data)
            }
            with open(meta_path, "w") as f:
                json.dump(meta, f, ensure_ascii=False, indent=2)
            
            print(f"下载完成: {len(data)/1024/1024:.1f}MB, Last-Modified: {last_modified}", file=sys.stderr)
            return js_path, True
            
    except (URLError, TimeoutError) as e:
        print(f"下载失败: {e}", file=sys.stderr)
        if os.path.exists(js_path):
            print("使用本地缓存", file=sys.stderr)
            return js_path, False
        raise


def parse_train_list(js_path: str) -> dict:
    """解析 train_list.js，返回 {日期: [{code, train_no, start, end, type}...]}"""
    with open(js_path, "r", encoding="utf-8") as f:
        raw = f.read()
    
    match = re.search(r"var train_list\s*=\s*(\{.*\})", raw, re.DOTALL)
    if not match:
        raise ValueError("无法解析 train_list.js")
    
    data = json.loads(match.group(1))
    
    result = {}
    for date, categories in data.items():
        trains = []
        for train_type, train_list in categories.items():
            for t in train_list:
                code_raw = t.get("station_train_code", "")
                train_no = t.get("train_no", "")
                # 解析 "G1(北京南-上海)" → code=G1, start=北京南, end=上海
                m = re.match(r"^([^(]+)\(([^)]*?)-([^)]*?)\)$", code_raw)
                if m:
                    trains.append({
                        "code": m.group(1),
                        "train_no": train_no,
                        "start": m.group(2),
                        "end": m.group(3),
                        "type": train_type
                    })
        result[date] = trains
    
    return result


def build_indexes(trains_by_date: dict) -> tuple[dict, dict]:
    """建倒排索引和正向索引"""
    # 取最新日期的数据作为主索引
    dates = sorted(trains_by_date.keys(), reverse=True)
    trains = trains_by_date[dates[0]]
    print(f"使用 {dates[0]} 的数据建索引（{len(trains)} 趟车）", file=sys.stderr)
    
    # 倒排索引: 站名 → [车次列表]
    station_index = {}
    # 正向索引: 车次号 → 车次信息
    train_index = {}
    
    for t in trains:
        code = t["code"]
        info = {
            "code": code,
            "train_no": t["train_no"],
            "start": t["start"],
            "end": t["end"],
            "type": t["type"]
        }
        
        # 正向索引
        train_index[code] = info
        
        # 倒排索引：起点和终点
        for station in [t["start"], t["end"]]:
            if station not in station_index:
                station_index[station] = []
            station_index[station].append(info)
    
    return station_index, train_index


def save_indexes(data_dir: str, station_index: dict, train_index: dict, meta: dict):
    """保存索引文件"""
    # 倒排索引
    inv_path = os.path.join(data_dir, "train_index.json")
    with open(inv_path, "w", encoding="utf-8") as f:
        json.dump(station_index, f, ensure_ascii=False)
    print(f"倒排索引: {inv_path} ({len(station_index)} 个车站)", file=sys.stderr)
    
    # 正向索引
    fwd_path = os.path.join(data_dir, "train_by_no.json")
    with open(fwd_path, "w", encoding="utf-8") as f:
        json.dump(train_index, f, ensure_ascii=False)
    print(f"正向索引: {fwd_path} ({len(train_index)} 趟车)", file=sys.stderr)
    
    # 更新元数据
    meta["train_count"] = len(train_index)
    meta["station_count"] = len(station_index)
    meta["index_build_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
    meta_path = os.path.join(data_dir, "metadata.json")
    with open(meta_path, "w") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def query_station(station_name: str, data_dir: str):
    """查询某站所有车次"""
    idx_path = os.path.join(data_dir, "train_index.json")
    if not os.path.exists(idx_path):
        print("索引不存在，请先运行不带参数的命令建索引", file=sys.stderr)
        sys.exit(1)
    
    with open(idx_path, "r", encoding="utf-8") as f:
        index = json.load(f)
    
    trains = index.get(station_name, [])
    if not trains:
        print(f"未找到车站: {station_name}", file=sys.stderr)
        # 尝试模糊匹配
        matches = [k for k in index.keys() if station_name in k]
        if matches:
            print(f"你是不是想查: {', '.join(matches[:10])}", file=sys.stderr)
        sys.exit(1)
    
    print(json.dumps(trains, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="12306 train_list.js 索引构建器")
    parser.add_argument("--force", action="store_true", help="强制重建索引")
    parser.add_argument("--data-dir", default=None, help="数据目录")
    parser.add_argument("--query", default=None, help="查询某站所有车次")
    args = parser.parse_args()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = args.data_dir or os.path.join(script_dir, "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    
    if args.query:
        query_station(args.query, data_dir)
        return
    
    # 下载
    js_path, updated = download_train_list(data_dir, force=args.force)
    
    # 检查是否需要重建索引
    meta_path = os.path.join(data_dir, "metadata.json")
    inv_path = os.path.join(data_dir, "train_index.json")
    
    if not updated and os.path.exists(inv_path) and not args.force:
        with open(meta_path) as f:
            meta = json.load(f)
        print(f"索引已存在: {meta['station_count']} 个车站, {meta['train_count']} 趟车", file=sys.stderr)
        print(f"上次构建: {meta.get('index_build_time', 'unknown')}", file=sys.stderr)
        return
    
    # 解析
    print("解析 train_list.js ...", file=sys.stderr)
    trains_by_date = parse_train_list(js_path)
    
    # 建索引
    print("构建索引 ...", file=sys.stderr)
    station_index, train_index = build_indexes(trains_by_date)
    
    # 读取现有元数据
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            meta = json.load(f)
    else:
        meta = {}
    
    # 保存
    save_indexes(data_dir, station_index, train_index, meta)
    print(f"完成！共 {len(station_index)} 个车站, {len(train_index)} 趟车", file=sys.stderr)


if __name__ == "__main__":
    main()
