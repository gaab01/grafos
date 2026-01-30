"""
Implementação de Grafos usando NetworkX com Interface Melhorada (Rich)

Funcionalidades:
- Grafos direcionados e não direcionados
- Pesos nas arestas
- Caminho mais curto (Dijkstra)
- Busca em largura (BFS)
- Grafo pré-definido direcionado
- Visualização gráfica
- Limites: 10 vértices / 20 arestas
"""

import os

# Verificação de dependências
try:
    import networkx as nx
    import matplotlib.pyplot as plt
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
except ModuleNotFoundError as e:
    print("Erro: dependência não instalada.")
    print("Execute:")
    print("python -m pip install networkx matplotlib rich")
    raise SystemExit(1)

console = Console()

MAX_VERTICES = 10
MAX_ARESTAS = 20


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    console.input("\n[italic]Pressione Enter para continuar...[/italic]")


def criar_grafo():
    limpar_tela()
    console.print(Panel.fit("[bold cyan]Sistema de Grafos[/bold cyan]", border_style="blue"))

    console.print("\n[bold]Escolha o tipo de grafo:[/bold]")
    console.print("1. Não Direcionado")
    console.print("2. Direcionado")

    opcao = Prompt.ask("Opção", choices=["1", "2"], default="1")

    if opcao == "1":
        return nx.Graph(), "Não Direcionado"
    else:
        return nx.DiGraph(), "Direcionado"


def adicionar_vertice(grafo, vertice):
    if grafo.number_of_nodes() >= MAX_VERTICES:
        console.print("[red]Limite de vértices atingido.[/red]")
        return
    if vertice in grafo:
        console.print("[yellow]Vértice já existe.[/yellow]")
    else:
        grafo.add_node(vertice)
        console.print(f"[green]Vértice '{vertice}' adicionado.[/green]")


def adicionar_aresta(grafo, v1, v2, peso=None):
    if grafo.number_of_edges() >= MAX_ARESTAS:
        console.print("[red]Limite de arestas atingido.[/red]")
        return
    if v1 not in grafo or v2 not in grafo:
        console.print("[red]Os dois vértices devem existir.[/red]")
        return
    grafo.add_edge(v1, v2, weight=peso)
    console.print("[green]Aresta adicionada com sucesso.[/green]")


def remover_vertice(grafo, v):
    if v in grafo:
        grafo.remove_node(v)
        console.print("[green]Vértice removido.[/green]")
    else:
        console.print("[red]Vértice não encontrado.[/red]")


def remover_aresta(grafo, v1, v2):
    if grafo.has_edge(v1, v2):
        grafo.remove_edge(v1, v2)
        console.print("[green]Aresta removida.[/green]")
    else:
        console.print("[red]Aresta não encontrada.[/red]")


def listar_vertices(grafo):
    if not grafo.nodes():
        console.print("[yellow]Nenhum vértice no grafo.[/yellow]")
        return False

    table = Table(title="Vértices")
    table.add_column("Vértice")
    table.add_column("Grau")

    for v in grafo.nodes():
        table.add_row(str(v), str(grafo.degree(v)))

    console.print(table)
    return True


def listar_arestas(grafo):
    if not grafo.edges():
        console.print("[yellow]Nenhuma aresta no grafo.[/yellow]")
        return

    table = Table(title="Arestas")
    table.add_column("Origem")
    table.add_column("Destino")
    table.add_column("Peso")

    for u, v, d in grafo.edges(data=True):
        table.add_row(str(u), str(v), str(d.get("weight", "-")))

    console.print(table)


def visualizar_grafo(grafo, nome_tipo):
    if grafo.number_of_nodes() == 0:
        console.print("[red]Grafo vazio.[/red]")
        return

    pos = nx.spring_layout(grafo, seed=42, k=1.5)

    plt.figure(figsize=(10, 7))
    nx.draw_networkx_nodes(grafo, pos, node_size=1200, node_color="#4A90E2")
    nx.draw_networkx_labels(grafo, pos, font_color="white", font_weight="bold")

    nx.draw_networkx_edges(
        grafo, pos,
        arrows=grafo.is_directed(),
        arrowstyle='-|>',
        arrowsize=25,
        width=2,
        alpha=0.7
    )

    labels = nx.get_edge_attributes(grafo, 'weight')
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=labels)

    plt.title(f"Grafo {nome_tipo}")
    plt.axis("off")
    plt.show()


def mostrar_informacoes(grafo, nome_tipo):
    texto = f"""
Tipo: {nome_tipo}
Vértices: {grafo.number_of_nodes()}
Arestas: {grafo.number_of_edges()}
"""
    console.print(Panel(texto, title="Informações do Grafo"))


def calcular_caminho_curto(grafo):
    if not listar_vertices(grafo):
        return
    o = Prompt.ask("Origem")
    d = Prompt.ask("Destino")
    try:
        caminho = nx.shortest_path(grafo, o, d, weight='weight')
        custo = nx.shortest_path_length(grafo, o, d, weight='weight')
        console.print(Panel(f"Caminho: {' -> '.join(caminho)}\nCusto: {custo}", title="Dijkstra"))
    except:
        console.print("[red]Caminho inexistente.[/red]")


def realizar_busca(grafo):
    if not listar_vertices(grafo):
        return
    inicio = Prompt.ask("Vértice inicial")
    if inicio not in grafo:
        console.print("[red]Vértice inválido.[/red]")
        return
    ordem = list(nx.bfs_tree(grafo, inicio))
    console.print(Panel(", ".join(ordem), title="BFS"))


def gerar_grafo_predefinido(grafo):
    """Cria um grafo de exemplo. Oferece opções para sobrescrever, mesclar ou cancelar.

    - Sobrescrever: apaga o grafo atual e cria o grafo pré-definido
    - Mesclar: adiciona nós/arestas do grafo pré-definido ao grafo atual
    - Cancelar: não faz nada
    """
    vertices = ["A", "B", "C", "D", "E"]
    arestas = [
        ("A", "B", 2),
        ("A", "C", 4),
        ("B", "C", 1),
        ("B", "D", 7),
        ("C", "E", 3),
        ("D", "E", 1)
    ]

    # Mostra pré-visualização do grafo de exemplo
    table = Table(title="Pré-visualização: Grafo pré-definido")
    table.add_column("Origem", justify="center")
    table.add_column("Destino", justify="center")
    table.add_column("Peso", justify="center")
    for u, v, p in arestas:
        table.add_row(u, v, str(p))

    console.print(table)

    console.print("[bold]Ações disponíveis:[/bold]")
    console.print("1. [red]Sobrescrever[/red] (apaga o grafo atual e cria o de exemplo)")
    console.print("2. [green]Mesclar[/green] (adiciona nós/arestas ao grafo atual)")
    console.print("0. [yellow]Cancelar[/yellow]")

    escolha = Prompt.ask("Escolha", choices=["1", "2", "0"], default="0")

    if escolha == "0":
        console.print("[yellow]Operação cancelada.[/yellow]")
        return

    if escolha == "1":
        grafo.clear()
        grafo.add_nodes_from(vertices)
        for u, v, p in arestas:
            grafo.add_edge(u, v, weight=p)
        console.print("[green]✔ Grafo pré-definido criado (sobrescrito).[/green]")
        return

    # Mesclar
    added_nodes = 0
    added_edges = 0
    for n in vertices:
        if n not in grafo:
            grafo.add_node(n)
            added_nodes += 1

    for u, v, p in arestas:
        if not grafo.has_edge(u, v):
            grafo.add_edge(u, v, weight=p)
            added_edges += 1
        else:
            # Se já existe, não altera o peso por padrão
            pass

    console.print(f"[green]✔ Grafo mesclado: {added_nodes} novos nós, {added_edges} novas arestas adicionadas.[/green]")


def menu(tipo):
    limpar_tela()
    console.print(Panel(f"Grafo Atual: {tipo}", style="blue"))

    opções = {
        "1": "Adicionar vértice",
        "2": "Adicionar aresta",
        "3": "Remover vértice",
        "4": "Remover aresta",
        "5": "Listar vértices",
        "6": "Listar arestas",
        "7": "Visualizar grafo",
        "8": "Informações",
        "9": "Caminho mais curto",
        "10": "Busca BFS",
        "11": "Gerar grafo pré-definido",
        "0": "Sair"
    }

    table = Table(show_header=False)
    for k, v in opções.items():
        table.add_row(k, v)

    console.print(table)
    return Prompt.ask("Escolha", choices=list(opções.keys()))


def main():
    grafo, tipo = criar_grafo()

    while True:
        opcao = menu(tipo)

        if opcao == "0":
            break
        elif opcao == "1":
            adicionar_vertice(grafo, Prompt.ask("Nome"))
        elif opcao == "2":
            adicionar_aresta(
                grafo,
                Prompt.ask("Origem"),
                Prompt.ask("Destino"),
                float(Prompt.ask("Peso")) if Confirm.ask("Tem peso?") else None
            )
        elif opcao == "3":
            remover_vertice(grafo, Prompt.ask("Vértice"))
        elif opcao == "4":
            remover_aresta(grafo, Prompt.ask("Origem"), Prompt.ask("Destino"))
        elif opcao == "5":
            listar_vertices(grafo)
        elif opcao == "6":
            listar_arestas(grafo)
        elif opcao == "7":
            visualizar_grafo(grafo, tipo)
        elif opcao == "8":
            mostrar_informacoes(grafo, tipo)
        elif opcao == "9":
            calcular_caminho_curto(grafo)
        elif opcao == "10":
            realizar_busca(grafo)
        elif opcao == "11":
            gerar_grafo_predefinido(grafo)

        pausar()


if __name__ == "__main__":
    main()
