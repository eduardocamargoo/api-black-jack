# Jogo do 21 (Blackjack) - API FastAPI

API desenvolvida em FastAPI que implementa um jogo de 21 (Blackjack) onde o jogador compete contra uma máquina.

## Regras do Jogo

**Objetivo:** Chegar o mais próximo possível de 21 pontos sem ultrapassar.

**Regras da Máquina:**
- A máquina continua a pedir cartas até atingir pelo menos 17 pontos
- Para automaticamente quando atinge entre 17 e 21 pontos
- Se ultrapassar 21, a máquina estoura e perde
- Se a máquina tiver uma pontuação maior que o jogador (sem estourar), ela vence

**Regras do Jogador:**
- Recebe 2 cartas iniciais
- Pode pedir mais cartas ou parar
- Se ultrapassar 21, estoura e perde imediatamente
- Se parar, a máquina joga automaticamente

**Valores das Cartas:**
- Cartas de 2 a 10: valor nominal
- Figuras (J, Q, K): valem 10
- Ás: vale 1 ou 11 (o que for mais vantajoso)

## Instalação

```bash
pip3 install -r requirements.txt
```

## Executar a API

```bash
python3 main.py
```

A API estará disponível em `http://localhost:8000`

## Endpoints Disponíveis

### 1. Raiz - Informações da API
```
GET /
```

### 2. Iniciar Novo Jogo
```
POST /novo-jogo
```

**Resposta:**
```json
{
  "cartas_jogador": [7, 10],
  "cartas_maquina": [5],
  "pontuacao_jogador": 17,
  "pontuacao_maquina": 5,
  "jogo_ativo": true,
  "mensagem": "Novo jogo iniciado! Suas cartas foram distribuídas.",
  "vencedor": null
}
```

### 3. Pedir Carta
```
POST /pedir-carta
```

**Resposta:**
```json
{
  "cartas_jogador": [7, 10, 3],
  "cartas_maquina": [5],
  "pontuacao_jogador": 20,
  "pontuacao_maquina": 5,
  "jogo_ativo": true,
  "mensagem": "Jogo em andamento. Escolha: pedir carta ou parar.",
  "vencedor": null
}
```

### 4. Parar (Máquina Joga)
```
POST /parar
```

**Resposta:**
```json
{
  "cartas_jogador": [7, 10],
  "cartas_maquina": [5, 10, 3],
  "pontuacao_jogador": 17,
  "pontuacao_maquina": 18,
  "jogo_ativo": false,
  "mensagem": "A máquina venceu com 18 contra 17.",
  "vencedor": "maquina"
}
```

### 5. Consultar Estado Atual
```
GET /estado
```

## Exemplo de Uso com cURL

```bash
# Iniciar novo jogo
curl -X POST http://localhost:8000/novo-jogo

# Pedir uma carta
curl -X POST http://localhost:8000/pedir-carta

# Parar (máquina joga)
curl -X POST http://localhost:8000/parar

# Consultar estado
curl http://localhost:8000/estado
```

## Documentação Interativa

Após iniciar a API, acesse:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Estrutura do Projeto

```
jogo_21/
├── main.py              # Código principal da API
├── requirements.txt     # Dependências do projeto
└── README.md           # Este arquivo
```

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido para construção de APIs
- **Pydantic**: Validação de dados e serialização
- **Uvicorn**: Servidor ASGI de alta performance
