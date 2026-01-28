"""
Implementação de Grafos usando NetworkX
Permite ao usuário inserir vértices e arestas de forma interativa

Limites:
- Máximo de 10 vértices
- Máximo de 20 arestas
"""

import networkx as nx
import matplotlib.pyplot as plt

# Constantes de limite para evitar lentidão na visualização
MAX_VERTICES = 10
MAX_ARESTAS = 20


def criar_grafo():
    """Cria um novo grafo vazio"""
    return nx.Graph()


def adicionar_vertice(grafo, vertice):
    """Adiciona um vértice ao grafo"""
    grafo.add_node(vertice)
    print(f"✓ Vértice '{vertice}' adicionado com sucesso!")


def adicionar_aresta(grafo, vertice1, vertice2, peso=None):
    """Adiciona uma aresta entre dois vértices"""
    if peso:
        grafo.add_edge(vertice1, vertice2, weight=peso)
        print(f"✓ Aresta '{vertice1}' <-> '{vertice2}' (peso: {peso}) adicionada com sucesso!")
    else:
        grafo.add_edge(vertice1, vertice2)
        print(f"✓ Aresta '{vertice1}' <-> '{vertice2}' adicionada com sucesso!")


def remover_vertice(grafo, vertice):
    """Remove um vértice do grafo"""
    if vertice in grafo.nodes():
        grafo.remove_node(vertice)
        print(f"✓ Vértice '{vertice}' removido com sucesso!")
    else:
        print(f"✗ Vértice '{vertice}' não encontrado!")


def remover_aresta(grafo, vertice1, vertice2):
    """Remove uma aresta do grafo"""
    if grafo.has_edge(vertice1, vertice2):
        grafo.remove_edge(vertice1, vertice2)
        print(f"✓ Aresta '{vertice1}' <-> '{vertice2}' removida com sucesso!")
    else:
        print(f"✗ Aresta '{vertice1}' <-> '{vertice2}' não encontrada!")


def listar_vertices(grafo):
    """Lista todos os vértices do grafo"""
    vertices = list(grafo.nodes())
    if vertices:
        print(f"\n📍 Vértices ({len(vertices)}): {vertices}")
    else:
        print("\n⚠ O grafo não possui vértices.")
    return vertices


def listar_arestas(grafo):
    """Lista todas as arestas do grafo"""
    arestas = list(grafo.edges(data=True))
    if arestas:
        print(f"\n🔗 Arestas ({len(arestas)}):")
        for aresta in arestas:
            if 'weight' in aresta[2]:
                print(f"   {aresta[0]} <-> {aresta[1]} (peso: {aresta[2]['weight']})")
            else:
                print(f"   {aresta[0]} <-> {aresta[1]}")
    else:
        print("\n⚠ O grafo não possui arestas.")
    return arestas


def visualizar_grafo(grafo):
    """Visualiza o grafo graficamente"""
    if len(grafo.nodes()) == 0:
        print("\n⚠ O grafo está vazio. Adicione vértices primeiro!")
        return
    
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(grafo, seed=42)
    
    # Desenha os nós
    nx.draw_networkx_nodes(grafo, pos, node_color='lightblue', 
                          node_size=700, alpha=0.9)
    
    # Desenha as arestas
    nx.draw_networkx_edges(grafo, pos, edge_color='black', 
                          width=2, alpha=0.7)
    
    # Desenha os rótulos dos vértices
    nx.draw_networkx_labels(grafo, pos, font_size=12, font_weight='bold')
    
    # Desenha os pesos das arestas (se existirem)
    edge_labels = nx.get_edge_attributes(grafo, 'weight')
    if edge_labels:
        nx.draw_networkx_edge_labels(grafo, pos, edge_labels, font_size=10)
    
    plt.title("Visualização do Grafo", fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def mostrar_informacoes(grafo):
    """Mostra informações sobre o grafo"""
    print("\n" + "=" * 50)
    print("📊 INFORMAÇÕES DO GRAFO")
    print("=" * 50)
    print(f"   Número de vértices: {grafo.number_of_nodes()}")
    print(f"   Número de arestas: {grafo.number_of_edges()}")
    
    if grafo.number_of_nodes() > 0:
        print(f"   Grau dos vértices:")
        for node in grafo.nodes():
            print(f"      - {node}: grau {grafo.degree(node)}")
        
        if nx.is_connected(grafo) and grafo.number_of_nodes() > 1:
            print(f"   Grafo é conexo: Sim")
        elif grafo.number_of_nodes() > 1:
            print(f"   Grafo é conexo: Não")
    print("=" * 50)


def menu():
    """Exibe o menu principal"""
    print("\n" + "=" * 50)
    print("       🔷 SISTEMA DE GRAFOS - W/H/O/🔷")
    print("=" * 50)
    print("  1. Adicionar vértice")
    print("  2. Adicionar aresta")
    print("  3. Remover vértice")
    print("  4. Remover aresta")
    print("  5. Listar vértices")
    print("  6. Listar arestas")
    print("  7. Visualizar grafo")
    print("  8. Informações do grafo")
    print("  0. Sair")
    print("=" * 50)
    return input("Escolha uma opção: ")


def main():
    """Função principal do programa"""
    grafo = criar_grafo()
    print("\n🎉 Bem-vindo ao Sistema de Grafos!")
    print("   Desenvolvido em Python para manipulação de grafos.\n")
    print("   Feito e Otimizado pela equipe Wesley, Heloisa e Ortega.\n")
    
    while True:
        opcao = menu()
        
        if opcao == "1":
            vertice = input("\nDigite o nome do vértice: ")
            adicionar_vertice(grafo, vertice)
            
        elif opcao == "2":
            v1 = input("\nDigite o primeiro vértice: ")
            v2 = input("Digite o segundo vértice: ")
            peso_input = input("Digite o peso da aresta (ou Enter para sem peso): ")
            peso = float(peso_input) if peso_input else None
            adicionar_aresta(grafo, v1, v2, peso)
            
        elif opcao == "3":
            listar_vertices(grafo)
            vertice = input("\nDigite o vértice a remover: ")
            remover_vertice(grafo, vertice)
            
        elif opcao == "4":
            listar_arestas(grafo)
            v1 = input("\nDigite o primeiro vértice da aresta: ")
            v2 = input("Digite o segundo vértice da aresta: ")
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
            print("\n👋 Obrigado por usar o Sistema de Grafos! Até logo!\n")
            break
            
        else:
            print("\n⚠ Opção inválida! Tente novamente.")


if __name__ == "__main__":
    main()
