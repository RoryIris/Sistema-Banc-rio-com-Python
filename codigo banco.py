from datetime import datetime
from zoneinfo import ZoneInfo
import time 

menu = """

[1] Criar usuário
[2] Criar conta
[3] Consultar usuario
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
            input("\nPressione ENTER para voltar ao menu...")

        elif opcao == "2":
           
           usuarios, contas = criar_conta(usuarios, contas)
           input("\nPressione ENTER para voltar ao menu...")

        elif opcao == "3":

            listar_usuarios(usuarios)
            input("\nPressione ENTER para voltar ao menu...")

        elif opcao == "4":

            conta = encontrar_conta(contas)
            if conta is not None:
                conta = depositar(conta)
            input("\nPressione ENTER para voltar ao menu...")

        elif opcao == "5":

            conta = encontrar_conta(contas)
            if conta is not None:
                conta = sacar(conta, limite, LIMITE_SAQUES)
            input("\nPressione ENTER para voltar ao menu...")    

        elif opcao == "6":
                
                conta = encontrar_conta(contas)

                if conta is not None:
                    exibir_extrato(conta)
                input("\nPressione ENTER para voltar ao menu...")    

        elif opcao == "7":

                    transferir(contas)
                    input("\nPressione ENTER para voltar ao menu...")

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
        time.sleep(1)

    else:

        print("Operação falhou! O valor informado é inválido.")
        time.sleep(1)

    return conta
     

def sacar(conta, limite, LIMITE_SAQUES):

    valor = float(input("Informe o valor do saque: "))

    excedeu_saldo = valor > conta["saldo"]
    excedeu_limite = valor > limite
    excedeu_saques = conta["numero_saques"] >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação falhou! Saldo insuficiente.")
        time.sleep(1)
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
        time.sleep(1)
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
        time.sleep(1)
    elif valor > 0:
        conta["saldo"] -= valor
        horario = horario_atual()
        conta["extrato"] += f"Saque: R$ {valor:.2f} - {horario.strftime('%d/%m/%Y %H:%M:%S')}\n"
        conta["numero_saques"] += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
        time.sleep(1)
    else:
        print("Operação falhou! O valor informado é inválido.")
        time.sleep(1)
    return conta
  

def exibir_extrato(conta):

        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not conta["extrato"] else conta["extrato"])
        print(f"\nSaldo: R$ {conta['saldo']:.2f}")
        print("==========================================")
        time.sleep(1)


def criar_usuario(usuarios):
    nome = input("Informe o nome completo: ")
    while True:
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ").replace("/", "").replace("-", "")
        if len(data_nascimento) != 8 or not data_nascimento.isdigit():
            print("Data de nascimento deve conter 8 numeros.")
            time.sleep(1)
        else:
            break    
    
    while True:
        cpf = input("Informe o CPF (somente números): ").replace(".", "").replace("-", "")
        if len(cpf) != 11 or not cpf.isdigit():
            print("CPF deve conter 11 numeros.")
            time.sleep(1)
        else:
            break           

    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("Já existe usuário com esse CPF!")
            time.sleep(1)
            return usuarios

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf})

    print("Usuário criado com sucesso!")
    time.sleep(2)

    return usuarios


def consultar_usuario(usuarios):
    cpf = input("Informe o CPF do usuário para listar: ").replace(".", "").replace("-", "")

    usuario_encontrado = None

    for usuario in usuarios: 
        if usuario["cpf"] == cpf:
            usuario_encontrado = usuario
            
            print("\n=== Usuário ===")
            print(f"Nome: {usuario['nome']}")
            print(f"CPF: {usuario['cpf']}")
            print(f"Data de Nascimento: {usuario['data_nascimento']}")
            print("================")
            time.sleep(1)
            return

    if usuario_encontrado is None:
        print("Usuário não encontrado!")
        time.sleep(1)
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
            time.sleep(1)
            return usuarios, contas

    if usuario_encontrado is None:
           print("Usuário não encontrado!")
           time.sleep(1)
           return usuarios, contas     


def encontrar_conta(contas):
    cpf = input("Informe o seu CPF: ").replace(".", "").replace("-", "")
    numero_conta = int(input("informe o numero da conta: "))
 
    for conta in contas:
        if conta["usuario"]["cpf"] == cpf and conta["numero"] == numero_conta:
            return conta

    print("Conta nao encontrada.")
    time.sleep(1)
    return None

    
def transferir(contas):

  conta_origem = encontrar_conta(contas)
  conta_destino = encontrar_conta(contas)
  

  if conta_origem is not None and conta_destino is not None:

    if conta_origem["usuario"]["cpf"] == conta_destino["usuario"]["cpf"] and conta_origem["numero"] == conta_destino["numero"]:
            print("Operaçao falhou! A conta de origem e destino são iguais.")
            time.sleep(1)
            return
  
    valor = float(input("Informe o valor da transferencia: "))

    excedeu_saldo = valor > conta_origem["saldo"]

    if excedeu_saldo:

        print("Saldo da conta insuficiente.")
        time.sleep(1)

    elif valor > 0:

        conta_origem["saldo"]  -= valor
        conta_destino["saldo"] += valor
        horario = horario_atual()
        conta_origem["extrato"] += f"transferencia para {conta_destino['usuario']['nome']}: R$ {valor:.2f} - {horario.strftime('%d/%m/%Y %H:%M:%S')}\n"
        conta_destino["extrato"] += f"transferencia recebida de {conta_origem['usuario']['nome']}: R$ {valor:.2f} - {horario.strftime('%d/%m/%Y %H:%M:%S')}\n"
        print(f"Tranferencia de R$ {valor:.2f} realizado com sucesso!")
        time.sleep(1)

    else:
        print(f"Operacao falhou! valor informado é invalido.")
        time.sleep(1)


def horario_atual():

    return datetime.now(ZoneInfo("America/Sao_Paulo"))
       
main()
