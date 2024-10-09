import oracledb as orcl
import pandas as pd


def main():
    conexao, str_connect, inst_SQL = conectar_banco()
    resp = 1
    while (resp != 0 and conexao == True):
        print("1 - Inserção de algum aluno: ")
        print("2 - Alteração")
        print("3 - Exclusão")
        print("4 - Exibição de todos os alunos")
        print("5 - Sair")
        opc = int(input("Digite a opção desejada (1 a 5):"))
        match opc:
            case 1:
                try:
                    rm = int(input("Digite o RM do aluno: "))
                    nome = input("Digite o nome do aluno: ")
                    curso = input("Digite o curso do aluno: ")
                    idade = int(input("Digite a idade do aluno: "))
                except ValueError:
                    print("Digite dados numericos!")
                else:
                    str_insert = f"""INSERT INTO alunos (aluno_rm, aluno_nome, aluno_curso, aluno_idade) VALUES ({rm},'{nome}', '{curso}',{idade})"""
                    executar_SQL(str_connect, inst_SQL, str_insert)
            case 2:
                lista_dados = []
                id = int(input("Digite o id do aluno a ser alterado: "))
                str_consulta = f"""SELECT * FROM ALUNOS WHERE ALUNO_ID = {id} """
                inst_SQL.execute(str_consulta)

                dados = inst_SQL.fetchall()
                for dado in dados:
                    lista_dados.append(dado)

                if (len(lista_dados) == 0):
                    print("O id do aluno não existe na tabela")
                else:
                    try:
                        rm = int(input("Digite o RM do aluno: "))
                        nome = input("Digite o nome do aluno: ")
                        curso = input("Digite o curso do aluno: ")
                        idade = int(input("Digite a idade do aluno: "))
                    except ValueError:
                        print("Digite dados numericos!")
                    else:
                        str_update = f"""UPDATE alunos set aluno_rm = {rm}, aluno_nome='{nome}', aluno_curso='{curso}, aluno_idade={idade} WHERE aluno_id = {id}'"""
                        executar_SQL(str_connect, inst_SQL, str_update)
            case 3:
                lista_dados = []
                id = int(input("Digite o id do aluno a ser excluido: "))
                str_consulta = f"""SELECT * FROM ALUNOS WHERE ALUNO_ID = {id} """
                inst_SQL.execute(str_consulta)

                dados = inst_SQL.fetchall()
                for dado in dados:
                    lista_dados.append(dado)

                if (len(lista_dados) == 0):
                    print("O id do aluno não existe na tabela")
                else:
                    try:
                        str_exclusao = f"""DELETE FROM ALUNOS WHERE aluno_id = {id}"""
                    except ValueError:
                        print("Digite um valor numérico")
                    else:
                        executar_SQL(str_connect, inst_SQL, str_exclusao)
            case 4:
                lista_dados = []
                inst_SQL.execute("SELECT * FROM ALUNOS")
                dados = inst_SQL.fetchall()

                for dado in dados:
                    lista_dados.append(dado)
                df_alunos = pd.DataFrame.from_records(lista_dados, columns=['ID', 'RM', 'NOME', 'CURSO', 'IDADE'], index=['ID'])
                if (df_alunos.empty):
                    print("Não existe dados na tabela")
                else:
                    print(df_alunos)
                    print("\n")

            case _:
                print("Opção invalida!")
        resp = int(input("Deseja continuar? "))
def conectar_banco():
    try:
        dados_serv = orcl.makedsn("oracle.fiap.com.br", 1521, "ORCL")
        str_connect = orcl.connect(user="xxxxx",password="xxxxx", dsn=dados_serv)

        inst_SQL = str_connect.cursor()
    except Exception as e:
        print(f"Erro: {e}")
        conexao = False
        str_connect = ""
        inst_SQL = ""
    else:
        conexao = True
    return (conexao, str_connect, inst_SQL)


def executar_SQL(str_connect, inst_SQL, str_SQL):
    try:
        inst_SQL.execute(str_SQL)
        str_connect.commit()
    except Exception as e:
        print(f"Erro: {e}")
    else:
        print("Transação relaizada com sucesso")

if __name__ == "__main__":
    main()