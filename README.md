# Contabilis

Um sistema baseado em Django para gerenciar processos e partes jurídicas, com extração automática de dados de arquivos HTML e elaboração de relatórios.

## Como rodar o projeto

### 🚀 Rodando com Docker (recomendado)

1. **Pré-requisitos:**
   - Docker e Docker Compose instalados
   - (Linux) Certifique-se de que seu usuário está no grupo `docker` para evitar erros de permissão:
     ```bash
     sudo usermod -aG docker $USER
     # Depois, faça logout/login ou reinicie o computador
     ```

2. **Suba o ambiente:**
   ```bash
   docker-compose up --build
   ```
   Isso irá:
   - Construir a imagem
   - Subir o banco de dados
   - Rodar as migrations
   - Popular o banco (usuários, processos, partes)
   - Subir o servidor Django

3. **Acesse o sistema:**
   - Acesse: http://localhost:8000

4. **Parar o ambiente:**
   ```bash
   docker-compose down
   ```

---

### ⚙️ Rodando localmente ( ambient venv)

1. **Crie e ative um ambiente virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure o banco de dados PostgreSQL localmente** (ou use Docker para o banco apenas):
   - Configure as variáveis de ambiente ou o arquivo `.env` conforme necessário.

   **Exemplo de variáveis para o banco**
      ```bash
      export SECRET_KEY="your-secret-key-here"
      export DEBUG=True
      export DB_NAME=legal_processes
      export DB_USER=postgres
      export DB_PASSWORD=postgres
      export DB_HOST=localhost
      export DB_PORT=5432
      ```

4. **Rode as migrations e scripts de popular banco:**
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   python scripts/create_users.py
   python scripts/populate_processes.py
   python scripts/populate_parties.py
   ```

5. **Inicie o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

---

## Dicas
- Se receber erro de permissão ao rodar Docker, adicione seu usuário ao grupo `docker` (veja acima).
- Para acessar o terminal do container web:
  ```bash
  docker exec -it contabilis-web-1 bash
  ```
- Para logs do container:
  ```bash
  docker logs contabilis-web-1
  ```


---
## Rodando os testes

#### Docker
```bash
docker-compose exec web pytest
# ou com cobertura:
docker-compose exec web pytest --cov=processes --cov=parties
```

#### Ambiente virtual (venv)
```bash
source venv/bin/activate
pytest
# ou com cobertura:
pytest --cov=processes --cov=parties
```
---
## Aplicação
<img width="1328" height="986" alt="image" src="https://github.com/user-attachments/assets/4100e6eb-6ea3-41e0-8124-127f98ac80e5" />

https://github.com/user-attachments/assets/76a15b7f-b0a9-40cc-8d42-c92ccccc2799



https://github.com/user-attachments/assets/06dd01ed-7248-461c-9714-6364abfd99ab



## 🔑 Credenciais:
web-1  |    Admin - Usuário: admin, Senha: admin123
web-1  |    Normal - Usuário: usuario, Senha: usuario123





## Contribuição
Caso queria contribuir com alterações sugestões so subir uma PR para ser analisada
