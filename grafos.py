# Implementação de Grafos usando NetworkX
# Permite ao usuário inserir vértices e arestas de forma interativa
# Gera uma visualização gráfica do grafo

import networkx as nx
import matplotlib.pyplot as plt


def criar_grafo():
    # Cria e retorna um grafo não direcionado vazio
    return nx.Graph()


def adicionar_vertice(grafo, vertice):
    # Adiciona um vértice ao grafo, respeitando o limite de 10 vértices
    if grafo.number_of_nodes() >= 10:
        print("Limite máximo de 10 vértices atingido.")
        return

    if vertice in grafo.nodes():
        print(f"O vértice '{vertice}' já existe.")
    else:
        grafo.add_node(vertice)
        print(f"Vértice '{vertice}' adicionado com sucesso!")


def adicionar_aresta(grafo, vertice1, vertice2, peso=None):
    # Adiciona uma aresta ao grafo, respeitando o limite de 20 arestas
    if grafo.number_of_edges() >= 20:
        print("Limite máximo de 20 arestas atingido.")
        return

    if vertice1 not in grafo.nodes() or vertice2 not in grafo.nodes():
        print("Ambos os vértices devem existir antes de criar a aresta.")
        return

    if peso is not None:
        grafo.add_edge(vertice1, vertice2, weight=peso)
        print(f"Aresta '{vertice1}' <-> '{vertice2}' (peso: {peso}) adicionada!")
    else:
        grafo.add_edge(vertice1, vertice2)
        print(f"Aresta '{vertice1}' <-> '{vertice2}' adicionada!")


def remover_vertice(grafo, vertice):
    # Remove um vértice do grafo
    if vertice in grafo.nodes():
        grafo.remove_node(vertice)
        print(f"Vértice '{vertice}' removido com sucesso!")
    else:
        print(f"Vértice '{vertice}' não encontrado.")


def remover_aresta(grafo, vertice1, vertice2):
    # Remove uma aresta do grafo
    if grafo.has_edge(vertice1, vertice2):
        grafo.remove_edge(vertice1, vertice2)
        print(f"Aresta '{vertice1}' <-> '{vertice2}' removida com sucesso!")
    else:
        print(f"Aresta '{vertice1}' <-> '{vertice2}' não encontrada.")


def listar_vertices(grafo):
    # Lista todos os vértices do grafo
    vertices = list(grafo.nodes())
    if vertices:
        print(f"\nVértices ({len(vertices)}): {vertices}")
    else:
        print("\nO grafo não possui vértices.")


def listar_arestas(grafo):
    # Lista todas as arestas do grafo
    arestas = list(grafo.edges(data=True))
    if arestas:
        print(f"\nArestas ({len(arestas)}):")
        for a in arestas:
            if 'weight' in a[2]:
                print(f"  {a[0]} <-> {a[1]} (peso: {a[2]['weight']})")
            else:
                print(f"  {a[0]} <-> {a[1]}")
    else:
        print("\nO grafo não possui arestas.")


def visualizar_grafo(grafo):
    # Exibe e salva a visualização do grafo
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
        font_weight="bold"
    )

    edge_labels = nx.get_edge_attributes(grafo, 'weight')
    if edge_labels:
        nx.draw_networkx_edge_labels(grafo, pos, edge_labels)

    plt.title("Visualização do Grafo")
    plt.savefig("grafo.png")
    plt.show()

    print("Imagem do grafo salva como 'grafo.png'")


def mostrar_informacoes(grafo):
    # Mostra informações gerais do grafo
    print("\n===INFORMAÇÕES DO GRAFO===")
    print(f"Número de vértices: {grafo.number_of_nodes()}")
    print(f"Número de arestas: {grafo.number_of_edges()}")

    if grafo.number_of_nodes() > 0:
        print("Grau dos vértices:")
        for v in grafo.nodes():
            print(f"  {v}: grau {grafo.degree(v)}")

        if grafo.number_of_nodes() > 1:
            print("Grafo conexo:", "Sim" if nx.is_connected(grafo) else "Não")


def menu():
    # Exibe o menu principal
    print("\n========= MENU =========")
    print("O que você deseja fazer?\n")
    print("1 - Adicionar vértice")
    print("2 - Adicionar aresta")
    print("3 - Remover vértice")
    print("4 - Remover aresta")
    print("5 - Listar vértices")
    print("6 - Listar arestas")
    print("7 - Visualizar grafo")
    print("8 - Informações do grafo")
    print("0 - Sair")
    return input("\nEscolha uma opção: ")


def main():
    # Função principal
    grafo = criar_grafo()
    print("Sistema de Grafos - NetworkX")

    while True:
        opcao = menu()

        if opcao == "1":
            v = input("Nome do vértice: ")
            adicionar_vertice(grafo, v)

        elif opcao == "2":
            v1 = input("Vértice de origem: ")
            v2 = input("Vértice de destino: ")
            peso_input = input("Peso da aresta (Enter para nenhum): ")

            try:
                peso = float(peso_input) if peso_input else None
                adicionar_aresta(grafo, v1, v2, peso)
            except ValueError:
                print("Peso inválido. Digite um número.")

        elif opcao == "3":
            listar_vertices(grafo)
            v = input("Vértice a remover: ")
            remover_vertice(grafo, v)

        elif opcao == "4":
            listar_arestas(grafo)
            v1 = input("Primeiro vértice: ")
            v2 = input("Segundo vértice: ")
            remover_aresta(grafo, v1, v2)

        elif opcao == "5":
            listar_vertices(grafo)

        elif opcao == "6":
            listar_arestas(grafo)

        elif opcao == "7":
            visualizar_grafo(grafo)

        elif opcao == "8":
            mostrar_informacoes(grafo)

        elif opcao == "0":
            print("Encerrando o programa...")
            print("Obrigado por utilizar nosso código!")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
