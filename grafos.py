# Implementação de Grafos usando NetworkX: Permite ao usuário inserir vértices e arestas de forma interativa

import networkx as nx
import matplotlib.pyplot as plt

# Constantes de limite para evitar lentidão na visualização
MAX_VERTICES = 10
MAX_ARESTAS = 20


def criar_grafo():
    # Pergunta ao usuário o tipo de grafo desejado
    while True:
        print("\nEscolha o tipo de grafo:")
        print("1. Não Direcionado (Simples)")
        print("2. Direcionado (Com setas)")
        resp = input("Opção: ")
        if resp == '1':
            return nx.Graph()
        elif resp == '2':
            return nx.DiGraph()
        print("Opção inválida.")


def adicionar_vertice(grafo, vertice):
    if grafo.number_of_nodes() >= MAX_VERTICES:
        print("Limite máximo de 10 vértices atingido.")
        return

    if vertice in grafo.nodes():
        print(f"O vértice '{vertice}' já existe.")
    else:
        grafo.add_node(vertice)
        print(f"Vértice '{vertice}' adicionado com sucesso!")


def adicionar_aresta(grafo, vertice1, vertice2, peso=None):
    if grafo.number_of_edges() >= MAX_ARESTAS:
        print("Limite máximo de 20 arestas atingido.")
        return

    if vertice1 not in grafo.nodes() or vertice2 not in grafo.nodes():
        print("Ambos os vértices devem existir antes de criar a aresta.")
        return

    if peso is not None:
        grafo.add_edge(vertice1, vertice2, weight=peso)
        print(f"Aresta '{vertice1}' -> '{vertice2}' (peso: {peso}) adicionada!")
    else:
        grafo.add_edge(vertice1, vertice2)
        print(f"Aresta '{vertice1}' -> '{vertice2}' adicionada!")


def remover_vertice(grafo, vertice):
    if vertice in grafo.nodes():
        grafo.remove_node(vertice)
        print(f"Vértice '{vertice}' removido com sucesso!")
    else:
        print(f"Vértice '{vertice}' não encontrado.")


def remover_aresta(grafo, vertice1, vertice2):
    if grafo.has_edge(vertice1, vertice2):
        grafo.remove_edge(vertice1, vertice2)
        print(f"Aresta '{vertice1}' -> '{vertice2}' removida com sucesso!")
    else:
        print(f"Aresta '{vertice1}' -> '{vertice2}' não encontrada.")


def listar_vertices(grafo):
    vertices = list(grafo.nodes())
    if vertices:
        print(f"\nVértices ({len(vertices)}): {vertices}")
    else:
        print("\nO grafo não possui vértices.")


def listar_arestas(grafo):
    arestas = list(grafo.edges(data=True))
    if arestas:
        print(f"\nArestas ({len(arestas)}):")
        for a in arestas:
            if 'weight' in a[2]:
                print(f"  {a[0]} -> {a[1]} (peso: {a[2]['weight']})")
            else:
                print(f"  {a[0]} -> {a[1]}")
    else:
        print("\nO grafo não possui arestas.")


def visualizar_grafo(grafo):
    if grafo.number_of_nodes() == 0:
        print("O grafo está vazio.")
        return

    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(grafo, seed=42)

    nx.draw(
        grafo,
        pos,
        with_labels=True,
        node_color="lightblue",
        node_size=700,
        arrows=grafo.is_directed(),
        font_weight="bold"
    )

    edge_labels = nx.get_edge_attributes(grafo, 'weight')
    if edge_labels:
        nx.draw_networkx_edge_labels(grafo, pos, edge_labels)

    plt.title("Visualização do Grafo")
    plt.axis('off')
    plt.show()


def mostrar_informacoes(grafo):
    print("\n=== INFORMAÇÕES DO GRAFO ===")
    print(f"Número de vértices: {grafo.number_of_nodes()}")
    print(f"Número de arestas: {grafo.number_of_edges()}")

    if grafo.number_of_nodes() > 0:
        print("Grau dos vértices:")
        for v in grafo.nodes():
            print(f"  {v}: grau {grafo.degree(v)}")

        if grafo.number_of_nodes() > 1:
            if grafo.is_directed():
                conexo = nx.is_weakly_connected(grafo)
                tipo = "Fracamente conexo"
            else:
                conexo = nx.is_connected(grafo)
                tipo = "Conexo"
            print(f"Grafo {tipo}:", "Sim" if conexo else "Não")


def calcular_caminho_curto(grafo, origem, destino):
    try:
        caminho = nx.shortest_path(grafo, source=origem, target=destino, weight='weight')
        custo = nx.shortest_path_length(grafo, source=origem, target=destino, weight='weight')
        print(f"\nCaminho mais curto de '{origem}' para '{destino}': {caminho}")
        print(f"Custo total: {custo}")
    except nx.NetworkXNoPath:
        print("Não existe caminho entre os vértices.")
    except nx.NodeNotFound as e:
        print(f"Erro: {e}")


def realizar_busca(grafo, inicio):
    if inicio not in grafo:
        print(f"O vértice '{inicio}' não existe.")
        return

    ordem_visita = list(nx.bfs_tree(grafo, source=inicio))
    print(f"\nBusca em Largura (BFS) a partir de '{inicio}':")
    print(f"Ordem de visita: {ordem_visita}")


def gerar_grafo_predefinido(grafo):
    # Limpa o grafo atual
    grafo.clear()

    vertices = ["A", "B", "C", "D", "E"]
    for v in vertices:
        grafo.add_node(v)

    arestas = [
        ("A", "B", 2),
        ("A", "C", 4),
        ("B", "C", 1),
        ("B", "D", 7),
        ("C", "E", 3),
        ("D", "E", 1)
    ]

    for origem, destino, peso in arestas:
        grafo.add_edge(origem, destino, weight=peso)

    print("\nGrafo pré-definido criado com sucesso!")
    print("Tipo:", "Direcionado" if grafo.is_directed() else "Não Direcionado")


def menu():
    print("\n" + "=" * 50)
    print("       SISTEMA DE GRAFOS - W/H/O/")
    print("=" * 50)
    print("  1. Adicionar vértice")
    print("  2. Adicionar aresta")
    print("  3. Remover vértice")
    print("  4. Remover aresta")
    print("  5. Listar vértices")
    print("  6. Listar arestas")
    print("  7. Visualizar grafo")
    print("  8. Informações do grafo")
    print("  9. Caminho mais curto (Dijkstra)")
    print("  10. Busca em Largura (BFS)")
    print("  11. Gerar grafo pré-definido")
    print("  0. Sair")
    print("=" * 50)
    return input("Escolha uma opção: ")


def main():
    grafo = criar_grafo()
    print("\nBem-vindo ao Sistema de Grafos!")
    print("Feito e Otimizado pela equipe Wesley, Heloiza e Ortega.\n")

    while True:
        opcao = menu()

        if opcao == "1":
            adicionar_vertice(grafo, input("Nome do vértice: "))

        elif opcao == "2":
            v1 = input("Vértice de origem: ")
            v2 = input("Vértice de destino: ")
            p = input("Peso (Enter para nenhum): ")
            peso = float(p) if p else None
            adicionar_aresta(grafo, v1, v2, peso)

        elif opcao == "3":
            listar_vertices(grafo)
            remover_vertice(grafo, input("Vértice a remover: "))

        elif opcao == "4":
            listar_arestas(grafo)
            remover_aresta(grafo, input("Primeiro vértice: "), input("Segundo vértice: "))

        elif opcao == "5":
            listar_vertices(grafo)

        elif opcao == "6":
            listar_arestas(grafo)

        elif opcao == "7":
            visualizar_grafo(grafo)

        elif opcao == "8":
            mostrar_informacoes(grafo)

        elif opcao == "9":
            calcular_caminho_curto(grafo, input("Origem: "), input("Destino: "))

        elif opcao == "10":
            realizar_busca(grafo, input("Vértice inicial: "))

        elif opcao == "11":
            gerar_grafo_predefinido(grafo)

        elif opcao == "0":
            print("Encerrando o programa...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
