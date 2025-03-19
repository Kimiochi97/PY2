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
    # Conecta ao banco de dados
    db_path = os.path.join(os.path.dirname(__file__), 'arquivos.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Busca o BLOB correspondente ao nome do arquivo
    cursor.execute('''
        SELECT data FROM segredos WHERE filename = 'segredo.enc'
    ''')
    
    blob_data = cursor.fetchone()
    conn.close()
    
    if not blob_data:
        raise ValueError(f"Arquivo não encontrado no banco de dados")
    
    # Escreve o conteúdo BLOB no arquivo de saída
    with open(output_file_path, 'wb') as file:
        file.write(blob_data[0])
        
def main():
    print('Iniciando busca ao tesouro...')


    # Extrai o arquivo criptografado do banco de dados
    db_to_file('arquivos.db', 'segredo.enc')

    # Lê o arquivo criptografado
    with open('segredo.enc', 'rb') as f:
        dados_cripto = f.read()

    for chave in range(83000000, 850000000):
        if chave % 100000 == 0:
            print(f'Tentando chave: {str(chave).zfill(8)}')  # Print da chave que está sendo tentada
        texto_descriptografado = tentar_descriptografia(dados_cripto, chave)
        if texto_descriptografado:
            #print(f'Dados descriptografados: {texto_descriptografado}')  # Print dos dados descriptografados
            if 'Parabéns' in texto_descriptografado:
                print(f'Chave encontrada: {str(chave).zfill(8)}')
                #print(f'Texto descriptografado: {texto_descriptografado}')
                break
    else:
        print('Nenhuma chave válida encontrada.')

if __name__ == '__main__':
    main()
        
    
    #grupo https://meet.google.com/dnw-emhx-gfm
    # use força bruta para descriptogravar o segredo.enc
    # esse arquivo encontra-se dentro do arquivos.db no formato sqllite
    # a chave é numérica de 8 digitos
    # o texto descriptografado contém a palavra Parabéns

    
    

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