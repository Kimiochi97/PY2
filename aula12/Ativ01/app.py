import sqlite3
import os

# Função para criptografar um arquivo usando operação XOR com chave numérica de 8 dígitos.
def criptografar_arquivo(arquivo_entrada, arquivo_saida, chave):
    """
    Criptografa um arquivo usando operação XOR com chave numérica de 8 dígitos.
    A chave será convertida para bytes e repetida ciclicamente durante o XOR.
    """
    with open(arquivo_entrada, 'rb') as f:
        dados = f.read()
    
    # Converte a chave para string com zeros à esquerda e transforma em bytes
    chave_bytes = str(chave).zfill(8).encode()  # Agora usando 8 dígitos
    
    # Aplica operação XOR usando a chave estendida
    dados_cripto = xor_bytes(dados, chave_bytes)
    
    with open(arquivo_saida, 'wb') as f:
        f.write(dados_cripto)

def xor_bytes(dados, chave):
    """
    Aplica XOR entre cada byte dos dados e a chave repetida.
    Mesma função para criptografar e descriptografar.
    """
    return bytes([dado ^ chave[i % len(chave)] for i, dado in enumerate(dados)])

def tentar_descriptografia(dados_cripto, chave_tentativa):
    """
    Tenta descriptografar com uma chave de 8 dígitos.
    Retorna None se a decodificação UTF-8 falhar (chave inválida)
    """
    try:
        chave_bytes = str(chave_tentativa).zfill(8).encode()  # 8 dígitos
        dados_decripto = xor_bytes(dados_cripto, chave_bytes)
        return dados_decripto.decode('utf-8')
    except UnicodeDecodeError:
        return None

def db_to_file(db_path, output_file_path):
    """
    Extrai um arquivo do banco de dados SQLite e salva no sistema de arquivos.
    """
    # Conecta ao banco de dados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Busca o BLOB correspondente ao nome do arquivo
    cursor.execute("SELECT data FROM segredos WHERE filename='segredo.enc'")
    
    blob_data = cursor.fetchone()
    conn.close()
    
    if not blob_data:
        raise ValueError("Arquivo não encontrado no banco de dados.")
    
    # Escreve o conteúdo BLOB no arquivo de saída
    with open(output_file_path, 'wb') as file:
        file.write(blob_data[0])

def forca_bruta(dados_cripto):
    """
    Testa todas as chaves numéricas de 8 dígitos (00000000 a 99999999)
    e exibe cada chave testada.
    """
    for chave_tentativa in range(80_000_000, 85_000_001): 
        if chave_tentativa % 100000 == 0:  # Mostra a senha a cada 100 mil tentativas
            print(f"Tentando chave: {chave_tentativa:08d}")
        
        resultado = tentar_descriptografia(dados_cripto, chave_tentativa)
        if resultado and "Parabéns" in resultado:
            print(f"\n🔥 Chave encontrada: {chave_tentativa:08d} 🔥")
            print(f"Mensagem descriptografada: {resultado}")
            return chave_tentativa  # Retorna a chave encontrada

    print("\nNenhuma chave válida encontrada.")
    return None

    print("\nNenhuma chave válida encontrada.")
    return None

def main():
    print("🔎 Iniciando busca ao tesouro...\n")
    
    # Extrai o arquivo do banco de dados
    db_to_file("arquivos.db", "segredo.enc")
    
    # Lê os dados criptografados do arquivo extraído
    with open("segredo.enc", "rb") as f:
        dados_cripto = f.read()

    # Inicia o ataque de força bruta para descobrir a chave
    chave_encontrada = forca_bruta(dados_cripto)

    if chave_encontrada:
        print("\n✅ Desafio concluído com sucesso!")
    else:
        print("\n❌ Não foi possível encontrar a chave.")

if __name__ == '__main__':
    main()

"""
PRINCIPAIS ALTERAÇÕES E DESAFIOS:
1. A chave agora tem 8 dígitos (100 milhões de combinações possíveis)
2. Aumento exponencial na complexidade do brute force
3. Necessidade de otimização e trabalho em equipe eficiente

ESTRATÉGIAS SUGERIDAS:
1. Divisão de tarefas:
   - Dividir o intervalo 0-99999999 entre os membros do grupo
   - Ex: Cada membro testa 12.500.000 chaves (100M / 8 pessoas)

"""