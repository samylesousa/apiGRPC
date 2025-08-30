import grpc

def createProfessorImport(stub, dados_pb2, request):
    try:
        professor = stub.CreateProfessor(dados_pb2.CreateProfessorRequest(
            nome=request["nome"],
            vertente=request["vertente"] if "vertente" in request else None,
            telefone=request["telefone"] if "telefone" in request else None,
            email=request["email"] if "email" in request else None,
            website=request["website"] if "website" in request else None,
            formacao=request["formacao"] if "formacao" in request else None,
        ))
        print(f'Nome: {professor.nome} Professor criado:{professor.email} (Website: {professor.website})')
    except grpc.RpcError as e:
        print(f"Erro ao criar o professor: {e.code()}: {e.details()}")
        return        
       

def getAllProfessoresImport(stub, dados_pb2):
    try:
        todos_professores = stub.ListProfessores(dados_pb2.ListProfessoreRequest())
        for professor in todos_professores.professores:
            print(f'Nome: {professor.nome} Email:{professor.email}')
    except grpc.RpcError as e:
        print(f"Erro ao listar os professores:{e.code()}: {e.details()}")
        
def getProfessorElementImport(stub, dados_pb2, request):
    try:
        #falta adicionar a parte de formação
        professores_filtrados = stub.ListProfessores(dados_pb2.ListProfessoreRequest(vertente=request["vertente"]))
        for professor in professores_filtrados.professores:
            print(f'Nome: {professor.nome} Email:{professor.email} (Website: {professor.website})')
    except grpc.RpcError as e:
        print(f"Erro ao filtrar os professores: {e.code(): {e.details()}}")
        
def getProfessorIdImport(stub, dados_pb2, request):
    try:
        professor_especifico = stub.GetProfessor(dados_pb2.ProfessorRequest(id=request["id"]))
        print(f'Nome: {professor_especifico.nome} Email:{professor_especifico.email} (Website: {professor_especifico.website})')
    except grpc.RpcError as e:
        print(f"Erro ao obter o professor específico: {e.code(): {e.details()}}")


def updateProfessorImport(stub, dados_pb2, request):
    try:
        professor_atual = stub.UpdateProfessor(dados_pb2.Professor(
            id=request["id"],
            nome=request["nome"],
            vertente=request["vertente"] if "vertente" in request else None,
            telefone=request["telefone"] if "telefone" in request else None,
            email=request["email"] if "email" in request else None,
            website=request["website"] if "website" in request else None,
            formacao=request["formacao"] if "formacao" in request else None,
        ))
        print(f"Professor atualizado: {professor_atual.nome}")
    except grpc.RpcError as e:
        print(f"Erro ao atualizar o professor: {e.code()}: {e.details()}")


def deleteProfessorImport(stub, dados_pb2, request):
    try:
        stub.DeleteProfessor(dados_pb2.ProfessorRequest(id=request["id"]))
        print(f"Professor deletado")
    except grpc.RpcError as e:
        print(f"Erro ao deletar o professor: {e.code()}: {e.details()}")
