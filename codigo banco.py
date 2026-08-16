from datetime import datetime
from zoneinfo import ZoneInfo

menu = """

[1] criar usuário
[2] criar conta
[3] listar usuários
[4] Depositar
[5] Sacar
[6] Extrato
[7] Transferir 
[0] Sair



=> """

def main():
    limite = 1500
    LIMITE_SAQUES = 3
    usuarios = []
    contas = []
    


    while True:
        opcao = input(menu)
        if opcao == "1":

            usuarios = criar_usuario(usuarios)

        elif opcao == "2":
           
           usuarios, contas = criar_conta(usuarios, contas)

        elif opcao == "3":

            listar_usuarios(usuarios)

        elif opcao == "4":

            conta = encontrar_conta(contas)
            if conta is not None:
                conta = depositar(conta)

        elif opcao == "5":

            conta = encontrar_conta(contas)
            if conta is not None:
                conta = sacar(conta, limite, LIMITE_SAQUES)

        elif opcao == "6":
                
                conta = encontrar_conta(contas)

                if conta is not None:
                    exibir_extrato(conta)

        elif opcao == "7":

                    transferir(contas)

        elif opcao == "0":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
        
    
def depositar(conta):

    valor = float(input("Informe o valor do depósito: "))

    if valor > 0:
        conta["saldo"] += valor
        horario =  horario_atual()
        conta["extrato"] += f"Depósito: R$ {valor:.2f} - {horario.strftime('%d/%m/%Y %H:%M:%S')}\n"
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return conta
     

def sacar(conta, limite, LIMITE_SAQUES):

       
    valor = float(input("Informe o valor do saque: "))

    excedeu_saldo = valor > conta["saldo"]
    excedeu_limite = valor > limite
    excedeu_saques = conta["numero_saques"] >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação falhou! Saldo insuficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        conta["saldo"] -= valor
        horario = horario_atual()
        conta["extrato"] += f"Saque: R$ {valor:.2f} - {horario.strftime('%d/%m/%Y %H:%M:%S')}\n"
        conta["numero_saques"] += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return conta
  

def exibir_extrato(conta):

        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not conta["extrato"] else conta["extrato"])
        print(f"\nSaldo: R$ {conta['saldo']:.2f}")
        print("==========================================")


def criar_usuario(usuarios):
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    cpf = (input("Informe o CPF (somente números): ").replace(".", "").replace("-", ""))
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("Já existe usuário com esse CPF!")
            return 

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("Usuário criado com sucesso!")

    return usuarios


def listar_usuarios(usuarios):
    cpf = input("Informe o CPF do usuário para listar: ").replace(".", "").replace("-", "")

    usuario_encontrado = None

    for usuario in usuarios: 
        if usuario["cpf"] == cpf:
            usuario_encontrado = usuario
            
            print("\n=== Usuário ===")
            print(f"Nome: {usuario['nome']}")
            print(f"CPF: {usuario['cpf']}")
            print(f"Data de Nascimento: {usuario['data_nascimento']}")
            print(f"Endereço: {usuario['endereco']}")
            print("================")
            return

    if usuario_encontrado is None:
        print("Usuário não encontrado!")
        return


def criar_conta(usuarios, contas):
    cpf = input("Informe o CPF do usuário: ").replace(".", "").replace("-", "")

    usuario_encontrado = None 
    contador = 0

    for usuario in usuarios:
        if usuario["cpf"] == cpf: 
            usuario_encontrado = usuario
            for conta in contas:
                    if conta["usuario"]["cpf"] == cpf:
                        contador += 1
            contas.append({
                "agencia": "0001",
                "numero": contador + 1,
                "usuario": usuario_encontrado,
                "saldo": 0, "extrato": "",
                "numero_saques": 0
             })
            print("Conta criada com sucesso!")
            return usuarios, contas

    if usuario_encontrado is None:
           print("Usuário não encontrado!")
           return usuarios, contas     


def encontrar_conta(contas):
    cpf = input("Informe o seu CPF: ").replace(".", "").replace("-", "")
    numero_conta = int(input("informe o numero da conta: "))
 
    for conta in contas:
        if conta["usuario"]["cpf"] == cpf and conta["numero"] == numero_conta:
            return conta

    print("Conta nao encontrada.")
    return None

    
def transferir(contas):

  conta_origem = encontrar_conta(contas)
  conta_destino = encontrar_conta(contas)
  

  if conta_origem is not None and conta_destino is not None:

    if conta_origem["usuario"]["cpf"] == conta_destino["usuario"]["cpf"] and conta_origem["numero"] == conta_destino["numero"]:
            print("Operaçao falhou! A conta de origem e destino são iguais.")
            return
  
    valor = float(input("Informe o valor da transferencia: "))

    excedeu_saldo = valor > conta_origem["saldo"]

    if excedeu_saldo:
        print("Saldo da conta insuficiente.")
    elif valor > 0:
        conta_origem["saldo"]  -= valor
        conta_destino["saldo"] += valor
        horario = horario_atual()
        conta_origem["extrato"] += f"transferencia para {conta_destino['usuario']['nome']}: R$ {valor:.2f} - {horario.strftime('%d/%m/%Y %H:%M:%S')}\n"
        conta_destino["extrato"] += f"transferencia recebida de {conta_origem['usuario']['nome']}: R$ {valor:.2f} - {horario.strftime('%d/%m/%Y %H:%M:%S')}\n"
        print(f"Tranferencia de R$ {valor:.2f} realizado com sucesso!")
    else:
        print(f"Operacao falhou! valor informado é invalido.")

def horario_atual():

    return datetime.now(ZoneInfo("America/Sao_Paulo"))
       
main()
