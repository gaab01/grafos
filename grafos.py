"""
Implementação de Grafos usando NetworkX
Permite ao usuário inserir vértices e arestas de forma interativa

Limites:
- Máximo de 10 vértices
- Máximo de 20 arestas
"""

import os
import networkx as nx
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import print as rprint

# Inicializa o console do Rich
console = Console()

# Constantes de limite
MAX_VERTICES = 10
MAX_ARESTAS = 20


def limpar_tela():
    """Limpa o terminal para manter a interface limpa"""
    os.system('cls' if os.name == 'nt' else 'clear')


def criar_grafo():
    """Pergunta ao usuário o tipo de grafo desejado com estilo"""
    limpar_tela()
    console.print(Panel.fit("[bold cyan]Bem-vindo ao Sistema de Grafos![/bold cyan]", border_style="blue"))
    
    console.print("\n[bold]Escolha o tipo de grafo:[/bold]")
    console.print("1. [green]Não Direcionado[/green] (Simples - Arestas de mão dupla)")
    console.print("2. [yellow]Direcionado[/yellow] (Digrafo - Arestas com setas)")
    
    while True:
        resp = Prompt.ask("\n[bold]Opção[/bold]", choices=["1", "2"], default="1")
        if resp == '1':
            return nx.Graph(), "Não Direcionado"
        elif resp == '2':
            return nx.DiGraph(), "Direcionado"


def pausar():
    """Pausa a execução para o usuário ler a mensagem"""
    console.input("\n[italic]Pressione Enter para continuar...[/italic]")


def adicionar_vertice(grafo, vertice):
    # Adiciona um vértice ao grafo, respeitando o limite de 10 vértices
    if grafo.number_of_nodes() >= 10:
        print("Limite máximo de 10 vértices atingido.")
        return

    if vertice in grafo.nodes():
        console.print(f"[bold yellow]⚠ O vértice '{vertice}' já existe.[/bold yellow]")
    else:
        grafo.add_node(vertice)
        console.print(f"[bold green]✔ Vértice '{vertice}' adicionado com sucesso![/bold green]")


def adicionar_aresta(grafo, vertice1, vertice2, peso=None):
    # Adiciona uma aresta ao grafo, respeitando o limite de 20 arestas
    if grafo.number_of_edges() >= 20:
        print("Limite máximo de 20 arestas atingido.")
        return

    if vertice1 not in grafo.nodes() or vertice2 not in grafo.nodes():
        console.print("[bold red]❌ Erro: Ambos os vértices devem existir antes de criar a aresta.[/bold red]")
        return

    if peso is not None:
        grafo.add_edge(vertice1, vertice2, weight=peso)
        print(f"Aresta '{vertice1}' <-> '{vertice2}' (peso: {peso}) adicionada!")
    else:
        grafo.add_edge(vertice1, vertice2)
        print(f"Aresta '{vertice1}' <-> '{vertice2}' adicionada!")


def remover_vertice(grafo, vertice):
    if vertice in grafo.nodes():
        grafo.remove_node(vertice)
        console.print(f"[bold green]✔ Vértice '{vertice}' removido com sucesso![/bold green]")
    else:
        console.print(f"[bold red]❌ Vértice '{vertice}' não encontrado.[/bold red]")


def remover_aresta(grafo, vertice1, vertice2):
    if grafo.has_edge(vertice1, vertice2):
        grafo.remove_edge(vertice1, vertice2)
        print(f"Aresta '{vertice1}' <-> '{vertice2}' removida com sucesso!")
    else:
        print(f"Aresta '{vertice1}' <-> '{vertice2}' não encontrada.")


def listar_vertices(grafo):
    vertices = list(grafo.nodes())
    if not vertices:
        console.print("[italic yellow]O grafo não possui vértices.[/italic yellow]")
        return False

    table = Table(title="Lista de Vértices", show_header=True, header_style="bold magenta")
    table.add_column("Vértice", style="cyan", justify="center")
    table.add_column("Grau", style="green", justify="center")

    for v in vertices:
        table.add_row(str(v), str(grafo.degree(v)))

    console.print(table)
    return True


def listar_arestas(grafo):
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
        console.print("[bold red]O grafo está vazio. Adicione vértices primeiro![/bold red]")
        return

    plt.figure(figsize=(8, 6))
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
        nx.draw_networkx_edge_labels(grafo, pos, edge_labels,
                                     font_color='#E74C3C', # Vermelho suave
                                     font_weight='bold',
                                     rotate=False,         # Texto sempre horizontal fica mais fácil de ler
                                     bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, boxstyle='round,pad=0.2'))

    plt.title(f"Visualização: Grafo {nome_tipo}", fontsize=16, fontweight='bold', color='#333333', pad=20)
    plt.axis('off')
    
    console.print("[bold blue]Abrindo janela de visualização estilizada...[/bold blue]")
    plt.show()


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
            # Verifica conectividade (para DiGraph usa is_weakly_connected ou fortemente, simplificando para is_connected se for Graph)
            if grafo.is_directed():
                conexo = nx.is_weakly_connected(grafo)
                tipo = "Fracamente conexo"
            else:
                conexo = nx.is_connected(grafo)
                tipo = "Conexo"
            print(f"Grafo {tipo}:", "Sim" if conexo else "Não")


def calcular_caminho_curto(grafo, origem, destino):
    # Calcula e exibe o caminho mais curto (Dijkstra)
    try:
        caminho = nx.shortest_path(grafo, source=origem, target=destino, weight='weight')
        custo = nx.shortest_path_length(grafo, source=origem, target=destino, weight='weight')
        
        # Formata o caminho bonitinho
        caminho_str = " -> ".join(caminho)
        console.print(Panel(f"[bold]Caminho:[/bold] {caminho_str}\n[bold]Custo Total:[/bold] {custo}", title="Resultado Dijkstra", style="green"))
    except nx.NetworkXNoPath:
        print(f"\nNão existe caminho entre '{origem}' e '{destino}'.")
    except nx.NodeNotFound as e:
        print(f"\nErro: {e}")


def realizar_busca(grafo, inicio):
    # Realiza uma busca em largura (BFS)
    if inicio not in grafo:
        console.print(f"[bold red]❌ O vértice '{inicio}' não existe.[/bold red]")
        return
    
    # Retorna uma lista com a ordem de visitação
    ordem_visita = list(nx.bfs_tree(grafo, source=inicio))
    console.print(Panel(f"[bold]Ordem de Visita:[/bold] {', '.join(ordem_visita)}", title="Resultado BFS", style="cyan"))


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
    print("  9. Caminho mais curto (Dijkstra)")
    print("  10. Busca em Largura (BFS)")
    print("  0. Sair")
    print("=" * 50)
    return input("Escolha uma opção: ")


def main():
    # Função principal
    grafo = criar_grafo()
    print("\n🎉 Bem-vindo ao Sistema de Grafos!")
    print("   Desenvolvido em Python para manipulação de grafos.\n")
    print("   Feito e Otimizado pela equipe Wesley, Heloisa e Ortega.\n")
    
    while True:
        opcao = menu(tipo_nome)

        if opcao == "0":
            console.print("\n[bold blue]Obrigado por utilizar! Encerrando...[/bold blue]")
            break

        console.print("\n" + "-"*30) # Separador visual

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
            visualizar_grafo(grafo, tipo_nome)

        elif opcao == "8":
            mostrar_informacoes(grafo)


        elif opcao == "9":
            listar_vertices(grafo)
            v1 = input("Vértice de origem: ")
            v2 = input("Vértice de destino: ")
            calcular_caminho_curto(grafo, v1, v2)

        elif opcao == "10":
            listar_vertices(grafo)
            v = input("Vértice inicial da busca: ")
            realizar_busca(grafo, v)

        elif opcao == "0":
            print("Encerrando o programa...")
            print("Obrigado por utilizar nosso código!")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Programa interrompido pelo usuário.[/bold red]")
