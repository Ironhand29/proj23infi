# proj23infi
PROJETOS 2023 - INFINITY
- Existem 2 projetos atualmente na pasta
- DESAFIO-BIBLIOTECA ( projeto de um gerenciador de livros)
- teste-velha ( projeto de Machine Learning utilizando aprendizagem por reforço). ( EM ANÁLISE)
  (Atualmente em looping para análise de dados.)

DESAFIO-BIBLIOTECA: CHECK LIST DE MELHORIAS A SEREM REALIZADAS [ok](07/11/2023)
- Adicionar 50 livros a biblioteca [ok](07/11/2023)
- Definir biblioteca JSON para que os alugueis, baixas e lista de livros sejam salvos quando o arquivo for fechado. [ok](13/11/2023)
-Modificar a estrutura de dados:
-Criar um novo dicionário chamado biblioteca para rastrear os livros disponíveis na biblioteca.  [ok](13/11/2023)
-Cada livro pode ser representado como um dicionário com informações como título, autor, quantidade disponível, etc. [ok](13/11/2023)
Além disso, crie um dicionário alugueis para rastrear os aluguéis de livros, associando o usuário ao livro alugado e à data de aluguel. [ok](13/11/2023)
Organização e Estrutura:
- Remover a arte ASCII no início do código [ok](13/11/2023)
- Mover a definição das funções para o topo do arquivo, logo após as importações, para tornar o código mais organizado. [ok](13/11/2023)
Tratamento de Exceções:
- Adicionar tratamento de exceções em partes do código que podem gerar erros, como ao ler ou gravar arquivos, para fornecer mensagens de erro mais amigáveis e evitar falhas inesperadas.
Comentários:
- Adicione comentários ao código para explicar o que cada função faz e fornecer informações sobre o propósito de cada bloco de código. [ok](13/11/2023)
Evitar Variáveis Globais:
- Evitar o uso excessivo de variáveis globais, como conta_logada. Em vez disso, passe essas variáveis como argumentos para as funções que as utilizam.
Separação de Responsabilidades:
- Tentar manter as funções com responsabilidades bem definidas. Isso torna o código mais fácil de entender e de depurar.
Validação de Entrada:
- Adicionar validação de entrada para garantir que os dados inseridos pelos usuários sejam válidos e seguros. Isso inclui a validação de senhas, títulos de livros, etc.
Tratamento de Erros:
-Implementar um tratamento mais robusto de erros e mensagens de erro mais informativas, para que o usuário saiba o que deu errado.
Melhorias na Manipulação de Dados:
-Usar estruturas de dados apropriadas para representar os usuários, senhas, alugueis e livros em vez de usar dicionários aninhados.
Utilização de F-strings:
-Usar f-strings para formatar mensagens e saídas, tornando o código mais legível.
Mensagens de Confirmação:
-Adicionar mensagens de confirmação após a execução de ações bem-sucedidas, para fornecer feedback ao usuário.
Refatoração:
- Considerar a refatoração do código em partes complexas, como a lógica de aluguel e devolução de livros, para torná-lo mais legível e mais fácil de manter.
