from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfutils
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os

# 日本語フォントの設定
def setup_japanese_fonts():
    """日本語フォントを設定する"""
    try:
        # Windows標準の日本語フォントを使用
        if os.name == 'nt':  # Windows
            # メイリオフォントを使用
            pdfmetrics.registerFont(TTFont('Japanese', 'C:/Windows/Fonts/meiryo.ttc'))
            pdfmetrics.registerFont(TTFont('Japanese-Bold', 'C:/Windows/Fonts/meiryob.ttc'))
        else:  # Linux/Mac
            # Noto Sansフォントを使用（システムにインストールされている場合）
            try:
                pdfmetrics.registerFont(TTFont('Japanese', '/System/Library/Fonts/Hiragino Sans GB.ttc'))
                pdfmetrics.registerFont(TTFont('Japanese-Bold', '/System/Library/Fonts/Hiragino Sans GB.ttc'))
            except:
                # フォールバック
                pdfmetrics.registerFont(TTFont('Japanese', 'HeiseiKakuGo-W5'))
                pdfmetrics.registerFont(TTFont('Japanese-Bold', 'HeiseiKakuGo-W5'))
        return True
    except Exception as e:
        print(f"日本語フォントの設定に失敗しました: {e}")
        return False

# カラーパレット
COLORS = {
    'primary': HexColor('#2563eb'),      # 青
    'secondary': HexColor('#64748b'),    # グレー
    'accent': HexColor('#f59e0b'),       # オレンジ
    'background': HexColor('#f8fafc'),   # ライトグレー
    'text': HexColor('#1e293b'),         # ダークグレー
    'light_blue': HexColor('#dbeafe'),   # ライトブルー
}

# JSONから読み取ったと想定
words = [
    {'word': '銀行', 'hiragana': 'ぎんこう', 'rome': 'ginkou', 'synonyms': '金融機関, 銀行業', 'antonym': '', 'example': '私は毎月、銀行に貯金しています。', 'example2': '銀行で口座を開設しました。', 'example_rome': 'Watashi wa maitsuki, ginkou ni chokin shiteimasu.', 'example_rome2': 'Ginkou de kouza o kaisetsu shimashita.'},
    {'word': '会社', 'hiragana': 'かいしゃ', 'rome': 'kaisha', 'synonyms': '企業、会社組織', 'antonym': '個人事業', 'example': '田中さんは毎日会社に行きます。', 'example_rome': 'Tanaka-san wa mainichi kaisha ni ikimasu.', 'example2': '来月、新しい会社を設立します。', 'example_rome2': 'Raigetsu, atarashii kaisha o setsuritsu shimasu.'},
]

def draw_header(c, width, height, page_num=1):
    """ページヘッダーを描画"""
    # ヘッダー背景
    c.setFillColor(COLORS['primary'])
    c.rect(0, height - 60, width, 60, fill=1, stroke=0)
    
    # タイトル
    c.setFillColor(white)
    c.setFont("Japanese-Bold", 20)
    c.drawString(50, height - 40, "Japanese Words Learning Sheet")
    
    # ページ番号
    c.setFont("Japanese", 12)
    c.drawRightString(width - 50, height - 40, f"Page {page_num}")

def draw_word_list_item(c, word_data, x, y, item_width, item_height):
    """単語リストアイテムを描画"""
    # 背景なし、枠線なし
    
    # 単語（日本語）- 大きく太文字
    c.setFillColor(COLORS['text'])
    c.setFont("Japanese-Bold", 18)
    c.drawString(x, y + item_height - 30, word_data['word'])
    
    # ひらがなとローマ字を並べて表示（キー名なし、値のみ）
    c.setFillColor(COLORS['primary'])
    c.setFont("Japanese", 12)
    c.drawString(x, y + item_height - 55, word_data['hiragana'])
    
    c.setFont("Helvetica", 12)
    c.drawString(x + 200, y + item_height - 55, word_data['rome'])
    
    # 類義語・反意語（もしあれば）
    c.setFillColor(COLORS['secondary'])
    c.setFont("Japanese", 10)
    if word_data.get('synonyms'):
        c.drawString(x, y + item_height - 75, f"類義語: {word_data['synonyms']}")
    if word_data.get('antonym'):
        c.drawString(x + 250, y + item_height - 75, f"反意語: {word_data['antonym']}")
    
    # 例文（キー名なし、値のみ）
    c.setFillColor(COLORS['text'])
    c.setFont("Japanese", 11)
    
    # 1つ目の例文
    example_text = word_data['example']
    max_chars_per_line = 60
    if len(example_text) > max_chars_per_line:
        # 日本語の場合、文字数で分割
        lines = []
        current_line = ""
        
        for char in example_text:
            if len(current_line + char) <= max_chars_per_line:
                current_line += char
            else:
                lines.append(current_line)
                current_line = char
        lines.append(current_line)
        
        for i, line in enumerate(lines):
            c.drawString(x, y + item_height - 95 - (i * 15), line)
    else:
        c.drawString(x, y + item_height - 95, example_text)
    
    # 2つ目の例文（もしあれば）
    if word_data.get('example2'):
        c.setFont("Japanese", 11)
        example2_text = word_data['example2']
        y_offset = 15 if len(example_text) <= max_chars_per_line else 30
        c.drawString(x, y + item_height - 95 - y_offset, example2_text)

def create_pdf():
    """PDFを作成"""
    # 日本語フォントの設定
    has_japanese_font = setup_japanese_fonts()
    if not has_japanese_font:
        print("警告: 日本語フォントが設定できませんでした。代替フォントを使用します。")
    
    c = canvas.Canvas("words.pdf", pagesize=A4)
    width, height = A4
    
    # 1ページあたりのアイテム数とレイアウト
    items_per_page = 6  # 情報量が増えたので1ページのアイテム数を減らす
    
    item_width = width - 100
    item_height = 100  # 高さを増やして情報を収める
    margin_x = 50
    margin_y = 80
    
    page_num = 1
    
    for i, word_data in enumerate(words):
        # ページの開始時にヘッダーを描画
        if i % items_per_page == 0:
            if i > 0:  # 最初のページでない場合は改ページ
                c.showPage()
                page_num += 1
            draw_header(c, width, height, page_num)
        
        # アイテムの位置を計算
        item_index_on_page = i % items_per_page
        
        x = margin_x
        y = height - margin_y - 80 - ((item_index_on_page + 1) * (item_height + 10))
        
        # リストアイテムを描画
        draw_word_list_item(c, word_data, x, y, item_width, item_height)
    
    # フッター情報
    c.setFillColor(COLORS['secondary'])
    c.setFont("Japanese", 8)
    c.drawString(50, 30, "Generated by JP Teacher AI - English Learning System")
    
    c.save()

if __name__ == "__main__":
    create_pdf()
    print("📚 洗練されたPDFが生成完了しました！")
