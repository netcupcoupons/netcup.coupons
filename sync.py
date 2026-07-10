import urllib.request
import json
import time

API_URL = "https://netcup.coupons/?api=1"

# 优惠券类型归类映射
CATEGORY_MAPPING = {
    "discount": "General Discounts",
    "rs": "Root Servers",
    "vps": "VPS (Virtual Private Servers)",
    "hosting": "Web Hosting"
}

def fetch_coupons():
    try:
        req = urllib.request.Request(
            API_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)
    except Exception as e:
        print(f"Error fetching data from API: {e}")
        return None

def build_readme(data):
    if not data or "coupons" not in data:
        print("Invalid data received.")
        return
        
    last_updated_display = data.get("last_sync_display", time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()))
    coupons = data["coupons"]
    
    # 格式化分组
    grouped = {cat: [] for cat in CATEGORY_MAPPING.keys()}
    for item in coupons:
        cat = item.get("category")
        if cat in grouped:
            grouped[cat].append(item)
            
    # 构建 Markdown 格式的 README
    md = []
    md.append("# Netcup Voucher Codes\n")
    md.append("> 🏷️ A curated collection of Netcup voucher codes. Checked automatically and synchronized in real-time.\n")
    md.append(f"⏰ **Last Updated:** `{last_updated_display}`\n")
    md.append("## Available Vouchers\n")
    
    for cat_key, cat_name in CATEGORY_MAPPING.items():
        items = grouped[cat_key]
        if not any(item.get("codes") for item in items):
            continue
            
        md.append(f"### {cat_name}\n")
        
        for item in items:
            codes = item.get("codes", [])
            if not codes:
                continue
                
            title = item.get("title", "")
            desc = item.get("desc", "").upper()
            
            md.append(f"- **{title}** ({desc})\n")
            for code in codes:
                md.append(f"  - `{code}`\n")
                
        md.append("") # 类别间距
        
    md.append("---\n")
    md.append("*(This README is updated automatically every 5 minutes using GitHub Actions. Vouchers are single-use only, so use them quickly!)*\n")
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print("README.md updated successfully!")

if __name__ == "__main__":
    coupon_data = fetch_coupons()
    if coupon_data:
        build_readme(coupon_data)
