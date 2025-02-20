import weaviate
from weaviate.connect import ConnectionParams

# Kết nối với Weaviate (chạy local)
client = weaviate.WeaviateClient(
    connection_params=ConnectionParams.from_url("http://localhost:8080")
)

# Kiểm tra kết nối
if client.is_ready():
    print("✅ Kết nối Weaviate thành công!")
else:
    print("❌ Không thể kết nối đến Weaviate. Kiểm tra lại server.")
    exit(1)

# Tạo collection (thay thế schema)
class_name = "Article"

if class_name not in client.collections.list_all():
    client.collections.create(
        name=class_name,
        description="A collection of articles",
        vectorizer="none",
        properties=[
            {"name": "title", "data_type": "text", "description": "Tiêu đề"},
            {"name": "content", "data_type": "text", "description": "Nội dung"}
        ]
    )
    print(f"✅ Collection '{class_name}' đã được tạo thành công!")
else:
    print(f"ℹ️ Collection '{class_name}' đã tồn tại.")

# Chèn dữ liệu vào Weaviate
data_object = {"title": "Weaviate là gì?", "content": "Weaviate là một vector database sử dụng AI để tìm kiếm thông tin."}
collection = client.collections.get(class_name)
collection.data.insert(properties=data_object)
print("✅ Dữ liệu đã được chèn vào Weaviate!")

# Truy vấn dữ liệu từ Weaviate
query_result = collection.query.fetch_objects()
print("📌 Dữ liệu truy vấn được:", query_result)

# Đóng kết nối
client.close()
