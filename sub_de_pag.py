import sys

ARQUIVO = "entradaMV.txt"


def fifo(quadros, refs):
    # FIFO: a página que entrou primeiro é a primeira a sair
    memoria = []
    faltas = 0

    for pag in refs:
        if pag not in memoria: #se nao tiver na memoria +1 nas faltas de pagina
            faltas += 1
            if len(memoria) < quadros:
                # ainda há espaço livre — só adiciona
                memoria.append(pag)
            else:
                # remove a página mais antiga (primeira da fila) e insere a nova
                memoria.pop(0)
                memoria.append(pag)

    return faltas


def otm(quadros, refs): #em um SO, é impossivel, mas aqui tem a lista completa, então ele sabe as proximas paginas
    
    # OTM: substitui a página que será usada mais tarde no futuro (algoritmo ótimo)
    memoria = []
    faltas = 0

    for i, pag in enumerate(refs):
        if pag not in memoria: #essa parte vai ser igual para todos
            faltas += 1
            if len(memoria) < quadros:
                # ainda há espaço livre — só adiciona
                memoria.append(pag)
            else:
                # para cada página na memória, encontra quando ela será usada novamente
                usos_futuros = []
                for p in memoria:
                    proximos = [j for j in range(i + 1, len(refs)) if refs[j] == p]
                    # se não será mais usada, recebe infinito (prioridade máxima para substituir)
                    usos_futuros.append(proximos[0] if proximos else float('inf'))

                # substitui a página cujo próximo uso é o mais distante
                memoria[usos_futuros.index(max(usos_futuros))] = pag

    return faltas


def lru(quadros, refs):
    # LRU: substitui a página que foi usada há mais tempo
    memoria = []
    faltas = 0

    for pag in refs:
        if pag in memoria:
            # atualiza a ordem: move a página para o final (mais recente)
            memoria.remove(pag)
            memoria.append(pag)
        else:
            faltas += 1
            if len(memoria) < quadros:
                # ainda há espaço livre — só adiciona
                memoria.append(pag)
            else:
                # remove a página menos recentemente usada (primeira da lista)
                memoria.pop(0)
                memoria.append(pag)

    return faltas


def ler_entrada(caminho):
    with open(caminho) as f:
        nums = list(map(int, f.read().split()))
    quadros = nums[0] #primeiro numero é o numero de quadros
    refs    = nums[1:]
    return quadros, refs


def main():
    try:
        quadros, refs = ler_entrada(ARQUIVO)
    except FileNotFoundError:
        print(f"Arquivo '{ARQUIVO}' não encontrado.")
        sys.exit(1)

    for nome, fn in [("FIFO", fifo), ("OTM", otm), ("LRU", lru)]:
        print(f"{nome} {fn(quadros, refs)}")


if __name__ == "__main__":
    main()
