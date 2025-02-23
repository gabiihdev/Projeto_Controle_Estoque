import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


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
    print(
        f'\n>> PRODUTO ({produto["Descrição"].upper()}) CADASTRADO COM SUCESSO!')


def listar_produtos(estoque):
    if not estoque:
        print('>> ESTOQUE VAZIO.')
        return

    print(f"{'Descrição'.ljust(25)}{'Código'.rjust(17)}{'Quantidade'.rjust(19)}{'Custo do produto'.rjust(24)}{'Preço de venda'.rjust(22)}")
    print('-' * 130)

    for n, produto in enumerate(estoque):
        descricao = produto['Descrição']
        codigo = produto['Código']
        qtd_estoque = produto['Qtd_estoque']
        custo_produto = locale.currency(produto['Custo_produto'], grouping=True)
        preco_venda = locale.currency(produto['Preço_venda'], grouping=True)

        print(descricao.ljust(30), str(codigo).rjust(10), str(qtd_estoque).rjust(15), custo_produto.rjust(23), preco_venda.rjust(23))


def ordenar_produtos_por_qtd(estoque):
    if not estoque:
        print('>> ESTOQUE VAZIO.')
        return

    ordem = input('Deseja ordenar os produtos em ordem crescente ou decrescente: ').lower()

    if ordem == 'crescente':
        produtos_ordenados = sorted(estoque, key=lambda x: x['Qtd_estoque'])
        print(f"\n{'PRODUTOS ORDENADOS EM ORDEM CRESCENTE'.rjust(75)}\n")
        print('-' * 130)
        listar_produtos(produtos_ordenados)

    elif ordem == 'decrescente':
        produtos_ordenados = sorted(estoque, key=lambda x: x['Qtd_estoque'], reverse=True)
        print(f"\n{'PRODUTOS ORDENADOS EM ORDEM DECRESCENTE'.rjust(75)}\n")
        print('-' * 130)
        listar_produtos(produtos_ordenados)

    else:
        print('>> ORDEM INVÁLIDA. ESCOLHA ENTRE "CRESCENTE" OU "DESCRESCENTE".')


def buscar_produto(estoque):
    if not estoque:
        print('>> ESTOQUE VAZIO.')
        return

    item = input(
        'Digite a descrição ou o código do produto que deseja buscar: ')
    produtos_encontrados = []

    try:
        codigo_int = int(item)

        for produto in estoque:
            if codigo_int == produto['Código']:
                produtos_encontrados.append(produto)

    except ValueError:
        for produto in estoque:
            if item.lower() in produto['Descrição'].lower():
                produtos_encontrados.append(produto)

    if produtos_encontrados:
        print(f"\n{'PRODUTOS ENCONTRADOS'.rjust(75)}\n")
        print('-' * 130)
        listar_produtos(produtos_encontrados)
    else:
        print('>> PRODUTO NÃO ENCONTRADO.')


def remover_produto(estoque):
    if not estoque:
        print('>> ESTOQUE VAZIO.')
        return

    codigo = validar_int('Digite o código do produto que deseja remover: ')

    for produto in estoque:
        if codigo == produto['Código']:
            estoque.remove(produto)
            print(f">> PRODUTO COM CÓDIGO {codigo} ({produto['Descrição']}) REMOVIDO COM SUCESSO!")
            return

    print('>> PRODUTO NÃO ENCONTRADO.')


def consultar_produtos_esgotados(estoque):
    if not estoque:
        print('>> ESTOQUE VAZIO')
        return

    produtos_esgotados = []

    for produto in estoque:
        if produto['Qtd_estoque'] == 0:
            produtos_esgotados.append(produto)

    if produtos_esgotados:
        print(f"{'PRODUTOS ESGOTADOS'.rjust(75)}\n")
        listar_produtos(produtos_esgotados)
    else:
        print('>> NENHUM PRODUTO ESGOTADO.')


def filtrar_produtos_baixa_qtd(estoque, quantidade_padrao=5):
    try:
        quantidade_max = input('Digite a quantidade limite dos produtos que deseja filtrar (padrão = 5): ')

        if quantidade_max:
            quantidade = int(quantidade_max)
        else:
            quantidade = quantidade_padrao

        produtos_baixa_qtd = list(filter(lambda produto: produto['Qtd_estoque'] <= quantidade, estoque))

        if produtos_baixa_qtd:
            print(f"\n{'PRODUTOS COM QUANTIDADE MENOR OU IGUAL A ' + str(quantidade):^115}\n")
            print('-' * 130)
            listar_produtos(produtos_baixa_qtd)
        else:
            print(f'>> NENHUM PRODUTO COM QUANTIDADE MENOR OU IGUAL A {quantidade}.')

    except ValueError:
        print('>> ERRO: DIGITE UM NÚMERO INTEIRO.')
        return


def atualizar_quantidade(estoque):
    codigo = validar_int('Digite o código do produto que deseja atualizar a quantidade: ')

    for produto in estoque:
        if codigo == produto['Código']:
            while True:
                opcao = input('Digite [1] para entrada(aumento) ou [2] para saída(redução): ')

                if opcao not in ('1', '2'):
                    print('\n>> OPÇÃO INVÁLIDA. DIGITE 1 OU 2.')
                    continue

                while True:
                    quantidade = validar_int('Digite a quantidade: ')

                    if quantidade <= 0:
                        print("\n>> ERRO: A QUANTIDADE DEVE SER MAIOR QUE 0.")
                        continue

                    if opcao == '2' and quantidade > produto['Qtd_estoque']:
                        print("\n>> ERRO: A SAÍDA É MAIOR DO QUE O ESTOQUE DISPONÍVEL.")
                        continue

                    produto['Qtd_estoque'] += quantidade if opcao == '1' else -quantidade
                    print(f"\n>> A QUANTIDADE EM ESTOQUE DO PRODUTO ({produto['Descrição']}) FOI ATUALIZADA PARA {produto['Qtd_estoque']}.")
                    return

    print('>> PRODUTO NÃO ENCONTRADO.')


def atualizar_preco(estoque):
    codigo = validar_int('Digite o código do produto: ')
        
    for produto in estoque:
        if codigo == produto['Código']:
            novo_preco = validar_float('Digite o novo preço do produto: ')
            produto['Preco_venda'] = novo_preco
            novo_preco_formatado = locale.currency(novo_preco, grouping=True)

            print(f"\n>> PREÇO DO PRODUTO ({produto['Descrição'].upper()}) ATUALIZADO PARA {novo_preco_formatado}")
            return
                 
    print('>> PRODUTO NÃO ENCONTRADO.')


def calcular_total_estoque(estoque):
    total = 0

    print(f"\n{'Produto'.ljust(38)} {'Total em estoque'.rjust(10)}")
    print('-' * 60)
    
    for produto in estoque:
        total_produto = produto['Qtd_estoque'] * produto['Preço_venda']
        total_produto_formatado = locale.currency(total_produto, grouping=True)

        print(f"{produto['Descrição'].ljust(40)} {total_produto_formatado}".rjust(20))
        total += total_produto
        
    total_formatado = locale.currency(total, grouping=True)
    print(f"\n{'VALOR TOTAL DO ESTOQUE'.ljust(40)} {total_formatado}")


def calcular_lucro_presumido(estoque):
    lucro_total = 0 
    print(f"\n{'Produto'.ljust(38)} {'Lucro Presumido'.rjust(10)}")
    print('-' * 60)   
    
    for produto in estoque:
        lucro_produto = (produto['Preço_venda'] - produto['Custo_produto']) * produto['Qtd_estoque']
        lucro_produto_formatado = locale.currency(lucro_produto, grouping=True)
        
        print(f"{produto['Descrição'].ljust(40)} {lucro_produto_formatado}".rjust(20))
        lucro_total += lucro_produto
 
    lucro_total_formatado = locale.currency(lucro_total, grouping=True)   
    print(f"\n{'LUCRO TOTAL PRESUMIDO DO ESTOQUE'.ljust(40)} {lucro_total_formatado}")
    
    
def gerar_relatorio_geral(estoque):
    if not estoque:
        print('>> ESTOQUE VAZIO.')
        return
    
    print(f"\n{'RELATÓRIO GERAL DO ESTOQUE'.rjust(75)}\n")
    print('-' * 130)
    print(f"{'Descrição'.ljust(25)}{'Código'.rjust(17)}{'Quantidade'.rjust(19)}{'Custo do produto'.rjust(24)}{'Preço de venda'.rjust(22)}{'Valor total'.rjust(22)}")
    print('-' * 130)

    custo_total = 0
    faturamento_total = 0

    for produto in estoque:
        descricao = produto['Descrição']
        codigo = produto['Código']
        qtd_estoque = produto['Qtd_estoque']
        custo_produto = produto['Custo_produto']
        preco_venda = produto['Preço_venda']
        total_produto =  qtd_estoque * preco_venda
        custo_total += qtd_estoque * custo_produto
        faturamento_total += total_produto
        lucro_total_bruto = faturamento_total - custo_total

        
        custo_produto_formatado = locale.currency(custo_produto, grouping=True)
        preco_venda_formatado = locale.currency(preco_venda, grouping=True)
        total_produto_formatado = locale.currency(total_produto, grouping=True)
        
        print(descricao.ljust(30), str(codigo).rjust(10), str(qtd_estoque).rjust(15), custo_produto_formatado.rjust(23), preco_venda_formatado.rjust(23), total_produto_formatado.rjust(23))
    
    print('-' * 130)
    
    custo_total_formatado = locale.currency(custo_total, grouping=True)
    faturamento_total_formatado = locale.currency(faturamento_total, grouping=True)
    lucro_total_bruto_formatado = locale.currency(lucro_total_bruto, grouping=True)

    print(f"\n{'CUSTO TOTAL:'.ljust(115)} {custo_total_formatado}")
    print(f"{'FATURAMENTO TOTAL:'.ljust(115)} {faturamento_total_formatado}")
    print(f"{'LUCRO TOTAL BRUTO:'.ljust(115)} {lucro_total_bruto_formatado}")
    

def menu():
    while True:
        print('_' * 130)
        print('\n==================== MENU ====================')
        print('[1] - Cadastrar produto')
        print('[2] - Listar produtos')
        print('[3] - Ordenar produtos por quantidade')
        print('[4] - Buscar produto')
        print('[5] - Remover produto')
        print('[6] - Consultar produtos esgotados')
        print('[7] - Filtrar produtos com baixa quantidade')
        print('[8] - Atualizar quantidade do produto')
        print('[9] - Atualizar preço do produto')
        print('[10] - Consultar valor total do estoque')
        print('[11] - Consultar lucro presumido do estoque')
        print('[12] - Gerar relatório geral do estoque')
        print('[0] - Sair do programa\n')

        opcao = input('ESCOLHA UMA OPÇÃO: ')
        print('_' * 130)

        if opcao == '1':
            cadastrar_produtos(estoque)
        elif opcao == '2':
            listar_produtos(estoque)
        elif opcao == '3':
            ordenar_produtos_por_qtd(estoque)
        elif opcao == '4':
            buscar_produto(estoque)
        elif opcao == '5':
            remover_produto(estoque)
        elif opcao == '6':
            consultar_produtos_esgotados(estoque)
        elif opcao == '7':
            filtrar_produtos_baixa_qtd(estoque)
        elif opcao == '8':
            atualizar_quantidade(estoque)
        elif opcao == '9':
            atualizar_preco(estoque)
        elif opcao == '10':
            calcular_total_estoque(estoque)
        elif opcao == '11':
            calcular_lucro_presumido(estoque)
        elif opcao == '12':
            gerar_relatorio_geral(estoque)
        elif opcao == '0':
            print('>> Programa encerrado.')
            break
        else:
            print('>> OPÇÃO INVÁLIDA.')


estoque_inicial = "Notebook Dell;201;15;3200.00;4500.00#Notebook Lenovo;202;10;2800.00;4200.00#Mouse Logitech;203;50;70.00;150.00#Mouse Razer;204;40;120.00;250.00#Monitor Samsung;205;10;800.00;1200.00#Monitor LG;206;8;750.00;1150.00#Teclado Mecânico Corsair;207;30;180.00;300.00#Teclado Mecânico Razer;208;25;200.00;350.00#Impressora HP;209;5;400.00;650.00#Impressora Epson;210;3;450.00;700.00#Monitor Dell;211;12;850.00;1250.00#Monitor AOC;212;7;700.00;1100.00"
estoque = processar_string(estoque_inicial)
menu()
