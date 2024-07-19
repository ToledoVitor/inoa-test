
  # Monitor de Ativos B3 📝
  Esse projeto é parte de um teste técnico feito para uma vaga de desenvolvedor Backend Python.
  O projeto consiste em criar um sistema que seja capaz de monitorar preços de ativos listados
  na B3, salvando os preços em um dado intervalo de tempo.
  

  ## Dependências 🚀 
  Todas as dependências do projeto são gerenciadas usando [Poetry](https://python-poetry.org/).
  Antes de rodar o projeto, você precisará ter instalado o Poetry e o 
  [Python na versão 3.12](https://www.python.org/downloads/release/python-3120/) ou superior.

  Com o poetry instalado, rode no seu terminal:

  ~~~bash  
    poetry install
  ~~~

  Isso já irá instalar todas as dependências e criar uma virtual env para o projeto.

  ## Rodando o Projeto 🔥  
  Antes de Começar, você primeiro precisa criar o banco e rodar as migrações.
  ~~~bash  
    python manage.py migrate
  ~~~

  Com o banco criado e as migrações feitas, para rodar o projeto você precisará de 3 coisas.
  
  ### 1. Subir o Django
  ~~~bash  
    python manage.py runserver
  ~~~

  ### 2. Subir o Celery
  ~~~bash  
    celery -A core worker --loglevel=info -P gevent --concurrency 1 -E
  ~~~

  ### 3. Subir o Celery Beat
  ~~~bash  
    celery -A core beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler --max-interval 10
  ~~~
  

  ## Criando Buscas e Monitorando Ativos ✔

  Com o projeto rodando, você pode acessar http://localhost:8000/ e verá um tela inicial
  do Django Rest mostrando as urls disponíveis.
  
  Para criar um novo modelo de busca acesse http://localhost:8000/buscas/ e configure os
  campos de túnel de preço, intervalo de busca e ativos monitorados.

  Ao criar uma nova busca, um schedule é criado e uma task é executada no celery com o
  intervalo passado. O sistema irá consultar a API e salvar os preços daqueles ativos
  para o túnel de preço selecionado.

  Para ver todos os preços de ativos salvos, acesse http://localhost:8000/precos/.
  

  ## Considerações ✨  
  Como dito anteriormente, esse projeto faz parte de um teste técnico, com o intuito
  de avaliar o conhecimento técnico e boas práticas de um desenvolvedor. O projeto
  foi feito em 3 dias e possui espaço para muitas melhorias.

  ### Frontend
  Na entrevista foi especificado que o Frontend não era algo tão relevante para esse
  escopo. Com isso, seguimos o desenvolvimento com o html gerado pelo própio DJango Rest,
  uma vez que o mesmo oferece maior velocidade no desenvolvimento, além de ter todas as
  funcionalidades necessárias.

  ### API B3
  A API para obter os dados foi uma grande limitação encontrada no desenvolvimento do projeto.
  A API escolhida foi a da [brapi](https://brapi.dev/docs/acoes/available), que foi a que
  ofereceu a maior quantidade de informações, e possui a opção de plano gratuito.

  > [!NOTE]
  > Para usarmos a api precisamos de um token, para que não seja necessário o usuário crie um, deixei salvo o meu token de teste. Em breve irei remove-lo.

  Ainda sim, existem algumas limitações pela utilização do plano gratuito. Como por exemplo:
  
  * Ativos que podem ser monitorados (a lista
  completa de ativos disponibilizada pela empresa está no arquivo avaliable-stocks.txt)
  * Quantidade de ativos por requisição, limitada por 1 ativo, o que obriga a serem feitas
  várias requisições ao invés de uma.
  * Quantidade de requisições por mês, limitada a 15.000 requisições

  Apesar de todos esses problemas, essa api foi a mais completa que encontrei. Existia também
  uma segunda opção de criarmos um web crawler, que buscasse online os preços e os salvasse,
  mas essa opção foi descartada.
  