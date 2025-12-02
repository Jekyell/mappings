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
    json_files = glob.glob(os.path.join(HIGH_PRIORITY_DIR, '*.json'))
    
    print(f"[*] 发现 {len(json_files)} 个高优先级文件，开始解析...")

    for file_path in json_files:
        filename = os.path.basename(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for key, value in data.items():
                if isinstance(value, dict) and value.get(TARGET_LANG):
                    translations[key] = value[TARGET_LANG]

        except (json.JSONDecodeError, UnicodeDecodeError, IOError) as e:
            print(f"[!] 读取或解析文件 {filename} 失败: {e}")
            
    print(f"[✓] 成功加载 {len(translations)} 条高优先级翻译。")
    return translations


def update_low_priority_files(high_priority_translations):
    """
    遍历 F_Replace 文件夹下的 JSON 文件，用高优先级翻译覆盖其中的键值对。
    排除文件：mstClass_name.json
    """
    if not os.path.isdir(LOW_PRIORITY_DIR):
        print(f"[!] 错误: 低优先级目录 '{LOW_PRIORITY_DIR}' 不存在。")
        return

    json_files = glob.glob(os.path.join(LOW_PRIORITY_DIR, '*.json'))
    print(f"\n[*] 发现 {len(json_files)} 个低优先级文件，开始检查和更新...")
    total_updates = 0

    for file_path in json_files:
        filename = os.path.basename(file_path)

        # --- 新增：排除 F_Replace/mstClass_name.json ---
        if filename == "mstClass_name.json":
            print(f"[!] 跳过低优先级文件: {filename}")
            continue

        file_updated = False

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                low_priority_data = json.load(f)

            keys_to_check = list(low_priority_data.keys())
            
            for key in keys_to_check:
                if key in high_priority_translations:
                    high_priority_value = high_priority_translations[key]
                    if low_priority_data.get(key) != high_priority_value:
                        print(f"  -> 在 {filename} 中更新 '{key}': '{low_priority_data.get(key)}' -> '{high_priority_value}'")
                        low_priority_data[key] = high_priority_value
                        file_updated = True
                        total_updates += 1
            
            if file_updated:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(low_priority_data, f, ensure_ascii=False, indent=2)
                print(f"  [✓] 文件 {filename} 已保存。")

        except (json.JSONDecodeError, UnicodeDecodeError, IOError) as e:
            print(f"[!] 处理文件 {filename} 失败: {e}")

    if total_updates == 0:
        print("\n[✓] 所有文件都已是最新，无需更新。")
    else:
        print(f"\n[✓] 更新完成，总共修改了 {total_updates} 个键值对。")


if __name__ == "__main__":
    print("--- 开始自动合并翻译 ---")
    master_translations = load_high_priority_translations()
    update_low_priority_files(master_translations)
    print("--- 任务执行完毕 ---")
