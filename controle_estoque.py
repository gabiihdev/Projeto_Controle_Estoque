def processar_string(estoque_inicial):
    produtos = []
    produtos_separados = estoque_inicial.split('#')

    for produto in produtos_separados:
        info_produto = produto.split(';')
        produto = {
            "Descrição": info_produto[0],
            "Código": int(info_produto[1]),
            "Qtd_estoque": int(info_produto[2]),
            "Custo_produto": float(info_produto[3]),
            "Preço_venda": float(info_produto[4]),
        }

        produtos.append(produto)
    return produtos


def validar_int(num):
    while True:
        valor = input(num)
        
        try:
            valor_int = int(valor)
            return valor_int
        
        except ValueError:
            print('>> ERRO: DIGITE UM NÚMERO INTEIRO.\n')


def validar_float(num):
    while True:
        valor = input(num)
        
        try:
            valor_float = float(valor)
            return valor_float
        
        except ValueError:
            print('>> ERRO: DIGITE UM NÚMERO VÁLIDO.\n')


def cadastrar_produtos(estoque):
    descricao = input('Digite a descrição do produto: ').strip()
    if any(produto['Descrição'].lower() == descricao.lower() for produto in estoque):
       print(f'\n>> ERRO: O PRODUTO "{descricao.upper()}" JÁ ESTÁ CADASTRADO NO ESTOQUE.')
       return
    
    codigo = validar_int('Digite o código: ')
    for produto in estoque:
        if codigo == produto['Código']:
            print(f'\n>> ERRO: EXISTE UM PRODUTO COM O CÓDIGO {codigo} NO ESTOQUE.')
            return

    qtd_estoque = validar_int('Digite a quantidade do produto em estoque: ')
    custo_produto = validar_float('Digite o custo do produto: ')
    preco_venda = validar_float('Digite o preço de venda do produto: ')

    produto = {
        "Descrição": descricao,
        "Código": codigo,
        "Qtd_estoque": qtd_estoque,
        "Custo_produto": custo_produto,
        "Preço_venda": preco_venda,
    }

    estoque.append(produto)
    print(f'\n>> PRODUTO ({produto["Descrição"].upper()}) CADASTRADO COM SUCESSO!')


def menu():
    while True:
        print('_' * 130)
        print('\n==================== MENU ====================')
        print('[1] - Cadastrar produto')
        print('[0] - Sair do programa\n')

        opcao = input('ESCOLHA UMA OPÇÃO: ')
        print('_' * 130)
        
        if opcao == '1':
            cadastrar_produtos(estoque)
        elif opcao == '0':
            print('>> Programa encerrado.')
            break
        else:
            print('>> OPÇÃO INVÁLIDA.')


estoque_inicial = "Notebook Dell;201;15;3200.00;4500.00#Notebook Lenovo;202;10;2800.00;4200.00#Mouse Logitech;203;50;70.00;150.00#Mouse Razer;204;40;120.00;250.00#Monitor Samsung;205;10;800.00;1200.00#Monitor LG;206;8;750.00;1150.00#Teclado Mecânico Corsair;207;30;180.00;300.00#Teclado Mecânico Razer;208;25;200.00;350.00#Impressora HP;209;5;400.00;650.00#Impressora Epson;210;3;450.00;700.00#Monitor Dell;211;12;850.00;1250.00#Monitor AOC;212;7;700.00;1100.00"
estoque = processar_string(estoque_inicial)
menu()
