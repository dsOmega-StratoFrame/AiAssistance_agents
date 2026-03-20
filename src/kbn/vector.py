import os
from tqdm import tqdm
from pathlib import Path

import numpy as np
import pandas as pd
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model="qwen3-embedding:4b"
)

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

# for db_collection_name in tqdm(["class1-sub2-chap3", "class2-sub3-chap4"]):
#     documents = []
#     doc_ids = []

#     for doc_index in range(3):
#         cl, sub, chap = db_collection_name.split("-")
#         content = f"This is {db_collection_name}-doc{doc_index}"
#         doc = Document(page_content=content, metadata={"chunk_num": doc_index, "chapter":chap, "class":cl, "subject":sub})
#         documents.append(doc)
#         doc_ids.append(str(doc_index))


#     # # Initialize a Chroma instance with the original document
#     db = Chroma.from_documents(
#          collection_name=db_collection_name,
#          documents=documents, ids=doc_ids,
#          embedding=embeddings, 
#          persist_directory="./data")
#     
#      db.persist()

def read_pizza_df(location: Path) -> pd.DataFrame:
    return pd.read_csv(location)

def init_pizza_vector_store(df: pd.DataFrame, db_path: Path) -> Chroma:
    add_documents = not os.path.exists(db_path)

    if add_documents:
        documents = []
        ids = []
        
        for i, row in df.iterrows():
            document = Document(
                page_content=row["Title"] + " " + row["Review"],
                metadata={"rating": row["Rating"], "date": row["Date"]},
                id=str(i)
            )
            ids.append(str(i))
            documents.append(document)

        # print(documents)
            
    vector_store = Chroma(
        collection_name="restaurant_reviews",
        persist_directory=db_path,
        embedding_function=embeddings
    )

    if add_documents:
        vector_store.add_documents(documents=documents, ids=ids)
        
    return vector_store

def read_taskwarrior_df(location: Path) -> pd.DataFrame:
    return pd.read_json(location)

def init_taskwarrior_vector_store(df: pd.DataFrame, db_path: Path) -> Chroma:
    add_documents = not db_path.exists()

    if add_documents:
        documents = []
        ids = []
        
        for _i, row in tqdm(df.iterrows()):
            metadata = row[[
                "urgency",
                "priority",
                "status",
                "due",
                "wait",
                "start",
                # "end",
                "project",
                "depends",
            ]].dropna()

            row = row.dropna()
            # print(row)
            page_content = row.get("logseqtitle") or row["description"]

            if (isinstance(row.get("tags"), list) and len(row.get("tags"))):
                tags = " ".join(map(lambda t: "#" + t, row.get("tags")))
                # print(page_content)
                # print(tags)
                page_content += f" {tags}"

            if (isinstance(row.get("annotations"), list) and len(row["annotations"])):
                anotations_body = "\n".join([
                     f"{ann["entry"]}: {ann["description"]}" for ann in row.get("annotations")
                ])
                page_content += "\n" + anotations_body

            id = str(row["uuid"])

            document = Document(
                page_content=page_content,
                metadata=metadata.to_dict(),
                id=id
            )
            ids.append(id)
            documents.append(document)

            
    vector_store = Chroma(
        collection_name="taskwarrior",
        persist_directory=db_path,
        embedding_function=embeddings
    )

    if add_documents:
        vector_store.add_documents(documents=documents, ids=ids)
        
    return vector_store

retriever = init_taskwarrior_vector_store(df=read_taskwarrior_df(taskwarrior_raw_data_path), db_path=taskwarrior_db_path).as_retriever(
    search_kwargs={"k": 10}
)
