Menu = """

----------- MENU ------------
[1] Deposito 
[2] Saque
[3] Extrato
[4] Sair
-----------------------------

=>   """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(Menu)

    if opcao  == "1":
        valor = (input("Informe o valor do depósito, ou digite MENU para voltar ao menu: "))

        if valor.upper() == "MENU":
            print("Voltando ao menu principal...")
            continue

        valor = float(valor)

        if valor > 0: 
            saldo += valor 
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print (f"Voce depositou R$ {valor:.2f} com sucesso! Em 15 minutos sera debitado em sua conta. Por favor, aguerde...")

       

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "2":
        valor = (input("Informe o valor do saque, ou digite MENU para voltar ao menu: "))

      

        if valor.upper() == "MENU":
            print("Voltando ao menu principal...")
            continue

        valor = float(valor)

        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação falhou! Saldo insuficiente.")
        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")
        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        

        else:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            print(f"Voce sacou R$ {valor:.2f} com sucesso!")

    elif opcao == "3":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================") 

    elif opcao == "4":
        print("Saindo do programa...")
        break

    else: 
        print("Operação inválida, por favor selecione novamente a operação desejada.")