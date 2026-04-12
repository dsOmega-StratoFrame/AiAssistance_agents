from pathlib import Path

data_dir = Path("data")

raw_data_dir = data_dir / "raw"
processed_data_dir = data_dir / "processed"

kbn_raw_data_dir = raw_data_dir / "kbn-"
kbn_processed_data_dir = processed_data_dir / "kbn-"

pizza_raw_data_path = raw_data_dir / "realistic_restaurant_reviews.csv"
taskwarrior_raw_data_path = kbn_raw_data_dir / "taskwarrior.json"

chroma_db_dir = processed_data_dir / "chrome_langchain_db"
kbn_chroma_db_dir = kbn_processed_data_dir / "chrome_langchain_db"

pizza_db_path = chroma_db_dir / "pizzas"
taskwarrior_db_path = kbn_chroma_db_dir / "taskwarrior"
zotero_db_path = kbn_chroma_db_dir / "zotero"
