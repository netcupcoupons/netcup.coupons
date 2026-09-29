import urllib.request
import json
import time

API_URL = "https://netcup.coupons/?api=1"

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

def write_english_readme(data, last_updated_display, grouped):
    md = []
    # Language Switcher
    md.append("🌐 **Select Language:** English | [简体中文](README_ZH.md) | [Deutsch](README_DE.md)\n")
    
    md.append("# Netcup Voucher Codes")
    md.append("> 🏷️ A curated collection of Netcup voucher codes. Checked automatically and synchronized in real-time.\n")
    md.append(f"⏰ **Last Updated:** `{last_updated_display}`\n")
    
    # Redemption Links
    md.append("## How to Redeem")
    md.append("- 🚀 **Direct One-Click Redemption:** Click any voucher code below to open the Netcup shopping cart with the coupon code automatically pre-applied!")
    md.append("- 🇩🇪 **German Cart URL:** [https://www.netcup.com/de/checkout/warenkorb](https://www.netcup.com/de/checkout/warenkorb)")
    md.append("- 🇬🇧 **English / International Cart URL:** [https://www.netcup.com/en/checkout/cart](https://www.netcup.com/en/checkout/cart)")
    md.append("- 🌐 **Live Fallback Website:** If all codes listed below are invalid, visit [netcup.coupons](https://netcup.coupons) directly to fetch fresh codes.\n")
    
    # Available Coupons
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
            title = item.get("title") or ""
            desc = (item.get("desc") or "").upper()
            if item.get("tag") == "rs4" or "RS 4000" in title:
                desc = "5 EUR OFF"
            md.append(f"- **{title}** ({desc})")
            for code in codes:
                link = f"https://www.netcup.com/en/checkout/cart?gutschein={code}"
                md.append(f"  - [`{code}`]({link})")
        md.append("")
        
    # Technical Specifications Table
    md.append("## Technical Specifications")
    md.append("### Root Servers G12.5")
    md.append("| Plan | CPU | vCores | RAM | Storage | Traffic | Price (excl. VAT) |")
    md.append("| --- | --- | --- | --- | --- | --- | --- |")
    md.append("| RS 500 G12.5 | AMD EPYC 9645 | 2 Dedicated | 4 GB DDR5 ECC | 64 GB NVMe | Flatrate | 10.86 €/mo |")
    md.append("| RS 1000 G12.5 | AMD EPYC 9645 | 4 Dedicated | 8 GB DDR5 ECC | 128 GB NVMe | Flatrate | 18.26 €/mo |")
    md.append("| RS 2000 G12.5 | AMD EPYC 9645 | 8 Dedicated | 16 GB DDR5 ECC | 256 GB NVMe | Flatrate | 34.20 €/mo |")
    md.append("| RS 4000 G12.5 | AMD EPYC 9645 | 12 Dedicated | 32 GB DDR5 ECC | 512 GB NVMe | Flatrate | 65.40 €/mo |")
    md.append("| RS 8000 G12.5 | AMD EPYC 9645 | 16 Dedicated | 64 GB DDR5 ECC | 1 TB NVMe | Flatrate | 124.72 €/mo |\n")

    md.append("### VPS G12.5")
    md.append("| Plan | vCores | RAM | Storage | Traffic | Price (excl. VAT) |")
    md.append("| --- | --- | --- | --- | --- | --- |")
    md.append("| VPS 500 G12.5 | 2 vCores | 4 GB RAM | 64 GB SSD | Flatrate | 6.94 €/mo |")
    md.append("| VPS 1000 G12.5 | 4 vCores | 8 GB RAM | 128 GB SSD | Flatrate | 12.18 €/mo |")
    md.append("| VPS 2000 G12.5 | 8 vCores | 16 GB RAM | 256 GB SSD | Flatrate | 22.62 €/mo |")
    md.append("| VPS 4000 G12.5 | 12 vCores | 32 GB RAM | 512 GB SSD | Flatrate | 38.11 €/mo |")
    md.append("| VPS 8000 G12.5 | 16 vCores | 64 GB RAM | 1 TB SSD | Flatrate | 56.39 €/mo |\n")

    # Guide & Redemption Walkthrough
    md.append("## Redeeming Walkthrough")
    md.append("### Option A: Direct One-Click Redemption (Fastest)")
    md.append("1. **Click any voucher code above:** It will open Netcup checkout directly with the coupon automatically applied to your cart.")
    md.append("2. **Add products to cart:** Pick your server or hosting product to see the discount deducted immediately.")
    md.append("3. **Complete checkout:** Proceed to finalize your order with the discounted total.")
    md.append("\n### Option B: Manual Voucher Code Entry")
    md.append("1. **Go to your cart:** Navigate to the Netcup checkout page ([English Cart](https://www.netcup.com/en/checkout/cart) or [German Cart](https://www.netcup.com/de/checkout/warenkorb)).")
    md.append("2. **Enter the code:** Locate the \"Redeem voucher\" section at the bottom, and paste your copied coupon code into the input field.")
    md.append("3. **Apply discount:** Click the Redeem button. The corresponding plan discount will be immediately calculated and applied.")
    md.append("4. **Complete checkout:** Review the updated price summary and click Continue to finish your purchase.\n")

    # Frequently Asked Questions
    md.append("## Frequently Asked Questions")
    md.append("#### Q1: How do I redeem a Netcup voucher?")
    md.append("A1: Click directly on your desired coupon code above to open the Netcup checkout with the voucher pre-applied, or copy the code and enter it manually during checkout.")
    md.append("#### Q2: Are the vouchers free?")
    md.append("A2: Yes. Generating, clicking, and using the vouchers is completely free for you.")
    md.append("#### Q3: Are the codes checked before listing?")
    md.append("A3: Every code is verified automatically by our backend API. We check the status against Netcup's systems every 5 minutes.")
    md.append("#### Q4: Can vouchers be combined with each other?")
    md.append("A4: No. Netcup vouchers cannot be stacked, so it's always just one code per order.")
    md.append("#### Q5: Do the codes work for existing customers too?")
    md.append("A5: Yes. Our voucher codes for web hosting, VPS, and root servers work for existing Netcup customers just as well as for new ones. (Only the general €5 new customer voucher is restricted to first-time orders).")
    md.append("#### Q6: What is the G12.5 generation at Netcup?")
    md.append("A6: G12.5 is Netcup's latest server hardware generation running on modern AMD EPYC 9645 (Zen 5 Turin) CPUs with DDR5 ECC RAM and NVMe SSDs in RAID 10.\n")

    # Contact & Details
    md.append("## Netcup Contact Details")
    md.append("- **Address:** Daimlerstraße 25, D-76185 Karlsruhe")
    md.append("- **Phone:** 0721 7540755 - 0")
    md.append("- **Hotline:** 08000 638 287 (Toll-free in Germany)")
    md.append("- **Email:** mail@netcup.de")
    md.append("- **Official Channels:** [Netcup on X (Twitter)](https://x.com/netcup) | [Facebook Page](https://www.facebook.com/netcup)\n")
    
    md.append("---\n")
    md.append("*(This README is updated automatically upon coupon changes. Vouchers are single-use only, so use them quickly!)*\n")
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md))

def write_chinese_readme(data, last_updated_display, grouped):
    md = []
    # Language Switcher
    md.append("🌐 **选择语言:** [English](README.md) | 简体中文 | [Deutsch](README_DE.md)\n")
    
    md.append("# Netcup 优惠码与折扣券")
    md.append("> 🏷️ 精选 Netcup 优惠券代码合集。自动检查检测并实时同步更新。\n")
    md.append(f"⏰ **最后更新:** `{last_updated_display}`\n")
    
    # Redemption Links
    md.append("## 优惠码使用方式")
    md.append("- 🚀 **一键直达兑换：** 直接点击下方任意优惠码链接，即可自动跳转至 Netcup 购物车并预填兑换该优惠券！")
    md.append("- 🇩🇪 **德语购物车直达链接:** [https://www.netcup.com/de/checkout/warenkorb](https://www.netcup.com/de/checkout/warenkorb)")
    md.append("- 🇬🇧 **英语/国际购物车链接:** [https://www.netcup.com/en/checkout/cart](https://www.netcup.com/en/checkout/cart)")
    md.append("- 🌐 **实时备用网站:** 如果下方列出的所有代码均失效，请直接访问 [netcup.coupons](https://netcup.coupons) 获取最新的有效优惠码。\n")
    
    # Available Coupons
    md.append("## 当前可用优惠码\n")
    for cat_key, cat_name in CATEGORY_MAPPING.items():
        items = grouped[cat_key]
        if not any(item.get("codes") for item in items):
            continue
        zh_cat_name = "通用优惠券"
        if cat_key == "rs": zh_cat_name = "Root 专用服务器 (RS)"
        elif cat_key == "vps": zh_cat_name = "VPS 虚拟服务器 (VPS)"
        elif cat_key == "hosting": zh_cat_name = "Web 虚拟主机 (Hosting)"
        
        md.append(f"### {zh_cat_name}\n")
        for item in items:
            codes = item.get("codes", [])
            if not codes:
                continue
            title = item.get("title") or ""
            desc = (item.get("desc") or "").upper()
            if item.get("tag") == "rs4" or "RS 4000" in title:
                desc = "5 EUR OFF"
            
            title_translated = title.replace("Free", "免费").replace("Month", "个月").replace("OFF", "立减")
            desc_translated = (
                desc.replace("FREE FOR", "免费体验")
                .replace("MONTHS", "个月")
                .replace("MONTH", "个月")
                .replace("5 EUR OFF", "立减 5 欧元")
                .replace("OFF", "立减")
                .replace("MINIMUM CONTRACT PERIOD APPLIES", "仅适用于新用户首个订单")
                .replace("NEW CUSTOMERS ONLY", "仅限新客户")
            )
            
            md.append(f"- **{title_translated}** ({desc_translated})")
            for code in codes:
                link = f"https://www.netcup.com/en/checkout/cart?gutschein={code}"
                md.append(f"  - [`{code}`]({link})")
        md.append("")
        
    # Technical Specifications Table
    md.append("## 技术参数对照表")
    md.append("### Root 服务器 G12.5")
    md.append("| 方案名称 | CPU 型号 | 核心数 (vCores) | 内存大小 (RAM) | 硬盘容量 (Storage) | 流量限制 | 价格 (不含税) |")
    md.append("| --- | --- | --- | --- | --- | --- | --- |")
    md.append("| RS 500 G12.5 | AMD EPYC 9645 | 2 独占物理核心 | 4 GB DDR5 ECC | 64 GB NVMe | 无限流量 | 10.86 €/月 |")
    md.append("| RS 1000 G12.5 | AMD EPYC 9645 | 4 独占物理核心 | 8 GB DDR5 ECC | 128 GB NVMe | 无限流量 | 18.26 €/月 |")
    md.append("| RS 2000 G12.5 | AMD EPYC 9645 | 8 独占物理核心 | 16 GB DDR5 ECC | 256 GB NVMe | 无限流量 | 34.20 €/月 |")
    md.append("| RS 4000 G12.5 | AMD EPYC 9645 | 12 独占物理核心 | 32 GB DDR5 ECC | 512 GB NVMe | 无限流量 | 65.40 €/月 |")
    md.append("| RS 8000 G12.5 | AMD EPYC 9645 | 16 独占物理核心 | 64 GB DDR5 ECC | 1 TB NVMe | 无限流量 | 124.72 €/月 |\n")

    md.append("### VPS 虚拟服务器 G12.5")
    md.append("| 方案名称 | 核心数 (vCores) | 内存大小 (RAM) | 硬盘容量 (Storage) | 流量限制 | 价格 (不含税) |")
    md.append("| --- | --- | --- | --- | --- | --- |")
    md.append("| VPS 500 G12.5 | 2 vCores | 4 GB RAM | 64 GB SSD | 无限流量 | 6.94 €/月 |")
    md.append("| VPS 1000 G12.5 | 4 vCores | 8 GB RAM | 128 GB SSD | 无限流量 | 12.18 €/月 |")
    md.append("| VPS 2000 G12.5 | 8 vCores | 16 GB RAM | 256 GB SSD | 无限流量 | 22.62 €/月 |")
    md.append("| VPS 4000 G12.5 | 12 vCores | 32 GB RAM | 512 GB SSD | 无限流量 | 38.11 €/月 |")
    md.append("| VPS 8000 G12.5 | 16 vCores | 64 GB RAM | 1 TB SSD | 无限流量 | 56.39 €/月 |\n")

    # Guide & Redemption Walkthrough
    md.append("## 优惠券兑换步骤")
    md.append("### 选项 A：一键点击直接兑换（最快捷）")
    md.append("1. **点击上方任意优惠码：** 即可直接打开 Netcup 购物车，系统会自动为您应用该优惠码。")
    md.append("2. **添加所选产品：** 将需要的服务器或虚拟主机加入购物车，折扣立即可见。")
    md.append("3. **结账下单：** 确认金额无误后完成支付即可。")
    md.append("\n### 选项 B：手动在购物车输入优惠码")
    md.append("1. **进入购物车：** 直接访问 Netcup 购物车页面（[英文购物车](https://netcup.com/en/checkout/cart) 或 [德语购物车](https://www.netcup.com/de/checkout/warenkorb)）。")
    md.append("2. **输入优惠码：** 滚动至购物车底部，找到 \"Redeem voucher (兑换优惠码)\" 输入框，粘贴复制好的优惠码。")
    md.append("3. **应用折扣：** 点击右侧 Redeem (兑换) 按钮。相应的折扣金额会立即计算并显示在您的总账单中。")
    md.append("4. **结账：** 核对折扣后金额无误后，点击 Continue 继续完成支付即可。\n")

    # Frequently Asked Questions
    md.append("## 常见问题解答 (FAQ)")
    md.append("#### Q1: 如何使用 Netcup 优惠券？")
    md.append("A1: 直接点击上方的优惠券代码链接即可一键跳转并预填使用，或者手动复制并在 Netcup 购物车结算页面输入使用。")
    md.append("#### Q2: 获取这些优惠券是免费的吗？")
    md.append("A2: 是的。生成、复制和使用这些优惠码对您来说完全是免费的。")
    md.append("#### Q3: 优惠码展示前是否进行核验？")
    md.append("A3: 所有优惠券均由我们网站的脚本自动核验。我们每 5 分钟与 Netcup 接口对齐检测一次。")
    md.append("#### Q4: 多张优惠券可以叠加使用吗？")
    md.append("A4: 不可以。Netcup 的优惠码不能叠加，每个订单只能使用一个优惠码。")
    md.append("#### Q5: 现有老用户可以使用这些优惠码吗？")
    md.append("A5: 可以的。我们的 RS、VPS 和虚拟主机优惠码老用户与新用户均能使用。唯一的例外是 5 欧元的通用新客券（仅限首单新用户）。")
    md.append("#### Q6: Netcup G12.5 世代有什么优势？")
    md.append("A6: G12.5 是 Netcup 采用 AMD EPYC 9645（Zen 5 Turin 架构）处理器、DDR5 ECC 内存和企业级 NVMe RAID 10 阵列的最新一代服务器硬件。\n")

    # Contact & Details
    md.append("## Netcup 官方联系信息")
    md.append("- **地址:** Daimlerstraße 25, D-76185 Karlsruhe, Germany")
    md.append("- **电话:** 0721 7540755 - 0")
    md.append("- **客服热线:** 08000 638 287 (德国境内免费)")
    md.append("- **电子邮件:** mail@netcup.de")
    md.append("- **官方社媒:** [X/Twitter 官方号](https://x.com/netcup) | [Facebook 主页](https://www.facebook.com/netcup)\n")
    
    md.append("---\n")
    md.append("*(本 README 在优惠券有变动时会自动运行更新。优惠码为一次性使用，请尽快兑换！)*\n")
    
    with open("README_ZH.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md))

def write_german_readme(data, last_updated_display, grouped):
    md = []
    # Language Switcher
    md.append("🌐 **Sprache auswählen:** [English](README.md) | [简体中文](README_ZH.md) | Deutsch\n")
    
    md.append("# Netcup Gutscheine & Rabattcodes")
    md.append("> 🏷️ Eine kuratierte Liste von aktiven Netcup Gutscheincodes. Automatisch geprüft und in Echtzeit aktualisiert.\n")
    md.append(f"⏰ **Zuletzt aktualisiert:** `{last_updated_display}`\n")
    
    # Redemption Links
    md.append("## Gutschein einlösen")
    md.append("- 🚀 **Direkte Einlösung per Klick:** Klicken Sie einfach auf einen Gutscheincode unten, um den Netcup-Warenkorb direkt mit aktiviertem Gutscheincode aufzurufen!")
    md.append("- 🇩🇪 **Deutscher Warenkorb Link:** [https://www.netcup.com/de/checkout/warenkorb](https://www.netcup.com/de/checkout/warenkorb)")
    md.append("- 🇬🇧 **Englischer / Internationaler Warenkorb Link:** [https://www.netcup.com/en/checkout/cart](https://www.netcup.com/en/checkout/cart)")
    md.append("- 🌐 **Live-Backup-Website:** Falls alle unten aufgeführten Codes ungültig sind, besuchen Sie direkt [netcup.coupons](https://netcup.coupons) für frische Codes.\n")
    
    # Available Vouchers
    md.append("## Verfügbare Gutscheine\n")
    for cat_key, cat_name in CATEGORY_MAPPING.items():
        items = grouped[cat_key]
        if not any(item.get("codes") for item in items):
            continue
        de_cat_name = "Allgemeine Rabatte"
        if cat_key == "rs": de_cat_name = "Root Server (RS)"
        elif cat_key == "vps": de_cat_name = "Virtual Server (VPS)"
        elif cat_key == "hosting": de_cat_name = "Webhosting"
        
        md.append(f"### {de_cat_name}\n")
        for item in items:
            codes = item.get("codes", [])
            if not codes:
                continue
            title = item.get("title") or ""
            desc = (item.get("desc") or "").upper()
            
            title_translated = title.replace("Free", "Kostenlos").replace("Month", "Monat").replace("Monate", "Monate").replace("OFF", "Rabatt")
            desc_translated = (
                desc.replace("FREE FOR", "KOSTENLOS FÜR")
                .replace("MONTHS", "MONATE")
                .replace("MONTH", "MONAT")
                .replace("5 EUR OFF", "5,00 € RABATT")
                .replace("OFF", "RABATT")
                .replace("MINIMUM CONTRACT PERIOD APPLIES", "Nur für Neukunden bei der ersten Bestellung")
                .replace("NEW CUSTOMERS ONLY", "NUR FÜR NEUKUNDEN")
            )
            
            md.append(f"- **{title_translated}** ({desc_translated})")
            for code in codes:
                # German specific redemption link
                link = f"https://www.netcup.com/de/checkout/warenkorb?gutschein={code}"
                md.append(f"  - [`{code}`]({link})")
        md.append("")
        
    # Technical Specifications Table
    md.append("## Technische Spezifikationen")
    md.append("### Root Server G12.5")
    md.append("| Tarif | Prozessor | Kerne | Arbeitsspeicher | Speicherplatz | Traffic | Preis (zzgl. MwSt.) |")
    md.append("| --- | --- | --- | --- | --- | --- | --- |")
    md.append("| RS 500 G12.5 | AMD EPYC 9645 | 2 dediziert | 4 GB DDR5 ECC | 64 GB NVMe | Flatrate | 10,86 €/Monat |")
    md.append("| RS 1000 G12.5 | AMD EPYC 9645 | 4 dediziert | 8 GB DDR5 ECC | 128 GB NVMe | Flatrate | 18,26 €/Monat |")
    md.append("| RS 2000 G12.5 | AMD EPYC 9645 | 8 dediziert | 16 GB DDR5 ECC | 256 GB NVMe | Flatrate | 34,20 €/Monat |")
    md.append("| RS 4000 G12.5 | AMD EPYC 9645 | 12 dediziert | 32 GB DDR5 ECC | 512 GB NVMe | Flatrate | 65,40 €/Monat |")
    md.append("| RS 8000 G12.5 | AMD EPYC 9645 | 16 dediziert | 64 GB DDR5 ECC | 1 TB NVMe | Flatrate | 124,72 €/Monat |\n")

    md.append("### VPS G12.5")
    md.append("| Tarif | Kerne | Arbeitsspeicher | Speicherplatz | Traffic | Preis (zzgl. MwSt.) |")
    md.append("| --- | --- | --- | --- | --- | --- |")
    md.append("| VPS 500 G12.5 | 2 vCores | 4 GB RAM | 64 GB SSD | Flatrate | 6,94 €/Monat |")
    md.append("| VPS 1000 G12.5 | 4 vCores | 8 GB RAM | 128 GB SSD | Flatrate | 12,18 €/Monat |")
    md.append("| VPS 2000 G12.5 | 8 vCores | 16 GB RAM | 256 GB SSD | Flatrate | 22,62 €/Monat |")
    md.append("| VPS 4000 G12.5 | 12 vCores | 32 GB RAM | 512 GB SSD | Flatrate | 38,11 €/Monat |")
    md.append("| VPS 8000 G12.5 | 16 vCores | 64 GB RAM | 1 TB SSD | Flatrate | 56,39 €/Monat |\n")

    # Guide & Redemption Walkthrough
    md.append("## Anleitung zum Einlösen")
    md.append("### Option A: Ein-Klick-Direkteinlösung (am schnellsten)")
    md.append("1. **Gutscheincode anklicken:** Klicken Sie einfach auf einen beliebigen Gutscheincode oben. Der Netcup-Warenkorb wird direkt mit dem eingelösten Gutschein geöffnet.")
    md.append("2. **Produkt auswählen:** Legen Sie den gewünschten Server- oder Webhosting-Tarif in den Warenkorb – der Rabatt wird sofort angewendet.")
    md.append("3. **Bestellung abschließen:** Überprüfen Sie den reduzierten Preis und schließen Sie die Bestellung ab.")
    md.append("\n### Option B: Manuelle Eingabe im Warenkorb")
    md.append("1. **Warenkorb aufrufen:** Navigieren Sie direkt zur Netcup Warenkorbseite ([Deutscher Warenkorb](https://www.netcup.com/de/checkout/warenkorb) oder [Englischer Warenkorb](https://www.netcup.com/en/checkout/cart)).")
    md.append("2. **Code eingeben:** Suchen Sie unten das Feld \"Gutschein einlösen\" und fügen Sie Ihren kopierten Gutscheincode ein.")
    md.append("3. **Rabatt anwenden:** Klicken Sie auf Einlösen. Der Rabatt wird sofort berechnet und vom Gesamtbetrag abgezogen.")
    md.append("4. **Bestellung abschließen:** Überprüfen Sie den Preis und klicken Sie auf Weiter, um den Kauf abzuschließen.\n")

    # Frequently Asked Questions
    md.append("## Häufig gestellte Fragen (FAQs)")
    md.append("#### Q1: Wie löse ich einen Netcup-Gutschein ein?")
    md.append("A1: Klicken Sie direkt auf den gewünschten Gutscheincode oben, um ihn direkt im Warenkorb vorzumerken, oder kopieren Sie ihn und geben ihn manuell im Warenkorb ein.")
    md.append("#### Q2: Sind die Gutscheine kostenlos?")
    md.append("A2: Ja. Die Generierung und Nutzung der Rabattcodes ist für Sie vollkommen gratis.")
    md.append("#### Q3: Werden die Gutscheincodes regelmäßig überprüft?")
    md.append("A3: Jeder Code wird automatisch durch unsere Skripte geprüft. Wir gleichen den Status alle 5 Minuten mit Netcup ab.")
    md.append("#### Q4: Können Gutscheine miteinander kombiniert werden?")
    md.append("A4: Nein. Pro Bestellung kann bei Netcup immer nur ein einziger Gutscheincode eingelöst werden.")
    md.append("#### Q5: Gelten die Rabatte auch für bestehende Kunden?")
    md.append("A5: Ja. Unsere Gutscheincodes für Webhosting, VPS und Root-Server können sowohl von Neukunden als auch von Bestandskunden genutzt werden. Einzige Ausnahme ist der 5 € Neukundengutschein.")
    md.append("#### Q6: Was zeichnet die Netcup G12.5 Generation aus?")
    md.append("A6: G12.5 steht für Netcups neueste Server-Hardwaregeneration auf Basis moderner AMD EPYC 9645 (Zen 5 Turin) Prozessoren mit DDR5 ECC RAM und Enterprise NVMe SSDs im RAID 10.\n")

    # Contact & Details
    md.append("## Netcup Kontaktinformationen")
    md.append("- **Adresse:** Daimlerstraße 25, D-76185 Karlsruhe")
    md.append("- **Telefon:** 0721 7540755 - 0")
    md.append("- **Hotline:** 08000 638 287 (Kostenfrei in Deutschland)")
    md.append("- **E-Mail:** mail@netcup.de")
    md.append("- **Offizielle Kanäle:** [Netcup auf X (Twitter)](https://x.com/netcup) | [Facebook-Seite](https://www.facebook.com/netcup)\n")
    
    md.append("---\n")
    md.append("*(Dieses README wird bei Gutscheinänderungen automatisch aktualisiert. Gutscheine sind nur einmalig nutzbar!)*\n")
    
    with open("README_DE.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md))

def build_readme(data):
    if not data or "coupons" not in data:
        print("Invalid data received.")
        return
        
    last_updated_display = data.get("last_sync_display", time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()))
    coupons = data["coupons"]
    
    # Group coupons by category
    grouped = {cat: [] for cat in CATEGORY_MAPPING.keys()}
    for item in coupons:
        cat = item.get("category")
        if cat in grouped:
            grouped[cat].append(item)
            
    # Write the three localized README documents
    write_english_readme(data, last_updated_display, grouped)
    write_chinese_readme(data, last_updated_display, grouped)
    write_german_readme(data, last_updated_display, grouped)
    print("All multi-language READMEs updated successfully!")

if __name__ == "__main__":
    coupon_data = fetch_coupons()
    if coupon_data:
        build_readme(coupon_data)