import os

# 你的字典配置
ANTI_HARMONY_DICT = { 
    "匕见": "荆轲", "虎狼": "吕布", "周照": "武则天", "莲偶": "哪吒", "重瞳": "项羽",
    "忠贞": "秦良玉", "祖政": "始皇帝", "雏罂": "虞美人", "丹驹": "赤兔马", "晋帝": "司马懿",
    "琰女": "杨贵妃", "瞑生院": "杀生院", "歌果": "美杜莎", "爱迪·萨奇": "爱德华·蒂奇",
    "雾都弃子": "开膛手杰克", "西行者": "玄奘三藏", "方巿": "徐福", "吾绰": "呼延灼",
    "暗匿者": "暗杀者", "【{0}】": "[{0}]"
}

def scan_and_replace():
    has_changes = False
    # 遍历当前目录下所有文件
    for root, dirs, files in os.walk("."):
        # 排除 .git 目录
        if ".git" in dirs:
            dirs.remove(".git")
        
        for file in files:
            # 只处理 .json 文件
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = content
                    for key, value in ANTI_HARMONY_DICT.items():
                        if key in new_content:
                            new_content = new_content.replace(key, value)
                    
                    if content != new_content:
                        print(f"🔄 正在修改文件: {file_path}")
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        has_changes = True
                except Exception as e:
                    print(f"❌ 读取文件出错 {file_path}: {e}")

    return has_changes

if __name__ == "__main__":
    if scan_and_replace():
        print("DETECT_CHANGE=true")
    else:
        print("DETECT_CHANGE=false")
