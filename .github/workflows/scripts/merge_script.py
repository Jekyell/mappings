import os
import json
import glob

# --- 配置 ---
# 高优先级文件所在目录 (仓库根目录)
HIGH_PRIORITY_DIR = '.' 
# 低优先级文件所在目录，这些文件将被修改
LOW_PRIORITY_DIR = 'F_Replace'
# 目标语言键
TARGET_LANG = 'CN'
# --- 配置结束 ---

def load_high_priority_translations():
    """
    加载根目录下所有 JSON 文件，并提取有效的 CN 翻译。
    返回一个字典: {"原文": "翻译"}
    """
    translations = {}
    # 查找根目录下的所有 .json 文件
    json_files = glob.glob(os.path.join(HIGH_PRIORITY_DIR, '*.json'))
    
    print(f"[*] 发现 {len(json_files)} 个高优先级文件，开始解析...")

    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for key, value in data.items():
                # 检查格式是否为 {"CN": "..."} 并且 CN 值不为空
                if isinstance(value, dict) and value.get(TARGET_LANG):
                    translations[key] = value[TARGET_LANG]
        except (json.JSONDecodeError, UnicodeDecodeError, IOError) as e:
            print(f"[!] 读取或解析文件 {os.path.basename(file_path)}失败: {e}")
            
    print(f"[✓] 成功加载 {len(translations)} 条高优先级翻译。")
    return translations

def update_low_priority_files(high_priority_translations):
    """
    遍历 F_Replace 文件夹下的 JSON 文件，用高优先级翻译覆盖其中的键值对。
    """
    if not os.path.isdir(LOW_PRIORITY_DIR):
        print(f"[!] 错误: 低优先级目录 '{LOW_PRIORITY_DIR}' 不存在。")
        return

    json_files = glob.glob(os.path.join(LOW_PRIORITY_DIR, '*.json'))
    print(f"\n[*] 发现 {len(json_files)} 个低优先级文件，开始检查和更新...")
    total_updates = 0

    for file_path in json_files:
        file_updated = False
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                low_priority_data = json.load(f)

            # 创建一个副本用于迭代，以避免在迭代时修改字典
            keys_to_check = list(low_priority_data.keys())
            
            for key in keys_to_check:
                # 如果这个 key 在高优先级翻译中存在
                if key in high_priority_translations:
                    high_priority_value = high_priority_translations[key]
                    # 只有当值不同时才更新，避免不必要的写入和提交
                    if low_priority_data.get(key) != high_priority_value:
                        print(f"  -> 在 {os.path.basename(file_path)} 中更新 '{key}': '{low_priority_data.get(key)}' -> '{high_priority_value}'")
                        low_priority_data[key] = high_priority_value
                        file_updated = True
                        total_updates += 1
            
            # 如果文件内容有变动，则写回文件
            if file_updated:
                with open(file_path, 'w', encoding='utf-8') as f:
                    # ensure_ascii=False 确保中文字符正常显示
                    # indent=2 格式化输出，方便查看 diff
                    json.dump(low_priority_data, f, ensure_ascii=False, indent=2)
                print(f"  [✓] 文件 {os.path.basename(file_path)} 已保存。")

        except (json.JSONDecodeError, UnicodeDecodeError, IOError) as e:
            print(f"[!] 处理文件 {os.path.basename(file_path)} 失败: {e}")

    if total_updates == 0:
        print("\n[✓] 所有文件都已是最新，无需更新。")
    else:
        print(f"\n[✓] 更新完成，总共修改了 {total_updates} 个键值对。")


if __name__ == "__main__":
    print("--- 开始自动合并翻译 ---")
    # 1. 加载所有高优先级翻译到内存
    master_translations = load_high_priority_translations()
    # 2. 更新低优先级文件
    update_low_priority_files(master_translations)
    print("--- 任务执行完毕 ---")
