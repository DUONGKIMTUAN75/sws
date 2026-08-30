import os
import json
from datetime import datetime
from google import genai

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = """
Hãy tự nghĩ một chủ đề thiết thực, hữu ích về cuộc sống, thủ tục hoặc kinh nghiệm tại Nhật Bản.
Hãy trả về kết quả DUY NHẤT dưới định dạng JSON chuẩn (không có markdown bọc ngoài nếu có thể, hoặc chuẩn cấu trúc JSON), gồm các trường:
{
  "title": "Tiêu đề bài viết",
  "summary": "Tóm tắt ngắn gọn nội dung khoảng 2-3 dòng",
  "content": "Nội dung chi tiết bài viết, có thể dùng thẻ HTML cơ bản như <p>, <ul>, <li>"
}
"""

response = client.models.generate_content(
    model='gemini-3.5-flash',
    contents=prompt,
)

try:
    raw_text = response.text.strip()
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:-3].strip()
    elif raw_text.startswith("```"):
        raw_text = raw_text[3:-3].strip()

    new_post = json.loads(raw_text)
    new_post["date"] = datetime.now().strftime("%Y-%m-%d")

    file_path = "news.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            news_list = json.load(f)
    else:
        news_list = []

    news_list.insert(0, new_post)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(news_list, f, ensure_ascii=False, indent=4)
    print("Đã tạo và cập nhật bài viết thành công!")
except Exception as e:
    print(f"Lỗi: {e}")
