"""
Implementação de Grafos usando NetworkX com Interface Melhorada (Rich)
Permite ao usuário inserir vértices e arestas de forma interativa com visual moderno.

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
    if grafo.number_of_nodes() >= MAX_VERTICES:
        console.print(f"[bold red]❌ Limite máximo de {MAX_VERTICES} vértices atingido.[/bold red]")
        return

    if vertice in grafo.nodes():
        console.print(f"[bold yellow]⚠ O vértice '{vertice}' já existe.[/bold yellow]")
    else:
        grafo.add_node(vertice)
        console.print(f"[bold green]✔ Vértice '{vertice}' adicionado com sucesso![/bold green]")


def adicionar_aresta(grafo, vertice1, vertice2, peso=None):
    if grafo.number_of_edges() >= MAX_ARESTAS:
        console.print(f"[bold red]❌ Limite máximo de {MAX_ARESTAS} arestas atingido.[/bold red]")
        return

    if vertice1 not in grafo.nodes() or vertice2 not in grafo.nodes():
        console.print("[bold red]❌ Erro: Ambos os vértices devem existir antes de criar a aresta.[/bold red]")
        return

    if peso is not None:
        grafo.add_edge(vertice1, vertice2, weight=peso)
        console.print(f"[bold green]✔ Aresta '{vertice1}' <-> '{vertice2}' (peso: {peso}) adicionada![/bold green]")
    else:
        grafo.add_edge(vertice1, vertice2)
        console.print(f"[bold green]✔ Aresta '{vertice1}' <-> '{vertice2}' adicionada![/bold green]")


def remover_vertice(grafo, vertice):
    if vertice in grafo.nodes():
        grafo.remove_node(vertice)
        console.print(f"[bold green]✔ Vértice '{vertice}' removido com sucesso![/bold green]")
    else:
        console.print(f"[bold red]❌ Vértice '{vertice}' não encontrado.[/bold red]")


def remover_aresta(grafo, vertice1, vertice2):
    if grafo.has_edge(vertice1, vertice2):
        grafo.remove_edge(vertice1, vertice2)
        console.print(f"[bold green]✔ Aresta '{vertice1}' <-> '{vertice2}' removida com sucesso![/bold green]")
    else:
        console.print(f"[bold red]❌ Aresta '{vertice1}' <-> '{vertice2}' não encontrada.[/bold red]")


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
    if not arestas:
        console.print("[italic yellow]O grafo não possui arestas.[/italic yellow]")
        return False

    table = Table(title="Lista de Arestas", show_header=True, header_style="bold magenta")
    table.add_column("Origem", style="cyan", justify="center")
    table.add_column("Destino", style="cyan", justify="center")
    table.add_column("Peso", style="yellow", justify="center")

    for u, v, data in arestas:
        peso = str(data.get('weight', '-'))
        table.add_row(str(u), str(v), peso)

    console.print(table)
    return True


def visualizar_grafo(grafo, nome_tipo):
    if grafo.number_of_nodes() == 0:
        console.print("[bold red]O grafo está vazio. Adicione vértices primeiro![/bold red]")
        return

    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(grafo, seed=42)
    
    # Desenha
    nx.draw_networkx_nodes(grafo, pos, node_color='#87CEFA', node_size=800, alpha=0.9)
    # Usa setas se for direcionado
    arrows = grafo.is_directed()
    nx.draw_networkx_edges(grafo, pos, edge_color='#404040', width=2, alpha=0.7, arrows=arrows)
    nx.draw_networkx_labels(grafo, pos, font_size=12, font_weight='bold')
    
    edge_labels = nx.get_edge_attributes(grafo, 'weight')
    if edge_labels:
        nx.draw_networkx_edge_labels(grafo, pos, edge_labels)

    plt.title(f"Visualização: Grafo {nome_tipo}")
    plt.axis('off')
    
    console.print("[bold blue]Abrindo janela de visualização...[/bold blue]")
    plt.show()
    console.print("[bold green]Visualização fechada.[/bold green]")


def mostrar_informacoes(grafo, nome_tipo):
    num_nos = grafo.number_of_nodes()
    num_arestas = grafo.number_of_edges()
    
    texto_info = f"[bold]Tipo:[/bold] {nome_tipo}\n"
    texto_info += f"[bold]Total de Vértices:[/bold] {num_nos}\n"
    texto_info += f"[bold]Total de Arestas:[/bold] {num_arestas}\n"
    
    if num_nos > 0:
        if grafo.is_directed():
            conexo = nx.is_weakly_connected(grafo)
            str_conexo = f"Fracamente Conexo: {'Sim' if conexo else 'Não'}"
        else:
            conexo = nx.is_connected(grafo)
            str_conexo = f"Conexo: {'Sim' if conexo else 'Não'}" if num_nos > 1 else "Conexo: Sim (único nó)"
        
        texto_info += f"[bold]{str_conexo}[/bold]"

    panel = Panel(texto_info, title="[bold white on blue] Informações do Grafo [/bold white on blue]", expand=False)
    console.print(panel)


def calcular_caminho_curto(grafo):
    if not listar_vertices(grafo): return
    
    console.print("\n[bold]Cálculo de Caminho Mais Curto (Dijkstra)[/bold]")
    origem = Prompt.ask("Vértice de [green]origem[/green]")
    destino = Prompt.ask("Vértice de [red]destino[/red]")

    try:
        caminho = nx.shortest_path(grafo, source=origem, target=destino, weight='weight')
        custo = nx.shortest_path_length(grafo, source=origem, target=destino, weight='weight')
        
        # Formata o caminho bonitinho
        caminho_str = " -> ".join(caminho)
        console.print(Panel(f"[bold]Caminho:[/bold] {caminho_str}\n[bold]Custo Total:[/bold] {custo}", title="Resultado Dijkstra", style="green"))
    except nx.NetworkXNoPath:
        console.print(f"[bold red]❌ Não existe caminho entre '{origem}' e '{destino}'.[/bold red]")
    except nx.NodeNotFound as e:
        console.print(f"[bold red]❌ Erro: Vértice não encontrado.[/bold red]")


def realizar_busca(grafo):
    if not listar_vertices(grafo): return

    console.print("\n[bold]Busca em Largura (BFS)[/bold]")
    inicio = Prompt.ask("Vértice inicial")

    if inicio not in grafo:
        console.print(f"[bold red]❌ O vértice '{inicio}' não existe.[/bold red]")
        return
    
    ordem_visita = list(nx.bfs_tree(grafo, source=inicio))
    console.print(Panel(f"[bold]Ordem de Visita:[/bold] {', '.join(ordem_visita)}", title="Resultado BFS", style="cyan"))


def menu(nome_tipo):
    limpar_tela()
    console.print(Panel(f"[bold white]Grafo Atual: {nome_tipo}[/bold white]", style="blue"))
    
    table = Table(show_header=False, box=None)
    table.add_column("Opção", style="bold cyan", width=4)
    table.add_column("Descrição")

    table.add_row("1", "Adicionar Vértice")
    table.add_row("2", "Adicionar Aresta")
    table.add_row("3", "Remover Vértice")
    table.add_row("4", "Remover Aresta")
    table.add_row("5", "Listar Vértices")
    table.add_row("6", "Listar Arestas")
    table.add_row("7", "Visualizar Grafo")
    table.add_row("8", "Informações Detalhadas")
    table.add_row("9", "Caminho Mais Curto (Dijkstra)")
    table.add_row("10", "Busca em Largura (BFS)")
    table.add_row("0", "[red]Sair[/red]")

    console.print(Panel(table, title="[bold]Menu Principal[/bold]", border_style="green"))
    return Prompt.ask("Escolha uma opção", choices=[str(i) for i in range(11)])


def main():
    while True:
        try:
            grafo, tipo_nome = criar_grafo()
            break
        except Exception:
            pass # Continua se der erro na criação (não deve ocorrer)

    while True:
        opcao = menu(tipo_nome)

        if opcao == "0":
            console.print("\n[bold blue]Obrigado por utilizar! Encerrando...[/bold blue]")
            break

        console.print("\n" + "-"*30) # Separador visual

        if opcao == "1":
            v = Prompt.ask("Nome do vértice")
            adicionar_vertice(grafo, v)

        elif opcao == "2":
            v1 = Prompt.ask("Vértice de origem")
            v2 = Prompt.ask("Vértice de destino")
            usa_peso = Confirm.ask("Essa aresta tem peso?", default=False)
            peso = None
            if usa_peso:
                while True:
                    try:
                        peso = float(Prompt.ask("Valor do peso"))
                        break
                    except ValueError:
                        console.print("[red]Valor inválido![/red]")
            
            adicionar_aresta(grafo, v1, v2, peso)

        elif opcao == "3":
            listar_vertices(grafo)
            v = Prompt.ask("Vértice a remover")
            remover_vertice(grafo, v)

        elif opcao == "4":
            listar_arestas(grafo)
            v1 = Prompt.ask("Primeiro vértice")
            v2 = Prompt.ask("Segundo vértice")
            remover_aresta(grafo, v1, v2)

        elif opcao == "5":
            listar_vertices(grafo)

        elif opcao == "6":
            listar_arestas(grafo)

        elif opcao == "7":
            visualizar_grafo(grafo, tipo_nome)

        elif opcao == "8":
            mostrar_informacoes(grafo, tipo_nome)

        elif opcao == "9":
            calcular_caminho_curto(grafo)

        elif opcao == "10":
            realizar_busca(grafo)

        # Pausa para o usuário ver o resultado antes de limpar a tela pro menu
        pausar()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Programa interrompido pelo usuário.[/bold red]")
