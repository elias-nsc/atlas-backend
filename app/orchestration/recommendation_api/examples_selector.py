from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors.semantic_similarity import SemanticSimilarityExampleSelector, MaxMarginalRelevanceExampleSelector

class ExamplesSelector:
    def __init__(self, base_url: str, embed_model_name: str, examples: list, k: int,  mmr=False):
        """
        Inicializa a classe `ExamplesSelector` que seleciona exemplos semânticos ou com MMR (Max Marginal Relevance)
        para uma consulta dada.

        :param base_url: A URL de conexão ao serviço Ollama.
        :type base_url: str
        :param embed_model_name: O nome do modelo de embeddings usado pela classe `OllamaEmbeddings`.
        :type embed_model_name: str
        :param examples: Lista inicial de exemplos para o vectorstore FAISS.
        :type examples: list
        :param k: Número de exemplos a serem retornados quando uma consulta é realizada.
        :type k: int
        :param mmr: Indica se deve usar MMR (Max Marginal Relevance) ao invés da similaridade semântica.
                     O padrão é False, ou seja, usa similaridade semântica.
        :type mmr: bool
        """
        self.examples = examples
        self.embed_model_name = embed_model_name
        self.k = k
        self.ollama_emb = OllamaEmbeddings(model=embed_model_name, base_url=base_url)
        self.mmr = mmr
        if self.mmr:
            self.example_selector = MaxMarginalRelevanceExampleSelector.from_examples(
                examples=self.examples,
                embeddings=self.ollama_emb,
                vectorstore_cls=FAISS,
                k=self.k,
                input_keys=["input"],
            )
        else:
            self.example_selector = SemanticSimilarityExampleSelector.from_examples(
                examples=self.examples,
                embeddings=self.ollama_emb,
                vectorstore_cls=FAISS,
                k=self.k,
                input_keys=["input"],
            )

    def select_examples(self, input_text: str):
        """
        Seleciona exemplos semânticamente similares ou com MMR para a entrada fornecida.

        :param input_text: A consulta ou texto de entrada.
        :type input_text: str
        :return: Uma lista de dicionários contendo os exemplos selecionados.
        :rtype: list
        """
        # Create a dictionary with the input text as required by the selector
        query_dict = {"input": input_text}
        
        # Use the example_selector to find semantically similar examples
        selected_examples = self.example_selector.select_examples(query_dict)
        
        return selected_examples