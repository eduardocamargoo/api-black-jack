from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import random
from enum import Enum
app = FastAPI(title="Jogo do 21 (Blackjack)", version="1.0")
origins = [
    "http://localhost",
    "http://localho st:8080", # Porta do servidor do frontend
    "http://127.0.0.1:8080",
    "https://8080-iqeltrslac0acdqmt372t-4acffe3c.manus.computer" # URL pública do frontend
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permitir todas as origens para simplificar no sandbox
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class AcaoJogador(str, Enum):
    PEDIR = "pedir"
    PARAR = "parar"
class EstadoJogo(BaseModel):
    cartas_jogador: List[int]
    cartas_maquina: List[int]
    pontuacao_jogador: int
    pontuacao_maquina: int
    jogo_ativo: bool
    mensagem: str
    vencedor: Optional[str] = None
class Baralho:
    """Representa um baralho de cartas para o jogo do 21"""
    
    def __init__(self):
        # Cartas de 1 a 11 (Ás pode ser 1 ou 11, figuras valem 10)
        self.cartas = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4
        random.shuffle(self.cartas)
    
    def pegar_carta(self) -> int:
        """Retira uma carta do baralho"""
        if not self.cartas:
            self.cartas = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4
            random.shuffle(self.cartas)
        return self.cartas.pop()
class JogoBlackjack:
    """Lógica principal do jogo do 21"""
    
    def __init__(self):
        self.baralho = Baralho()
        self.cartas_jogador: List[int] = []
        self.cartas_maquina: List[int] = []
        self.jogo_ativo = True
    
    def calcular_pontuacao(self, cartas: List[int]) -> int:
        """Calcula a pontuação considerando Ás como 1 ou 11"""
        pontuacao = sum(cartas)
        ases = cartas.count(1)
        
        # Tenta usar Ás como 11 se não estourar
        while ases > 0 and pontuacao + 10 <= 21:
            pontuacao += 10
            ases -= 1
        
        return pontuacao
    
    def iniciar_jogo(self):
        """Inicia um novo jogo distribuindo 2 cartas para cada"""
        self.cartas_jogador = [self.baralho.pegar_carta(), self.baralho.pegar_carta()]
        self.cartas_maquina = [self.baralho.pegar_carta()]
        self.jogo_ativo = True
    
    def jogador_pedir_carta(self):
        """Jogador pede uma nova carta"""
        if not self.jogo_ativo:
            raise HTTPException(status_code=400, detail="O jogo já terminou")
        
        self.cartas_jogador.append(self.baralho.pegar_carta())
        
        pontuacao = self.calcular_pontuacao(self.cartas_jogador)
        if pontuacao > 21:
            self.jogo_ativo = False
            return self._finalizar_jogo()
        
        return self._obter_estado()
    
    def jogador_parar(self):
        """Jogador para e a máquina joga"""
        if not self.jogo_ativo:
            raise HTTPException(status_code=400, detail="O jogo já terminou")
        
        # Máquina joga seguindo as regras: para entre 17-21
        while self.calcular_pontuacao(self.cartas_maquina) < 17:
            self.cartas_maquina.append(self.baralho.pegar_carta())
        
        self.jogo_ativo = False
        return self._finalizar_jogo()
    
    def _finalizar_jogo(self) -> EstadoJogo:
        """Determina o vencedor e retorna o estado final"""
        pontuacao_jogador = self.calcular_pontuacao(self.cartas_jogador)
        pontuacao_maquina = self.calcular_pontuacao(self.cartas_maquina)
        
        # Determina o vencedor
        if pontuacao_jogador > 21:
            vencedor = "maquina"
            mensagem = f"Você estourou com {pontuacao_jogador}! A máquina venceu."
        elif pontuacao_maquina > 21:
            vencedor = "jogador"
            mensagem = f"A máquina estourou com {pontuacao_maquina}! Você venceu."
        elif pontuacao_maquina > pontuacao_jogador:
            vencedor = "maquina"
            mensagem = f"A máquina venceu com {pontuacao_maquina} contra {pontuacao_jogador}."
        elif pontuacao_jogador > pontuacao_maquina:
            vencedor = "jogador"
            mensagem = f"Você venceu com {pontuacao_jogador} contra {pontuacao_maquina}!"
        else:
            vencedor = "empate"
            mensagem = f"Empate! Ambos com {pontuacao_jogador}."
        
        return EstadoJogo(
            cartas_jogador=self.cartas_jogador,
            cartas_maquina=self.cartas_maquina,
            pontuacao_jogador=pontuacao_jogador,
            pontuacao_maquina=pontuacao_maquina,
            jogo_ativo=False,
            mensagem=mensagem,
            vencedor=vencedor
        )
    
    def _obter_estado(self) -> EstadoJogo:
        """Retorna o estado atual do jogo"""
        pontuacao_jogador = self.calcular_pontuacao(self.cartas_jogador)
        pontuacao_maquina = self.calcular_pontuacao(self.cartas_maquina)
        
        return EstadoJogo(
            cartas_jogador=self.cartas_jogador,
            cartas_maquina=self.cartas_maquina,
            pontuacao_jogador=pontuacao_jogador,
            pontuacao_maquina=pontuacao_maquina,
            jogo_ativo=self.jogo_ativo,
            mensagem="Jogo em andamento. Escolha: pedir carta ou parar."
        )
jogo_atual = JogoBlackjack()
@app.get("/")
def raiz():
    """Endpoint raiz com informações da API"""
    return {
        "mensagem": "Bem-vindo ao Jogo do 21 (Blackjack)!",
        "endpoints": {
            "/novo-jogo": "POST - Inicia um novo jogo",
            "/pedir-carta": "POST - Jogador pede uma carta",
            "/parar": "POST - Jogador para e a máquina joga",
            "/estado": "GET - Consulta o estado atual do jogo"
        }
    }
@app.post("/novo-jogo", response_model=EstadoJogo)
def novo_jogo():
    """Inicia um novo jogo do 21"""
    global jogo_atual
    jogo_atual = JogoBlackjack()
    jogo_atual.iniciar_jogo()
    
    estado = jogo_atual._obter_estado()
    estado.mensagem = "Novo jogo iniciado! Suas cartas foram distribuídas."
    return estado
@app.post("/pedir-carta", response_model=EstadoJogo)
def pedir_carta():
    """Jogador pede uma nova carta"""
    return jogo_atual.jogador_pedir_carta()
@app.post("/parar", response_model=EstadoJogo)
def parar():
    """Jogador para e a máquina joga automaticamente"""
    return jogo_atual.jogador_parar()
@app.get("/estado", response_model=EstadoJogo)
def obter_estado():
    """Retorna o estado atual do jogo"""
    return jogo_atual._obter_estado()
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
