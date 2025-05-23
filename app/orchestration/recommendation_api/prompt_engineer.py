class PromptEngineer:
    
    @staticmethod
    def few_shot(endpoints, user_input):
        """
        Técnica Few-Shot Learning.
        """
        return f"""
        Você é um especialista em entender um solicitação ou comando escrito em linguagem natural e, a partir da análise do conteúdo de documentação de API disponível, você deve encontrar e recomendar endpoints candidatos com capacidade de atender a demanda do usuário.
        Aqui estão alguns EXEMPLOS de como você deve realizar a análise e recomendação:
       
        Demanda do usuário: 'Quais opções de funcionalidades o sistema me fornecesse relacionado a manutenção dos projetos favoritos?'
        Resposta esperada:
        'Após análise da documentação das APIs disponíveis, encontrei algumas opções que podem atender à sua demanda.\n\n'
        'Opção 1 - GET /projects/favorite - Find Favorite Projects\nEste endpoint permite recuperar registros de projetos marcados como favorito.\n\n'
        'Opção 2 - POST /projects/favorite - Remove Favorite Project\nEste endpoint permite adicionar registros de projetos marcados como favorito.\n\n'
        'Opção 3 - DELETE /projects/favorite/project_id - Add Mortem General\nEste endpoint permite remover registros de projetos marcados como favorito.\n\n'
        'Essas são as opções que encontrei. Qual delas melhor atende à sua necessidade?'
        EXEMPLO 2:
        Demanda do usuário: 'Quero adicionar um registro no post-mortem'
        Resposta esperada:
        'Após análise da documentação das APIs disponíveis, encontrei algumas opções que podem atender à sua demanda.\n\n'
        'Opção 1 - /post_mortem/project/mortem_general - Add Mortem General\nEste endpoint permite adicionar um registro no sistema de post-mortem.\n\n'
        'Essas são as opções que encontrei. Qual delas melhor atende à sua necessidade?'
        Com base nos exemplos fornecidos para resolução desta tarefa, analise o seguinte metadata: {endpoints}
        e recomende os endpoints que podem atender à demanda do usuário: {user_input}.
        Siga o mesmo formato dos exemplos acima sem o uso de **
        'Opção 1 - {{path}} - {{description}}\n<Comentário de recomendação>\n\n'
        'Opção 2 - {{path}} - {{description}}\n<Comentário de recomendação>\n\n'.
        """