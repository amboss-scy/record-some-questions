# Create vector embeddings fom markdown documents in folder "articles"
def embed_md_documents():
    from langchain.document_loaders import DirectoryLoader
    from langchain.document_loaders import UnstructuredMarkdownLoader
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.vectorstores import Chroma
    import os
    import shutil

    absolute_path = os.path.dirname(os.path.abspath(__file__))
    articles_path = os.path.join(absolute_path, "../articles")
    database_path = os.path.join(absolute_path, "../database")

    if not os.path.exists(articles_path) or not any(
        fname.endswith(".md")
        for fname in os.listdir(articles_path)
        if os.path.isfile(os.path.join(articles_path, fname))
    ):
        print("No content to embed yet. Record article(s) first.")
        return

    print("Rewriting embeddings database ...")

    # Load and process markdown documents
    loader = DirectoryLoader(
        f"{absolute_path}/../articles",
        glob="./*.md",
        loader_cls=UnstructuredMarkdownLoader,
    )
    documents = loader.load()

    # Split the documents into text chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    # Embed and store the text chunks
    if not os.path.exists(database_path):
        os.makedirs(database_path)

    for fname in os.listdir(database_path):
        file_path = os.path.join(database_path, fname)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(
                f"Failed to reset database. {file_path} could not be deleted.\nReason: {e}\nConsider deleting folder database manually."
            )

    embedding = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(
        documents=texts, embedding=embedding, persist_directory=database_path
    )
    vectordb.persist()
    vectordb = None
