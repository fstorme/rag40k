import json
import os.path

from llama_hub.file.unstructured import UnstructuredReader
from llama_index.node_parser import SentenceSplitter
from llama_index import Document, VectorStoreIndex, ServiceContext
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.llms import HuggingFaceLLM, LlamaCPP
from llama_index.postprocessor import LongContextReorder
import logging
logger = logging.getLogger('rag')
logger.setLevel(logging.DEBUG)


class RetrieverAssistedGenerator:
    def __init__(self, chunk_size=200, chunk_overlap=20,
                 embedding_model="../../../models/allminilm",
                 llm_model="../../../models/llms/zephyr-7b-beta.Q3_K_S.gguf"):
        self.loader = UnstructuredReader()
        self.parser = SentenceSplitter(chunk_size=chunk_size,
                                       chunk_overlap=chunk_overlap)
        hf = HuggingFaceEmbedding(model_name=embedding_model)
        llm = LlamaCPP(model_path=llm_model)
        self.service_context = ServiceContext.from_defaults(embed_model=hf, llm=llm)
        self.index = []
        self.query_engine = []


    def create_index(self, pdf_file):
        logger.info("Loading document")
        document = self.loader.load_data(pdf_file)
        nodes = self.parser.get_nodes_from_documents(document)
        logger.info("Creating index")
        self.index = VectorStoreIndex(nodes, service_context=self.service_context)
        return self.index

    def create_query_engine(self, streaming=False, node_postprocessors=[LongContextReorder]):
        if isinstance(self.index, list):
            raise Exception("Vector Index must be initialized before the query engine")
        return self.index.as_query_engine(node_postprocessors=node_postprocessors, streaming=streaming)

    def persist(self, persist_path):
        assert os.path.isdir(persist_path)
        self.index.storage_context.persist(os.path.join(persist_path, "index"))
        with open(os.path.join(persist_path, "service_context.json"), 'w') as f:
            json.dump(self.service_context.to_dict(), f)
        with open(os.path.join(persist_path, "parser.json"), "w") as f:
            json.dump(self.parser.to_dict(), f)

    @staticmethod
    def from_dir(persist_path):
        #TODO add a loading from directory
        return []
