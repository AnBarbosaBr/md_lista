import sys
import os
import numpy as np 
import pandas as pd
from collections import namedtuple

Separacao = namedtuple("Separacao", ["atributo","tipo", "limiar"])
EntropiaDaDivisao = namedtuple("EntropiaDaDivisao", ["atributo_de_divisao","entropia"])
TreeStructure = namedtuple("TreeStructure", ["separacao","menores","maiores"])


def encontra_melhor_separacao(coluna, classes):
    atributo = coluna.name
    print(f"encontra_melhor_separacao para {atributo}.")
    limiar = coluna.mean()
    return Separacao(atributo, limiar)

def entropia(pertencem_a_classe, total):
    probabilidade_de_pertencer_a_classe = pertencem_a_classe/total
    return -(probabilidade_de_pertencer_a_classe*log(probabilidade_de_pertencer_a_classe))

def calcula_entropia_do_grupo(coluna, classes):
    classes_unicas = classes.unique()
    total = len(classes)
    entropia_acumulada = 0
    for classe in classes_unicas:
        pertencem_a_classe = sum(classe==classes)
        entropia_classe = entropia(pertencem_a_classe, total)
        entropia_acumulada = entropia_acumulada + entropia_classe
        
    return entropia_acumulada


def calcula_entropia(coluna, classes, separacao):
    atributo = coluna.name

    if(separacao.tipo == ATRIBUTO_CONTINUO):
        dados_divisao_abaixo, classes_divisao_abaixo = separa_dados_abaixo(dados, classes, separacao)
        dados_divisao_acima, classes_divisao_acima = separa_dados_acima(dados, classes, separacao)
        entropia = calcula_entropia_do_grupo(dados_divisao_abaixo, classes_divisao_abaixo) + calcula_entropia_do_grupo(dados_divisao_acima, classes_divisao_acima)
    else:
        grupos, classes = separa_categorias(coluna, classes)
        entropia = sum([calcula_entropia_do_grupo(grupo, classe) for grupo, classe in zip(grupos, classes)])



    print(f"calcula_entropia para {atributo}: {entropia}.")

    return EntropiaDaDivisao(coluna.name, entropia)
    
def separa_categorias(colunas, classes):
    pass
        
def separa_dados_abaixo(colunas, classes, separacao):
    atributo = separacao.atributo
    limiar = separacao.limiar
    print(f"separa_dados_abaixo para {atributo} abaixo de {limiar}")
    
def separa_dados_acima(colunas, classes, separacao):
    print(f"separa_dados_acima para {coluna}, {classes}, {separacao}")
    

def arvore(dados, classes):
    # entropia = calcula_entropia(dados, classes) -> Não é necessário, já que será o mesmo valor para todos os filhos
    colunas = dados.columns
    separacoes_dos_atributos = [encontra_melhor_separacao(dados[coluna], classes) for coluna in colunas]
    entropias = [calcula_entropia(dados[separacao.atributo], classes, separacao) for separacao in separacoes_dos_atributos]
    melhor_separacao = max(entropias, key = lambda sep: sep.entropia)

    dados_divisao_abaixo, classes_divisao_abaixo = separa_dados_abaixo(dados, classes, melhor_separacao)
    dados_divisao_acima, classes_divisao_acima = separa_dados_acima(dados, classes, melhor_separacao)

    return TreeStructure(separacao = melhor_separacao,
                     menores = arvore(dados_divisao_abaixo, classes_divisao_abaixo),
                     maiores = arvore(dados_divisao_acima, classes_divisao_acima))
    









if (__name__ == "__main__"):
    path = os.path.join(".","data","iris.csv")
    is(len(sys.argv > 1)):
        path = str(sys.argv[1])

    alvo = pd.read_csv(path)

    X = alvo.iloc[ : , 0:-1] # Seleciona todas as colunas menos a ultima
    y = alvo.iloc[ : , -1]   # Seleciona a ultima coluna

    arvore = arvore(X, y)




